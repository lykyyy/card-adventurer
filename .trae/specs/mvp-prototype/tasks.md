# MVP原型 任务清单

## 阶段0：设计裁定（阻塞项，必须先完成）

- [ ] Task 0.1：裁定CE模型冲突
  - 向用户展示GDD-CORE-001（重置制·统一CE=3）与GDD-BATTLEFIELD-001（恢复制·职业差异化）的冲突
  - 用户选择GDD-BATTLEFIELD-001模型（推荐）
  - 记录决策到.changelog.md（DEC-20260712-05）
  - 同步更新GDD-CORE-001 §5.2

- [ ] Task 0.2：确认MVP预设角色属性表
  - 向用户展示4职业预设属性（战士/盗贼/法师/牧师）
  - 用户确认或调整数值
  - 记录决策到.changelog.md（DEC-20260712-06）
  - 写入GDD-BATTLEFIELD-001 §10 "MVP预设角色"

## 阶段1：CSV数据补齐

- [ ] Task 1.1：补全cards.csv
  - 录入24张职业卡牌（C-010~C-014·C-020~C-024·C-030~C-034·C-050~C-054）+ 4张团队卡牌（C-076~C-079）+ 通用卡牌（C-004/C-072/C-073）
  - 每张卡牌含：card_id, card_name, card_type, rarity, ce_cost, profession_restriction（职业限制）, damage, shield, heal, aoe（是否AOE）, description
  - 标注C-001~C-009为❌已废弃

- [ ] Task 1.2：补全card_effects.csv
  - 为Task 1.1中所有卡牌录入效果数据
  - 包含：状态施加（S-001~S-008）、多段攻击标记、特殊效果标记（无视护盾/怒气消费/CP消费等）

- [ ] Task 1.3：补全professions.csv
  - 添加P-002（盗贼）、P-003（法师）、P-004（牧师）
  - 字段：profession_id, name_zh, primary_attr, secondary_attr, hp_base, ce_base, energy_type, energy_max, energy_decay

- [ ] Task 1.4：补全profession_starting_deck.csv
  - 添加P-002/P-003/P-004的初始牌组
  - P-002：C-020×2, C-021×1, C-004×1
  - P-003：C-030×1, C-031×1, C-004×1, C-070×1
  - P-004：C-050×1, C-051×1, C-004×1, C-072×1

- [ ] Task 1.5：补全status_effects.csv
  - 添加S-004（流血）、S-005（灼烧）、S-006（减速）、S-007（致盲）、S-008（标记）
  - 字段：status_id, name_zh, duration, decay, stackable, interaction（互动规则）, description

- [ ] Task 1.6：更新equipment_slots.csv
  - 标注为[待MVP v2更新·当前版本不启用装备系统]

## 阶段2：ID注册补全

- [ ] Task 2.1：补注册C-010~C-079区间卡牌
  - 逐个登记C-010~C-014（战士5）、C-020~C-024（盗贼5）、C-030~C-034（法师戏法5）、C-035~C-049（法师法术·当前仅注册预留）
  - 逐个登记C-050~C-054（牧师5）、C-070~C-073（通用3）、C-076~C-079（团队4）
  - 全部标记✅已注册·来源GDD-CORE-001
  - 更新ID-REGISTRY统计表

- [ ] Task 2.2：补注册P-002/P-003/P-004
  - 盗贼(P-002)、法师(P-003)、牧师(P-004)标记✅已注册

- [ ] Task 2.3：补注册S-004~S-008
  - 流血(S-004)、灼烧(S-005)、减速(S-006)、致盲(S-007)、标记(S-008)标记✅已注册

## 阶段3：HTML TDD编制

- [ ] Task 3.1：编制TDD-BATTLEFIELD-001-html.md
  - 基于GDD-BATTLEFIELD-001编制HTML版TDD
  - 包含：模块清单（6模块）、数据结构（Grid/Card/Character/Enemy/StateEffect）、接口定义（8核心函数）、DOM结构、EMBEDDED_CSV
  - ≤300行

- [ ] Task 3.2：TDD技术评审
  - 验证所有引用ID在ID-REGISTRY中存在
  - 验证接口定义覆盖GDD中所有战斗功能
  - 验证数据结构字段完整

## 阶段4：PDD编制

- [ ] Task 4.1：编制PDD-BATTLEFIELD-001.md
  - 基于TDD-BATTLEFIELD-001编制PDD
  - 包含：模块清单+函数清单（仅签名+描述，不含函数体）
  - 状态机（PRE_BATTLE→PRE_TURN→PLAYER_ACTION→ENEMY_ACTION→END_TURN→CHECK_WIN）
  - 全局变量、事件清单、模块依赖

- [ ] Task 4.2：PDD格式校验
  - 确认无function/var/let/const/{}关键字
  - 确认所有函数仅保留签名+描述
  - 确认模块依赖图完整

## 阶段5：HTML原型实现

- [ ] Task 5.1：实现战场渲染模块
  - 3×3网格绘制（我方左·敌方右·列向排布）
  - 角色/敌人位置渲染
  - 选中高亮

- [ ] Task 5.2：实现卡牌管理模块
  - 三层手牌系统（共享+专属+团队）
  - 单行水平排列·横向滚动·6色边框区分
  - 卡牌可用性校验（职业限制/CE不足灰度）

- [ ] Task 5.3：实现回合控制系统
  - 独立CE池（每角色独立·每回合恢复+2）
  - 行动阶段（自由顺序·出牌/移动/换位/主动结束）
  - 回合结束阶段（状态结算·死亡判定·胜负检查）

- [ ] Task 5.4：实现敌方AI系统
  - 5种敌人类型AI行为
  - 敌人意图展示
  - 敌人行动执行

- [ ] Task 5.5：实现伤害结算系统
  - 7步伤害结算公式
  - 5种特殊伤害类型（无视护盾/DOT/多段/AOE/反伤）
  - 状态效果结算（8状态+互动规则）
  - 战斗日志

- [ ] Task 5.6：实现职业能量系统
  - 战士怒气（获取/衰减/消费）
  - 盗贼连击点（获取/衰减/消费）
  - 法师/牧师法力值（消费/每日恢复）

- [ ] Task 5.7：MVP集成测试
  - 单场遭遇战完整流程测试
  - 4职业各角色卡牌打出验证
  - 敌方AI行为验证
  - 状态效果互动验证
  - 边界情况（HP归零/CE耗尽/手牌溢出）

# 任务依赖

- Task 1.1~1.6 依赖 Task 0.1~0.2（设计裁定完成后才能确定CSV字段）
- Task 2.1~2.3 依赖 Task 1.1~1.5（CSV数据确定后注册ID）
- Task 3.1 可并行于 Task 1.1~2.3（TDD基于GDD编制，不依赖CSV）
- Task 4.1 依赖 Task 3.2（TDD通过后编制PDD）
- Task 5.1~5.7 依赖 Task 4.2（PDD通过后实现HTML）
