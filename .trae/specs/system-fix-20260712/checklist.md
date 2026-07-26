# 系统修正实施检查清单

## 阶段0：用户决策裁定

- [x] Task 0.1：MAT-003/MAT-004名称冲突已裁定，决策记录在.changelog.md
- [x] Task 0.2：P-002/P-003/P-004职业归属已裁定，已注册到ID-REGISTRY
- [x] Task 0.3：禁止清单与职业规划矛盾已裁定，矛盾GDD已标记待同步
- [x] Task 0.4：ID格式权威标准已裁定（C-001）

## 阶段1：ID体系修复

### ID-REGISTRY验证
- [x] ID-REGISTRY中所有ID格式统一（无混合格式）
- [x] ID-REGISTRY中约92个未注册ID已补注册，状态为✅已注册
- [x] ID-REGISTRY统计表数据与实际清单一致

### CSV ID验证
- [x] cards.csv中无C001-C007等废弃编号
- [x] cards.csv中所有卡牌ID在ID-REGISTRY中已注册
- [x] 所有CSV文件中无废弃编号引用（Grep确认）

### ID-ALIAS验证
- [x] ID-ALIAS.md包含所有废弃编号的别名映射（≥8条）
- [x] 每条映射格式：旧编号→新编号（替代编号）+ 废弃原因

### ID-REFERENCE-GRAPH验证
- [x] ID-REFERENCE-GRAPH.md包含所有已注册前缀（≥15个）
- [x] 每个前缀有跨系统引用位置记录

## 阶段2：CSV数据修复

### 结构修复验证
- [ ] equipment_slots.csv列名为slot_id/name_zh/slot_type
- [ ] professions.csv使用profession_id（非prof_id）
- [ ] profession_starting_deck.csv使用profession_id（非prof_id）
- [ ] _foreign_keys.csv中profession外键列名一致

### 列结构一致性验证
- [ ] card_effects.csv列名与_schema.csv一致
- [ ] enemy_skills.csv列名与_schema.csv一致
- [ ] professions.csv列名与_schema.csv一致
- [ ] profession_starting_deck.csv列名与_schema.csv一致
- [ ] status_effects.csv列名与_schema.csv一致
- [ ] skill_texts.csv列名与_schema.csv一致
- [ ] cards.csv列数与_schema.csv定义一致
- [ ] enemies.csv列数与_schema.csv定义一致
- [ ] enemy_skills.csv列数与_schema.csv定义一致
- [ ] professions.csv列数与_schema.csv定义一致
- [ ] races.csv列数与_schema.csv定义一致
- [ ] skills.csv列数与_schema.csv定义一致
- [ ] leveling.csv列数与_schema.csv定义一致

### 本地化文件验证
- [ ] element_names.csv以#注释行开头
- [ ] element_names.csv列名为小写下划线格式
- [ ] skill_texts.csv以#注释行开头
- [ ] skill_texts.csv列名为小写下划线格式

### 数据值验证
- [ ] 所有CSV数值在定义范围内
- [ ] 所有CSV枚举值在允许值集合内
- [ ] 所有外键引用目标存在

### 版本号验证
- [ ] _schema.csv中所有修改过的CSV版本号已+0.0.1
- [ ] _foreign_keys.csv版本号已更新

## 阶段3：GDD/TDD/PDD文档修复

### 版本号同步验证
- [ ] GDD-CORE-001 frontmatter版本=变更日志最新版本
- [ ] GDD-CHARACTER-001 frontmatter版本=变更日志最新版本
- [ ] GDD-COMBAT-001 frontmatter版本=变更日志最新版本
- [ ] GDD-CRAFTING-001 frontmatter版本=变更日志最新版本
- [ ] TDDH-COMBAT-001 version≥GDD-COMBAT-001版本
- [ ] _schema.csv中cards.csv版本与GDD-COMBAT-001一致

### 内部链接验证
- [ ] 所有GDD中跨文件ID引用使用[[ID-REGISTRY|...]]格式
- [ ] 无裸ID引用（排除同文件内和数值表）

### TDD命名验证
- [ ] 所有TDD文件命名符合TDD-{系统}-{序号}-html/godot.md格式
- [ ] 所有引用TDD的文档已更新

### PDD内容验证
- [ ] PDD-COMBAT-001状态机与scripts/index.html代码一致
- [ ] PDD-COMBAT-001中无loadCSV函数引用
- [ ] TDDH-COMBAT-001中无loadCSV函数引用
- [ ] PDD-COMBAT-001 §3函数清单包含executeEffect
- [ ] PDD-COMBAT-001中无builEnemySkillMap拼写错误
- [ ] PDD-COMBAT-001中数组数量描述一致（8个CSV）

### TDD/PDD覆盖验证
- [ ] GDD-CORE-001有对应TDD和PDD
- [ ] GDD-BATTLEFIELD-001有对应TDD和PDD
- [ ] GDD-CHARACTER-001有对应TDD和PDD
- [ ] GDD-CRAFTING-001有对应TDD和PDD
- [ ] GDD-TOWER-001有对应TDD和PDD
- [ ] 所有新增TDD/PDD中ID引用在ID-REGISTRY中已注册

## 阶段4：代码同步

### ID格式验证
- [ ] scripts/index.html中所有ID格式与ID-REGISTRY一致
- [ ] scripts/index.html中无废弃编号引用

### 状态机验证
- [ ] scripts/index.html状态机实现与PDD-COMBAT-001定义一致
- [ ] 状态转换逻辑正确

### CSV引用验证
- [ ] scripts/index.html中EMBEDDED_CSV字段与CSV文件结构一致
- [ ] 所有CSV数据可正常解析

## 阶段5：自动化校验实现

### 脚本存在性验证
- [ ] scripts/validation/目录存在
- [ ] scripts/validation/id-format-check.py存在且可执行
- [ ] scripts/validation/id-registry-check.py存在且可执行
- [ ] scripts/validation/csv-schema-check.py存在且可执行
- [ ] scripts/validation/foreign-key-check.py存在且可执行
- [ ] scripts/validation/deprecated-id-check.py存在且可执行
- [ ] scripts/validation/tdd-pdd-coverage.py存在且可执行
- [ ] scripts/validation/version-sync-check.py存在且可执行
- [ ] scripts/validation/alias-graph-check.py存在且可执行

### 脚本功能验证
- [ ] id-format-check.py运行后输出正确校验报告
- [ ] id-registry-check.py运行后输出未注册ID清单
- [ ] csv-schema-check.py运行后输出列名不一致清单
- [ ] foreign-key-check.py运行后输出外键断链清单
- [ ] deprecated-id-check.py运行后输出废弃编号引用清单
- [ ] tdd-pdd-coverage.py运行后输出覆盖缺口清单
- [ ] version-sync-check.py运行后输出版本不同步清单
- [ ] alias-graph-check.py运行后输出缺失映射/前缀清单

### Git Hook验证
- [ ] .git/hooks/pre-commit存在且可执行
- [ ] 提交前自动执行所有校验脚本
- [ ] 任一脚本失败阻止提交
- [ ] 校验报告格式符合automation-validation.md定义

### 全量验收
- [ ] 所有8个脚本对当前项目运行结果为✅全部通过
- [ ] 无残留问题
- [ ] .changelog.md记录完整修正过程