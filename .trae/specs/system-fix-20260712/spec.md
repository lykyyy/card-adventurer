# 系统修正实施规范 Spec

## Why
基于2026-07-12系统全面核实报告，当前项目存在81个实质性问题（12个P0致命、28个P1严重、35个P2一般、6项剩余待处理事项），其中4个P0问题需要用户决策后才能推进。规则文件层已修复完毕，但数据层、代码层、GDD内容层完全未修复。本规范定义分阶段修正方案，按优先级逐步解决所有问题。

## What Changes
- **阶段0（用户决策）**：裁定4个P0决策项（MAT-003/004名称、P-002~004归属、禁止清单、职业规划）
- **阶段1（ID体系修复）**：统一ID格式、补注册92个未注册ID、更新cards.csv为有效卡牌、补全ID-ALIAS和ID-REFERENCE-GRAPH
- **阶段2（CSV数据修复）**：修复equipment_slots.csv结构、修复profession外键、同步CSV列结构与_schema.csv（11处）、修正本地化文件格式、修复CSV数据值问题（8处）
- **阶段3（GDD/TDD/PDD修复）**：同步版本号（6处）、修正GDD内部链接格式、修正TDD命名规范、修正PDD状态机、清理loadCSV幻觉、补充executeEffect函数、修正PDD拼写错误和内部矛盾、为5个GDD系统生成TDD/PDD
- **阶段4（代码同步）**：统一代码中ID格式、同步状态机到代码、对齐EMBEDDED_CSV描述
- **阶段5（自动化实现）**：实现8个校验脚本、配置Git pre-commit hook

## Impact
- Affected specs: 无（首次系统修正规范）
- Affected code: [scripts/index.html](file:///d:/game/card-adventurer/scripts/index.html)
- Affected docs: 全部GDD/TDD/PDD/ID-REGISTRY/ID-ALIAS/ID-REFERENCE-GRAPH
- Affected data: 全部CSV文件（15个）

---

## ADDED Requirements

### Requirement: 阶段0 — 用户决策裁定
系统 SHALL 在开始任何数据/代码修改前，由用户完成4个P0决策项的裁定。

#### Scenario: 用户裁定ID-REGISTRY与GDD内容冲突
- **WHEN** MAT-003/MAT-004名称在ID-REGISTRY与GDD-CRAFTING-001中存在冲突
- **THEN** 用户选择权威定义来源（ID-REGISTRY 或 GDD-CRAFTING-001）
- **AND** 裁决结果记录在.changelog.md中

#### Scenario: 用户裁定P-002~P-004职业归属
- **WHEN** P-002/P-003/P-004在GDD-CRAFTING-001中已定义但ID-REGISTRY未注册
- **THEN** 用户确认职业归属（法师/盗贼/牧师对应编号）
- **AND** 确认后注册到ID-REGISTRY

#### Scenario: 用户裁定禁止清单与职业规划
- **WHEN** GDD-CHARACTER-001禁止清单与GDD-CORE-001职业规划矛盾
- **THEN** 用户选择以哪份GDD为权威来源
- **AND** 另一份GDD同步更新

### Requirement: 阶段1 — ID体系修复
系统 SHALL 完成ID格式统一、未注册ID补注册、废弃ID替换、ID-ALIAS和ID-REFERENCE-GRAPH补全。

#### Scenario: 统一ID格式
- **WHEN** 用户确认权威ID格式（C-001带连字符 或 C001无连字符）
- **THEN** 全项目所有ID引用统一为权威格式
- **AND** 波及范围：ID-REGISTRY、全部GDD、全部CSV、全部TDD/PDD、scripts/index.html

#### Scenario: 补注册未注册ID
- **WHEN** 约92个ID未在ID-REGISTRY注册
- **THEN** 在ID-REGISTRY中补充注册所有未注册ID
- **AND** 每个新增注册包含：元素类型/名称/定义源文件/功能描述

#### Scenario: 更新cards.csv为有效卡牌
- **WHEN** cards.csv使用6个废弃编号（C001-C007）
- **THEN** 替换为ID-REGISTRY中已注册的有效卡牌编号（C-080~C-094等）
- **AND** 卡牌数据与GDD-COMBAT-001定义一致

#### Scenario: 补全ID-ALIAS
- **WHEN** ID-ALIAS.md为"暂无别名"空模板
- **THEN** 记录8个废弃编号的别名映射（C-001~C-009 → 废弃+替代编号）
- **AND** 格式：旧编号 → 新编号 + 废弃原因

#### Scenario: 补全ID-REFERENCE-GRAPH
- **WHEN** ID-REFERENCE-GRAPH.md只列出4个前缀
- **THEN** 补充所有15个已注册前缀的跨系统引用关系
- **AND** 记录每个前缀在各系统中的引用位置

### Requirement: 阶段2 — CSV数据修复
系统 SHALL 修复所有CSV文件的列结构、外键、枚举值、数据值问题，使其与_schema.csv定义完全一致。

#### Scenario: 修复equipment_slots.csv结构
- **WHEN** equipment_slots.csv实际为键值对规则而非装备栏位数据
- **THEN** 重写为slot_id/name_zh/slot_type结构
- **AND** 数据与GDD-EQUIPMENT系统定义一致

#### Scenario: 修复profession外键
- **WHEN** professions.csv和profession_starting_deck.csv使用prof_id而非profession_id
- **THEN** 统一为_schema.csv定义的列名
- **AND** 更新_foreign_keys.csv中对应的外键定义

#### Scenario: 同步CSV列结构与_schema.csv
- **WHEN** 11个CSV文件的列名与_schema.csv定义不一致
- **THEN** 逐一修正为schema定义的标准列名
- **AND** 涉及文件：card_effects.csv/enemy_skills.csv/professions.csv/profession_starting_deck.csv/status_effects.csv/skill_texts.csv/cards.csv/enemies.csv/races.csv/skills.csv/leveling.csv

#### Scenario: 修正本地化文件格式
- **WHEN** element_names.csv和skill_texts.csv缺少#注释行、列名使用大写
- **THEN** 添加#注释行、列名改为小写下划线格式
- **AND** 数据内容保持不变

#### Scenario: 修复CSV数据值问题
- **WHEN** 8处CSV数据值存在范围越界、枚举违规、外键引用无效等问题
- **THEN** 逐一修正为合规值
- **AND** 修正后通过外键完整性校验

### Requirement: 阶段3 — GDD/TDD/PDD文档修复
系统 SHALL 修复所有文档的版本号同步、内部链接格式、TDD命名、PDD内容一致性等问题。

#### Scenario: 同步版本号
- **WHEN** 6处GDD/TDD/PDD的frontmatter版本号与变更日志不一致
- **THEN** 以变更日志中的最新版本号为准，更新frontmatter
- **AND** 涉及文件：GDD-CORE-001/GDD-CHARACTER-001/GDD-COMBAT-001/GDD-CRAFTING-001/TDDH-COMBAT-001/_schema.csv

#### Scenario: 修正GDD内部链接格式
- **WHEN** GDD中使用裸ID引用（如C-001~C-003）而非Obsidian内部链接
- **THEN** 替换为[[ID-REGISTRY|显示文本]]格式
- **AND** 涉及所有GDD文件中的跨文件ID引用

#### Scenario: 修正TDD命名规范
- **WHEN** TDD文件使用TDDH/TDDG前缀而非规则定义的TDD-{系统}-{序号}-html/godot格式
- **THEN** 重命名文件为规范格式
- **AND** 更新所有引用这些TDD的文档

#### Scenario: 修正PDD状态机
- **WHEN** PDD-COMBAT-001状态机定义与scripts/index.html实际代码不一致
- **THEN** 以代码为准更新PDD状态机定义
- **AND** 新增battle_end状态，移除不存在的victory/defeat独立状态

#### Scenario: 清理loadCSV幻觉
- **WHEN** TDD/PDD描述loadCSV(filename)异步fetch接口但代码使用EMBEDDED_CSV对象
- **THEN** 将TDD/PDD中的loadCSV描述替换为EMBEDDED_CSV机制
- **AND** 函数清单中移除loadCSV，新增EMBEDDED_CSV数据说明

#### Scenario: 补充executeEffect函数到PDD
- **WHEN** scripts/index.html存在executeEffect函数但PDD §3函数清单未记录
- **THEN** 在PDD-COMBAT-001 §3函数清单中追加executeEffect签名
- **AND** 格式：executeEffect(effectDef, source, target) → 执行单个效果定义

#### Scenario: 修正PDD拼写错误和内部矛盾
- **WHEN** PDD-COMBAT-001:72存在builEnemySkillMap拼写错误
- **THEN** 修正为buildEnemySkillMap
- **AND** 统一数组数量描述（8个数组 vs 6个CSV → 统一为8个CSV）

#### Scenario: 为5个GDD系统生成TDD/PDD
- **WHEN** GDD-CORE-001/GDD-BATTLEFIELD-001/GDD-CHARACTER-001/GDD-CRAFTING-001/GDD-TOWER-001无对应TDD/PDD
- **THEN** 为每个系统生成TDD和PDD文件
- **AND** TDD/PDD必须引用来源GDD ID
- **AND** TDD/PDD中引用的所有ID必须在ID-REGISTRY中注册

### Requirement: 阶段4 — 代码同步
系统 SHALL 将scripts/index.html中的ID格式、状态机实现与修复后的文档保持一致。

#### Scenario: 统一代码中ID格式
- **WHEN** 阶段1已统一ID格式
- **THEN** 更新scripts/index.html中所有卡牌/职业/敌人/技能ID引用
- **AND** 确保与CSV和ID-REGISTRY一致

#### Scenario: 对齐PDD状态机描述
- **WHEN** 阶段3已修正PDD状态机
- **THEN** 确认scripts/index.html中的状态机实现与PDD一致
- **AND** 如有偏差，以PDD为准修正代码或反向修正PDD

### Requirement: 阶段5 — 自动化校验实现
系统 SHALL 实现8个自动化校验脚本并配置Git pre-commit hook，确保后续修改自动通过校验。

#### Scenario: 实现校验脚本
- **WHEN** automation-validation.md定义了8个校验脚本
- **THEN** 在scripts/validation/目录下创建所有脚本
- **AND** 脚本列表：id-registry-check.py/id-format-check.py/csv-schema-check.py/foreign-key-check.py/deprecated-id-check.py/tdd-pdd-coverage.py/version-sync-check.py/alias-graph-check.py
- **AND** 每个脚本支持命令行执行和报告输出

#### Scenario: 配置Git pre-commit hook
- **WHEN** 校验脚本已实现
- **THEN** 创建.git/hooks/pre-commit调用所有校验脚本
- **AND** 任一脚本失败则阻止提交
- **AND** 输出校验报告格式与automation-validation.md定义一致

---

## MODIFIED Requirements
无（首次系统修正规范，无修改现有需求）

## REMOVED Requirements
无