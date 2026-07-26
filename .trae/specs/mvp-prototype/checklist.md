# MVP原型 检查清单

## 阶段0：设计裁定

- [ ] Task 0.1：CE模型冲突已裁定，GDD-CORE-001 §5.2已同步，决策记录在.changelog.md
- [ ] Task 0.2：MVP预设角色属性已确认，已写入GDD-BATTLEFIELD-001 §10

## 阶段1：CSV数据补齐

### cards.csv验证
- [ ] C-010~C-014（战士5张）已录入，含card_id/name/type/rarity/ce_cost/profession/damage/shield/heal/description
- [ ] C-020~C-024（盗贼5张）已录入，同上字段完整
- [ ] C-030~C-034（法师5张）已录入，同上字段完整
- [ ] C-050~C-054（牧师5张）已录入，同上字段完整
- [ ] C-004/C-072/C-073（通用3张）已录入或确认存在
- [ ] C-076~C-079（团队4张）已录入，含每战/每回合使用限制
- [ ] C-001~C-009区间卡牌已标注❌已废弃
- [ ] CSV编码UTF-8，首行#注释，列名全小写下划线

### card_effects.csv验证
- [ ] 所有新增卡牌的效果数据已录入
- [ ] 状态施加字段（apply_status_id）正确引用S-001~S-008
- [ ] 多段攻击标记（multi_hit）正确
- [ ] 特殊效果标记（ignore_shield/consume_rage/consume_cp/mana_cost）正确

### professions.csv验证
- [ ] P-002（盗贼）：profession_id=PROF-002, energy_type=combo_point, energy_max=3
- [ ] P-003（法师）：profession_id=PROF-003, energy_type=mana, energy_max=7
- [ ] P-004（牧师）：profession_id=PROF-004, energy_type=mana, energy_max=6
- [ ] 字段与_schema.csv中professions.csv定义一致

### profession_starting_deck.csv验证
- [ ] P-002初始牌组已录入（C-020×2, C-021×1, C-004×1）
- [ ] P-003初始牌组已录入（C-030×1, C-031×1, C-004×1, C-070×1）
- [ ] P-004初始牌组已录入（C-050×1, C-051×1, C-004×1, C-072×1）

### status_effects.csv验证
- [ ] S-004（流血）：duration=3, decay=1/回合, stackable=true
- [ ] S-005（灼烧）：duration=3, decay=1/回合, stackable=true, vs_shield_multiplier=2.0
- [ ] S-006（减速）：duration=1, decay=无, stackable=false, effect=CE-1
- [ ] S-007（致盲）：duration=2, decay=无, stackable=false, effect=命中率-30%
- [ ] S-008（标记）：duration=until_triggered_or_3, decay=触发后移除, stackable=false, damage_multiplier=1.5

## 阶段2：ID注册验证

- [ ] ID-REGISTRY中C-010~C-014全部标记✅已注册，card_type=战士核心牌
- [ ] ID-REGISTRY中C-020~C-024全部标记✅已注册，card_type=盗贼核心牌
- [ ] ID-REGISTRY中C-030~C-034全部标记✅已注册，card_type=法师戏法
- [ ] ID-REGISTRY中C-050~C-054全部标记✅已注册，card_type=牧师核心牌
- [ ] ID-REGISTRY中C-070~C-073全部标记✅已注册，card_type=通用辅助
- [ ] ID-REGISTRY中C-076~C-079全部标记✅已注册，card_type=团队卡牌
- [ ] ID-REGISTRY中P-002/P-003/P-004已注册
- [ ] ID-REGISTRY中S-004~S-008已注册
- [ ] ID-REGISTRY统计表数字与实际清单一致
- [ ] Grep全项目确认无未注册编号引用

## 阶段3：TDD验证

- [ ] TDD-BATTLEFIELD-001-html.md已创建，≤300行
- [ ] TDD中所有ID引用在ID-REGISTRY中存在（Grep验证）
- [ ] TDD包含6模块清单（战场渲染/卡牌管理/回合控制/AI/伤害结算/手牌UI）
- [ ] TDD包含5数据结构定义（Grid/Card/Character/Enemy/StateEffect）
- [ ] TDD包含8核心接口定义（moveCharacter/playCard/processTurn/calculateDamage/applyStatus/checkWin/spawnEnemy/renderHand）
- [ ] TDD包含DOM结构（#battlefield-grid/#hand-area/#status-bar/#combat-log）
- [ ] TDD包含所有卡牌的EMBEDDED_CSV数据段

## 阶段4：PDD验证

- [ ] PDD-BATTLEFIELD-001.md已创建
- [ ] PDD中无function/var/let/const/{}关键字
- [ ] PDD函数清单格式：函数名(参数) → 一句话描述
- [ ] PDD状态机包含全部阶段转换（PRE_BATTLE→...→CHECK_WIN）
- [ ] PDD全局变量清单完整
- [ ] PDD事件清单完整
- [ ] PDD模块依赖图完整
- [ ] PDD与TDD接口定义一致（无遗漏/无越权新增）

## 阶段5：HTML原型验证

### 战场渲染
- [ ] 3×3我方网格正确绘制（列向排布·P1-P9标签）
- [ ] 3×3敌方网格正确绘制（列向排布·E1-E9标签）
- [ ] 4角色初始位置正确（战士P3·盗贼P6·法师P7·牧师P4，按预设阵型）
- [ ] 敌方初始位置正确（按所选阵型模板）
- [ ] 选中角色高亮显示

### 卡牌管理
- [ ] 手牌区单行水平排列
- [ ] 手牌超过10张时可横向滚动
- [ ] 战士专属牌红色边框+🔴标记
- [ ] 盗贼专属牌绿色边框+🟢标记
- [ ] 法师专属牌紫色边框+🟣标记
- [ ] 牧师专属牌黄色边框+🟡标记
- [ ] 共享通用牌白色边框+🌐标记
- [ ] 团队卡牌金色边框+⭐标记
- [ ] 非法职业卡牌灰度·不可点击
- [ ] 每回合抽牌正确（共享+2·每角色专属+1）

### 回合控制
- [ ] CE独立计算（战士5/盗贼4/法师3/牧师3）
- [ ] CE每回合恢复+2
- [ ] 出牌消耗对应角色CE
- [ ] 移动消耗1CE
- [ ] 换位0CE·全队1次/回合
- [ ] 主动结束回合按钮可用
- [ ] 未用CE显式略过（不累积到下回合）

### 敌方AI
- [ ] 杂兵AI：攻击最近目标·不移动
- [ ] 射手AI：优先后排·保持中后排
- [ ] 精英AI：攻击最低HP目标
- [ ] Boss AI：阶段切换（单体→AOE→狂暴）
- [ ] 施法者AI：法术循环（护盾→AOE→单体）
- [ ] 敌人意图正确显示（已揭示的显示·未揭示的隐藏）

### 伤害结算
- [ ] 基础伤害正确
- [ ] 护盾先扣·后扣HP
- [ ] DOT回合结束时触发
- [ ] 多段伤害每段独立计算
- [ ] AOE每个目标独立计算
- [ ] 最低伤害≥1

### 状态效果
- [ ] S-001护盾正确抵消伤害
- [ ] S-004流血每回合伤害=层数
- [ ] S-005灼烧每回合伤害=层数·对护盾×2
- [ ] S-008标记触发后伤害×1.5并移除
- [ ] 灼烧+流血互动正确（流血本回合×2）
- [ ] 护盾+灼烧互动正确（灼烧×2对盾）

### 职业能量
- [ ] 战士怒气获取（受伤+1/命中+1）
- [ ] 战士怒气衰减（1-4安全·5-9减1·10减2）
- [ ] 盗贼CP获取（基础攻击命中+1）
- [ ] 盗贼CP衰减（受伤-1·下限0）
- [ ] 法师/牧师法力值每日恢复

### 胜负判定
- [ ] 全部敌人HP≤0 → 胜利
- [ ] 全部角色HP≤0 → 失败
- [ ] 战斗日志记录完整

## 系统集成
- [ ] CSV数据通过EMBEDDED_CSV正确加载
- [ ] ID-REGISTRY与CSV的card_id一致
- [ ] HTML单文件可独立运行（浏览器直接打开）
- [ ] 无console报错
- [ ] 页面响应正常（60fps+）
