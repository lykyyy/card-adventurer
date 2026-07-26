---
id: TDD-BATTLEFIELD-001-html
title: 双战场战斗系统HTML版技术设计
type: TDD
source: GDD-BATTLEFIELD-001
version: 0.1.0
status: draft
created: 2026-07-12
related:
  - "[[GDD-BATTLEFIELD-001]]"
  - "[[GDD-CORE-001]]"
tags: [TDD, html, battlefield, combat, prototype]
---

# TDD-BATTLEFIELD-001-html · 双战场战斗系统HTML版技术设计

> 来源：[[GDD-BATTLEFIELD-001]]（双战场·地面战）、[[GDD-CORE-001]]（CE/职业能量/状态/装备体系）。
> 太空船战不在MVP范围内，标记为阶段2。

## 1. 模块清单（6模块）

| 模块ID | 模块名 | 职责 | 来源GDD |
|--------|--------|------|---------|
| MOD-RENDER | 战场渲染 | DOM构建·网格绘制·角色/敌人位置更新 | GDD-BATTLEFIELD-001 §2 |
| MOD-CARD | 卡牌管理 | 牌库维护·抽牌·三层归属判定·CE校验 | GDD-BATTLEFIELD-001 §6 |
| MOD-TURN | 回合控制 | 阶段流转·CE恢复·状态结算·胜负检查 | GDD-BATTLEFIELD-001 §5 |
| MOD-AI | 敌方AI | 行为决策树·目标选择·技能使用·意图展示 | GDD-BATTLEFIELD-001 §7 |
| MOD-DAMAGE | 伤害结算 | 伤害公式·护盾扣除·DOT触发·状态倍率 | GDD-BATTLEFIELD-001 §8 |
| MOD-HAND | 手牌UI | 手牌渲染·6色区分·CE高亮/灰度 | GDD-BATTLEFIELD-001 §6.2 |

## 2. 数据结构

### GridPosition
```
{ row: 0|1|2, col: 0|1|2 }
row: 0=后排, 1=中排, 2=前排
col: 0=上行, 1=中行, 2=下行
```

### Card
```
{ id, name, type, owner, ceCost, damage, shield, heal, aoe, ignoreShield, statusApply, manaCost, specialRules, limitedUse }
```

### Character
```
{ id, name, hp, maxHp, ce, ceMax, ceRecovery, position, professionEnergy{type,current,max}, statusEffects[], deck[], hand[], isAlive }
```

### Enemy
```
{ id, name, type, hp, maxHp, damage, position, intent, skills[], statusEffects[], isAlive }
```

### StatusEffect
```
{ id, name, stacks, duration, effect{type, value, ignoreShield, shieldMultiplier} }
```

## 3. 核心接口

- renderBattlefield() → 渲染6×3网格+角色/敌人+HP条
- renderHand() → 渲染手牌区·单行水平·6色区分
- playCard(card, caster, target) → 执行出牌·扣CE·计算伤害·更新状态
- moveCharacter(char, to) → 移动角色·校验合法·扣CE
- calculateDamage(card, caster, target) → 伤害公式7步结算
- applyStatus(target, statusId, stacks) → 施加状态效果
- executeEnemyAI() → 敌方按决策树行动
- processTurn(phase) → 阶段流转
- checkWin() → 胜负判定

## 4. DOM结构

- #status-bar: 回合数+阶段+CE概览
- #combat-log: 战斗日志(可折叠)
- #battlefield-grid: 我方3列 #player-zone + 敌方3列 #enemy-zone
- #hand-area: 单行水平flexbox·overflow-x:auto
- #action-bar: 结束回合+撤销按钮

## 5. EMBEDDED_CSV

卡牌/敌人/状态效果数据嵌入式定义（见实现文件）。

## 6. 技术约束

- 单文件HTML·零外部依赖·纯原生JS
- 网格固定6列×3行
- 手牌单行水平·可横向滚动
- CE最低0·伤害最低1·单目标状态≤4种
- 卡牌修正上限≤50%

## 7. MVP预设角色

| 角色 | 职业 | HP | CE | 能量 | 初始位置 | 初始手牌 |
|------|------|-----|-----|------|----------|----------|
| 战士 | P-001 | 120 | 5 | 怒0/10 | P3(前排) | C-010×2,C-011×1,C-004×1 |
| 盗贼 | P-003 | 90 | 4 | CP0/3 | P6(前排) | C-020×2,C-021×1,C-004×1 |
| 法师 | P-002 | 70 | 3 | 法7/7 | P7(后排) | C-030×1,C-031×1,C-004×1,C-072×1 |
| 牧师 | P-004 | 80 | 3 | 法6/6 | P4(中排) | C-050×1,C-051×1,C-004×1,C-072×1 |

## 变更日志
- 2026-07-12 v0.1.0 初始创建 MVP地面3×3战斗HTML版TDD
