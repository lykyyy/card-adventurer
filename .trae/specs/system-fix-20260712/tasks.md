# 系统修正实施任务清单

## 阶段0：用户决策裁定（阻塞项，必须先完成）

- [x] Task 0.1：裁定MAT-003/MAT-004名称冲突
  - 向用户展示ID-REGISTRY（魔晶碎片/远古遗物）与GDD-CRAFTING-001（魔晶核/星核碎片）的冲突
  - 用户选择权威来源
  - 记录决策到.changelog.md（DEC-20260712-01）

- [x] Task 0.2：裁定P-002/P-003/P-004职业归属
  - 向用户展示GDD-CRAFTING-001中P-002=法师/P-003=盗贼/P-004=牧师的定义
  - 用户确认归属后注册到ID-REGISTRY
  - 记录决策到.changelog.md（DEC-20260712-02）

- [ ] Task 0.3：裁定禁止清单与职业规划矛盾
  - 向用户展示GDD-CHARACTER-001禁止清单（法师在禁止列）与GDD-CORE-001（法师为4基础职业之一）的矛盾
  - 用户选择权威来源
  - 记录决策到.changelog.md（DEC-20260712-03）

- [x] Task 0.4：裁定ID格式权威标准
  - 向用户确认全项目ID格式：C-001（带连字符）还是C001（无连字符）
  - 记录决策到.changelog.md（DEC-20260712-04）

## 阶段1：ID体系修复

- [x] Task 1.1：统一ID-REGISTRY中所有ID格式
  - 根据阶段0裁定结果，修正ID-REGISTRY中所有ID格式
  - 确保所有注册ID遵循统一格式
  - 验证：Grep全项目确认无混合格式

- [x] Task 1.2：补注册约92个未注册ID
  - 从GDD和CSV中提取所有使用但未注册的ID
  - 在ID-REGISTRY中追加注册（含元素类型/名称/定义源/功能描述）
  - 验证：所有ID在ID-REGISTRY中状态为✅已注册

- [ ] Task 1.3：更新cards.csv为有效卡牌ID
  - 替换C001-C007为ID-REGISTRY中已注册的有效卡牌编号
  - 卡牌数据与GDD-COMBAT-001定义对齐
  - 验证：cards.csv中无废弃编号出现

- [ ] Task 1.4：补全ID-ALIAS.md
  - 记录8个废弃编号的别名映射（C-001~C-009结合ID-REGISTRY废弃表）
  - 格式：旧编号→新编号（替代编号）+ 废弃原因
  - 验证：每个废弃编号在ID-ALIAS中有对应映射

- [x] Task 1.5：补全ID-REFERENCE-GRAPH.md
  - 补充所有已注册前缀（C-/E-/P-/S-/EQUIP-/ITEM-/MAT-/PL-/PROF-FEAT-/W-FEAT-/R-FEAT-/F-/LOC-/RES-/MISC-）的跨系统引用关系
  - 记录每个前缀在GDD/CSV/TDD/PDD中的引用位置
  - 验证：每个注册前缀在引用图中有对应记录

- [x] Task 1.6：清洗所有CSV文件中的废弃编号
  - Grep全项目搜索废弃编号（C-001~C-009等）
  - 在CSV中替换为有效编号
  - 验证：Grep确认无废弃编号残留

## 阶段2：CSV数据修复

- [x] Task 2.1：重写equipment_slots.csv
- [x] Task 2.2：修复profession外键
- [x] Task 2.3：同步card_effects.csv列结构
- [x] Task 2.4：同步enemy_skills.csv列结构
- [x] Task 2.5：同步professions.csv列结构
- [x] Task 2.6：同步profession_starting_deck.csv列结构
- [x] Task 2.7：同步status_effects.csv列结构
- [x] Task 2.8：修正本地化文件格式
- [x] Task 2.9：修复CSV多列问题
- [x] Task 2.10：修复CSV数据值问题（8处）
- [x] Task 2.11：更新_schema.csv和_foreign_keys.csv版本号

## 阶段3：GDD/TDD/PDD文档修复

- [ ] Task 3.1：同步GDD-CORE-001版本号
  - frontmatter 0.5.0→1.1.0（与变更日志一致）
  - 验证：frontmatter版本=变更日志最新版本

- [ ] Task 3.2：同步GDD-CHARACTER-001版本号
  - frontmatter 1.0.0→1.1.0（与变更日志一致）
  - 验证：frontmatter版本=变更日志最新版本

- [ ] Task 3.3：同步GDD-COMBAT-001版本号
  - frontmatter 0.3.0→0.4.0（与变更日志一致）
  - 验证：frontmatter版本=变更日志最新版本

- [ ] Task 3.4：同步GDD-CRAFTING-001版本号
  - frontmatter 0.3.0→0.8.0（与变更日志一致）
  - 验证：frontmatter版本=变更日志最新版本

- [ ] Task 3.5：同步TDDH-COMBAT-001和_schema.csv版本号
  - TDDH-COMBAT-001 version与GDD-COMBAT-001 v0.4.0对齐
  - _schema.csv中cards.csv版本与GDD-COMBAT-001 v0.3.0对齐
  - 验证：TDD版本≥GDD版本

- [ ] Task 3.6：修正GDD内部链接格式
  - 所有GDD中的跨文件ID引用改为[[ID-REGISTRY|显示文本]]格式
  - 验证：Grep确认无裸ID引用（排除同文件内引用和数值表）

- [ ] Task 3.7：修正TDD文件命名
  - TDDH-COMBAT-001.md→TDD-COMBAT-001-html.md
  - TDDG-COMBAT-001.md→TDD-COMBAT-001-godot.md
  - 更新所有引用这些TDD的文档
  - 验证：文件名符合规则定义

- [ ] Task 3.8：修正PDD-COMBAT-001状态机
  - 以scripts/index.html实际代码为准，更新状态机定义
  - 状态：idle→battle_start→player_turn→enemy_turn→battle_end（循环player_turn/enemy_turn）
  - 移除不存在的victory/defeat独立状态
  - 验证：PDD状态机与代码Grep结果一致

- [ ] Task 3.9：清理loadCSV幻觉
  - TDDH-COMBAT-001中loadCSV描述替换为EMBEDDED_CSV机制
  - PDD-COMBAT-001中loadCSV描述替换为EMBEDDED_CSV机制
  - 验证：Grep确认TDD/PDD中无loadCSV残留

- [ ] Task 3.10：补充executeEffect函数到PDD
  - 在PDD-COMBAT-001 §3函数清单追加executeEffect(effectDef, source, target)
  - 验证：PDD函数清单包含executeEffect

- [ ] Task 3.11：修正PDD拼写错误和内部矛盾
  - builEnemySkillMap→buildEnemySkillMap（PDD-COMBAT-001:72）
  - 统一数组数量描述：8个数组→8个CSV
  - 验证：Grep确认无builEnemySkillMap残留

- [ ] Task 3.12：为GDD-CORE-001生成TDD和PDD
  - 基于GDD-CORE-001生成TDD-CORE-001-html.md和TDD-CORE-001-godot.md
  - 基于TDD-CORE-001生成PDD-CORE-001.md
  - 验证：TDD/PDD引用GDD-CORE-001 ID，所有ID在ID-REGISTRY中注册

- [ ] Task 3.13：为GDD-BATTLEFIELD-001生成TDD和PDD
  - 基于GDD-BATTLEFIELD-001生成TDD-BATTLEFIELD-001-html.md和TDD-BATTLEFIELD-001-godot.md
  - 基于TDD-BATTLEFIELD-001生成PDD-BATTLEFIELD-001.md
  - 验证：TDD/PDD引用GDD-BATTLEFIELD-001 ID

- [ ] Task 3.14：为GDD-CHARACTER-001生成TDD和PDD
  - 基于GDD-CHARACTER-001生成TDD-CHARACTER-001-html.md和TDD-CHARACTER-001-godot.md
  - 基于TDD-CHARACTER-001生成PDD-CHARACTER-001.md
  - 验证：TDD/PDD引用GDD-CHARACTER-001 ID

- [ ] Task 3.15：为GDD-CRAFTING-001生成TDD和PDD
  - 基于GDD-CRAFTING-001生成TDD-CRAFTING-001-html.md和TDD-CRAFTING-001-godot.md
  - 基于TDD-CRAFTING-001生成PDD-CRAFTING-001.md
  - 验证：TDD/PDD引用GDD-CRAFTING-001 ID

- [ ] Task 3.16：为GDD-TOWER-001生成TDD和PDD
  - 基于GDD-TOWER-001生成TDD-TOWER-001-html.md和TDD-TOWER-001-godot.md
  - 基于TDD-TOWER-001生成PDD-TOWER-001.md
  - 验证：TDD/PDD引用GDD-TOWER-001 ID

## 阶段4：代码同步

- [ ] Task 4.1：统一scripts/index.html中ID格式
  - 根据阶段0裁定结果，更新所有ID引用格式
  - 验证：Grep确认代码中ID格式与ID-REGISTRY一致

- [ ] Task 4.2：验证代码状态机与PDD一致
  - 对比scripts/index.html状态机实现与PDD-COMBAT-001修正后的状态机
  - 如有偏差，以PDD为准修正代码
  - 验证：代码状态机与PDD定义完全一致

- [ ] Task 4.3：更新代码中CSV引用
  - 确保代码中的EMBEDDED_CSV字段与修正后的CSV结构一致
  - 验证：所有CSV引用可正常解析

## 阶段5：自动化校验实现

- [ ] Task 5.1：创建scripts/validation/目录
  - 验证：目录存在且可写入

- [ ] Task 5.2：实现id-format-check.py
  - 校验所有CSV/GDD/TDD/PDD/代码中的ID格式
  - 正则：^[A-Z]+(-[0-9]+)+$
  - 验证：运行脚本，输出校验报告

- [ ] Task 5.3：实现id-registry-check.py
  - 校验所有ID在ID-REGISTRY中的注册状态
  - 验证：运行脚本，输出未注册ID清单

- [ ] Task 5.4：实现csv-schema-check.py
  - 校验所有CSV列名与_schema.csv定义一致
  - 验证：运行脚本，输出列名不一致清单

- [ ] Task 5.5：实现foreign-key-check.py
  - 读取_foreign_keys.csv，校验所有外键引用完整性
  - 验证：运行脚本，输出外键断链清单

- [ ] Task 5.6：实现deprecated-id-check.py
  - 校验全项目无废弃编号引用
  - 验证：运行脚本，输出废弃编号引用清单

- [ ] Task 5.7：实现tdd-pdd-coverage.py
  - 校验每个GDD有对应TDD，每个TDD有对应PDD
  - 验证：运行脚本，输出覆盖缺口清单

- [ ] Task 5.8：实现version-sync-check.py
  - 校验GDD/TDD/PDD frontmatter版本与变更日志一致
  - 验证：运行脚本，输出版本不同步清单

- [ ] Task 5.9：实现alias-graph-check.py
  - 校验ID-ALIAS.md和ID-REFERENCE-GRAPH.md完整性
  - 验证：运行脚本，输出缺失映射/前缀清单

- [ ] Task 5.10：配置Git pre-commit hook
  - 创建.git/hooks/pre-commit调用所有校验脚本
  - 任一失败阻止提交
  - 验证：尝试提交一个错误文件，确认被阻止

# Task Dependencies
- [Task 0.1] 无依赖，可立即执行
- [Task 0.2] 无依赖，可立即执行
- [Task 0.3] 无依赖，可立即执行
- [Task 0.4] 无依赖，可立即执行
- [阶段1全部] 依赖阶段0完成（ID格式裁定）
- [Task 1.1~1.6] 依赖Task 0.4
- [阶段2全部] 依赖阶段1完成（ID格式已统一，ID-REGISTRY已补全）
- [Task 2.1~2.11] 依赖Task 1.1和Task 1.2
- [阶段3全部] 依赖阶段1和阶段2完成（ID格式已统一，CSV数据已修复）
- [Task 3.1~3.5] 依赖Task 1.1
- [Task 3.6] 依赖Task 1.1
- [Task 3.7] 依赖Task 1.1
- [Task 3.8~3.11] 依赖Task 2.1~2.11
- [Task 3.12~3.16] 依赖Task 1.1, Task 1.2
- [阶段4全部] 依赖阶段1和阶段3完成
- [Task 4.1] 依赖Task 1.1, Task 3.6
- [Task 4.2] 依赖Task 3.8
- [Task 4.3] 依赖Task 2.1~2.11
- [阶段5全部] 依赖阶段1~4全部完成（数据已修复，可作为校验基线）
- [Task 5.2~5.9] 依赖阶段1~4完成
- [Task 5.10] 依赖Task 5.2~5.9全部完成