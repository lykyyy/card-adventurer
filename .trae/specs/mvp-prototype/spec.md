# 卡牌冒险者 MVP 原型 Spec

## Why
基于2026-07-12 GDD完备性评估，设计文档覆盖面约80%（BATTLEFIELD-001尤为完备），但数据层覆盖率仅15%，且存在两份核心GDD的CE模型冲突。本规范定义MVP最小范围，裁定阻塞性设计冲突，补齐CSV数据缺漏，为HTML原型开发铺路。

## What Changes
- **阶段0（设计裁定）**：裁定CE模型冲突（GDD-CORE-001 vs GDD-BATTLEFIELD-001）、确认MVP角色预设属性
- **阶段1（CSV数据补齐）**：补全cards.csv(+24张职业牌·4张团队牌)、professions.csv(+3职业)、status_effects.csv(+5状态)、profession_starting_deck.csv(+3职业)
- **阶段2（ID注册）**：ID-REGISTRY补注册C-010~C-079区间全部活跃卡牌
- **阶段3（TDD编制）**：编制GDD-BATTLEFIELD-001对应的HTML TDD技术文档 **BREAKING**
- **阶段4（PDD编制）**：基于TDD编制PDD实现文档 **BREAKING**
- **阶段5（HTML原型实现）**：基于TDD/PDD实现可玩的3×3地面战斗HTML原型 **BREAKING**

## Impact
- Affected specs: system-fix-20260712（部分P0修正与MVP重叠，需协调优先级）
- Affected docs: GDD-CORE-001（CE裁定同步）、GDD-BATTLEFIELD-001（版本更新）
- Affected data: cards.csv、card_effects.csv、professions.csv、profession_starting_deck.csv、status_effects.csv、ID-REGISTRY.md

## MVP范围定义

### IN scope（第一阶段可玩原型）
- 地面3×3网格战斗（单场遭遇战）
- 4职业预设角色（战士/盗贼/法师/牧师固定属性，无需角色创建流程）
- 职业核心牌+通用牌+团队牌（~30张）
- 5种敌人（E-001~E-005）+ 敌方AI
- 8种状态效果 + 互动规则
- 独立CE系统（每角色独立）+ 职业能量（怒气/CP/法力值）
- 伤害公式（7步结算）
- 回合流程（开始→行动→敌方→结束）
- 三层手牌系统（共享+专属+团队）
- 空手战斗（装备系统延后至MVP v2）

### OUT scope（延后）
- 装备系统（12槽位+词缀+耐久）
- 太空船战斗
- 角色创建流程（种族/出身/属性分配）
- 制作/附魔/法师塔/消耗品
- L1地图/L2网格/L3难度匹配
- 等级成长/传奇道途
- 卡牌升级/专长重修/装备重铸

---

## ADDED Requirements

### Requirement: 阶段0A — CE模型裁定
系统 SHALL 统一CE模型的初始值、上限和恢复机制，消除GDD-CORE-001（重置制）与GDD-BATTLEFIELD-001（恢复制）的冲突。

#### Scenario: CE模型选型
- **WHEN** 用户裁定CE模型
- **THEN** 选定GDD-BATTLEFIELD-001的独立CE模型（每角色独立·职业差异化·恢复制）
- **AND** GDD-CORE-001 §5.2 CE描述同步更新
- **AND** 决策记录到.changelog.md（DEC-20260712-05）

### Requirement: 阶段0B — MVP角色预设属性
系统 SHALL 为MVP阶段定义4个预设角色的完整属性表，跳过角色创建流程。

#### Scenario: 预设角色
- **WHEN** MVP原型启动
- **THEN** 直接加载以下4个预设角色：

| 职业 | 名称 | HP | CE上限 | 职业能量 | STR | DEX | CON | INT | WIS | CHA |
|------|------|-----|--------|----------|-----|-----|-----|-----|-----|-----|
| 战士(P-001) | 预设战士 | 120 | 5 | 怒气0/10 | 16 | 12 | 14 | 10 | 10 | 12 |
| 盗贼(P-002) | 预设盗贼 | 90 | 4 | CP 0/3 | 10 | 18 | 10 | 12 | 10 | 14 |
| 法师(P-003) | 预设法师 | 70 | 3 | 法力7/7 | 8 | 12 | 10 | 18 | 10 | 10 |
| 牧师(P-004) | 预设牧师 | 80 | 3 | 法力6/6 | 10 | 10 | 10 | 10 | 16 | 14 |

### Requirement: 阶段1A — CSV职业卡牌补齐
系统 SHALL 将以下已设计的卡牌录入cards.csv和card_effects.csv：

- 战士核心牌：C-010~C-014（5张）
- 盗贼核心牌：C-020~C-024（5张）
- 法师戏法：C-030~C-034（5张）
- 牧师核心牌：C-050~C-054（5张）
- 通用辅助：C-004急救、C-072战备、C-073专注（3张·若已存在则跳过）
- 团队卡牌：C-076~C-079（4张）

#### Scenario: 卡牌CSV结构
- **WHEN** 卡牌录入CSV
- **THEN** 每张卡牌包含：card_id、card_name、CE cost、职业限制、效果描述、伤害/护盾/治疗数值

### Requirement: 阶段1B — CSV职业和状态补齐
系统 SHALL 补全professions.csv（P-002盗贼/P-003法师/P-004牧师）、profession_starting_deck.csv（3职业初始牌组）、status_effects.csv（S-004~S-008）。

### Requirement: 阶段2 — ID注册补全
系统 SHALL 在ID-REGISTRY中补注册C-010~C-079区间所有活跃卡牌（~30张），全部标记✅已注册。

### Requirement: 阶段3 — HTML TDD编制
系统 SHALL 为3×3地面战斗编制HTML版TDD技术文档，定义：
- 模块清单（战场渲染/卡牌管理/回合控制/AI/伤害结算/手牌UI）
- 数据结构（Grid、Card、Character、Enemy、StateEffect）
- 接口定义（moveCharacter、playCard、processTurn、calculateDamage等）
- DOM结构（棋盘容器/手牌区/状态栏）
- EMBEDDED_CSV数据段

### Requirement: 阶段4 — PDD编制
系统 SHALL 基于TDD编制PDD实现文档，遵循最优解耦原则：
- 模块清单（函数名+一句话描述）
- 全局变量（不包含函数体）
- 状态机（战斗阶段状态转换）
- 事件清单
- 模块依赖关系

### Requirement: 阶段5 — HTML原型实现
系统 SHALL 基于TDD+PDD实现单个HTML文件原型，包含：
- 3×3网格战场（我方左·敌方右·列向排布）
- 4角色队伍（预设属性+职业牌库）
- 5种敌人+AI
- 回合流程（开始→行动→敌方→结束）
- 三层手牌系统（单行水平排列·可横向滚动·6色区分）
- 伤害公式（7步结算）
- 8状态效果+互动
- 移动/换位操作
- 战斗日志

---

## MODIFIED Requirements

### Requirement: GDD-CORE-001 §5.2 CE定义
**原内容**：CE初始值3·上限6·每回合重置至当前上限
**修改为**：CE由职业基础+CON调整值+身份+装备决定·每回合恢复+2·独立CE池（引用GDD-BATTLEFIELD-001 §1.2）

### Requirement: GDD-COMBAT-001 状态
**原状态**：draft
**修改为**：标记为[已过时·参照GDD-BATTLEFIELD-001]，在文档头部添加废弃通知
