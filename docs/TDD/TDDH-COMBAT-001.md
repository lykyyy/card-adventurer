---
id: TDDH-COMBAT-001
title: 战斗系统技术设计（HTML原型）
type: TDD-HTML
system: combat
version: 0.4.0
status: draft
source_gdd: "[[GDD-BATTLEFIELD-001]]（原 [[GDD-COMBAT-001]]·已废弃）"
related_pdd: "[[PDD-COMBAT-001]]"
created: 2026-06-29
updated: 2026-07-15
author: tech-lead
reviewer: human
---

> **⚠️ 源GDD文档变更（2026-07-15）**
> 本文档原关联的 [[GDD-COMBAT-001]] 已被裁定废弃（旧版单角色通用卡牌战斗模型），
> 当前战斗系统权威设计文档为 [[GDD-BATTLEFIELD-001]]（双战场战斗系统·多角色队伍架构）。
> 
> 本 TDD 基于旧版架构（单角色·通用CE池·3类卡牌），如后续需要 Godot 实现，
> 请基于 GDD-BATTLEFIELD-001 重新生成 TDD。

# 战斗系统技术设计（HTML原型）

## 1. 技术方案
- 单文件HTML（内联CSS+JavaScript）
- 无外部依赖，浏览器直接打开运行
- Vanilla JS，不用框架
- **数据驱动架构**：所有游戏数据来自 `data/csv/` 目录，页面启动时异步加载
- CSV 首行 `#` 开头的注释行描述各字段含义，解析器自动跳过

## 2. CSV 数据架构

### 2.1 设计原则
- **元数据与效果分离**：卡牌身份信息（名称/类型/费用）与效果配置分属不同表，一卡可有多行效果
- **列名全小写**：所有 CSV 列名统一小写下划线格式（如 `card_id`, `effect_type`）
- **注释自文档化**：每个 CSV 首行以 `#` 开头，描述所有字段含义和可选值
- **数量用 count 字段**：初始牌组等配置用 `count` 列替代变长行，结构规整

### 2.2 配置举例：新增一张卡牌

**Step 1** — 在 `cards.csv` 添加一行：
```
C007,火球,Fireball,skill,2,uncommon,
```

**Step 2** — 在 `card_effects.csv` 添加效果行：
```
C007,damage,20,enemy,on_play,0
C007,shield,3,self,on_play,0
```

刷新页面后自动生效：一张 2 费 uncommon「火球」卡牌，打出时造成 20 点伤害 + 获得 3 点护盾。

### 2.3 效果类型速查表

| effect_type | 含义 | target 选项 | timing 选项 | 示例 |
|-------------|------|------------|------------|------|
| `damage` | 造成伤害 | `enemy` | `on_play` | 攻击牌 |
| `shield` | 获得护盾 | `self` | `on_play` | 防御牌 |
| `heal` | 恢复生命 | `self` | `on_play` | 治疗牌 |
| `shield_per_turn` | 每回合获得护盾 | `self` | `turn_start` | 护甲装备 |
| `damage_bonus` | 攻击伤害加成 | `self` | `on_play`(-1) | 武器装备 |

> 新增效果类型只需在 `effectDescMap`（index.html）中注册描述生成函数，无需改 switch-case。

## 3. CSV 文件规范

### 3.1 cards.csv — 卡牌元数据

| 列名 | 类型 | 说明 |
|------|------|------|
| `card_id` | string | 唯一编号，格式 `C-XXX`，必须在 ID-REGISTRY 注册 |
| `name_zh` | string | 中文名 |
| `name_en` | string | 英文名 |
| `type` | enum | `basic`(基本) / `skill`(技能) / `equip`(装备) / `status`(状态) |
| `cost` | int | 法力消耗 |
| `rarity` | enum | `common` / `uncommon` / `rare` / `epic` |
| `tags` | string | 逗号分隔标签，用于筛选（如 `装备,火焰`） |

### 3.2 card_effects.csv — 卡牌效果（★核心）

一卡多行 = 一卡多效果。完全解耦，无需修改代码即可赋予任意效果组合。

| 列名 | 类型 | 说明 |
|------|------|------|
| `card_id` | string | 关联 cards.csv 的 card_id |
| `effect_type` | enum | 效果类型（见 §2.3 速查表） |
| `value` | int | 效果数值 |
| `target` | enum | `self` / `enemy` / `all_enemies` |
| `timing` | enum | `on_play`(打出时) / `turn_start`(回合开始) / `turn_end`(回合结束) / `on_hit`(受击时) / `on_kill`(击杀时) |
| `duration` | int | 持续回合数（0=瞬时，-1=永久） |

### 3.3 enemies.csv — 敌人基础属性

| 列名 | 类型 | 说明 |
|------|------|------|
| `enemy_id` | string | 唯一编号，格式 `E-XXX` |
| `name_zh` | string | 中文名 |
| `name_en` | string | 英文名 |
| `hp` | int | 生命值（Boss 以此为准；普通敌人动态计算：50+20×(场次-1)） |
| `atk` | int | 基础攻击力 |

### 3.4 enemy_skills.csv — 敌人技能

| 列名 | 类型 | 说明 |
|------|------|------|
| `enemy_id` | string | 关联 enemies.csv |
| `name_zh` | string | 技能中文名 |
| `name_en` | string | 技能英文名 |
| `probability` | float | 概率权重（同敌人所有技能权重和归一化） |
| `damage` | int | 伤害值（0=无伤害） |
| `heal` | int | 治疗值（0=无治疗） |
| `shield` | int | 护盾值（0=无护盾） |
| `buff` | enum | 特殊增益：`berserk`(伤害=ATK×2) / `flee`(跳过) / 空 |
| `desc_zh` | string | 中文描述（仅用于阅读，不影响逻辑） |

### 3.5 professions.csv — 职业

| 列名 | 类型 | 说明 |
|------|------|------|
| `prof_id` | string | 唯一编号，格式 `P-XXX` |
| `name_zh` | string | 中文名 |
| `name_en` | string | 英文名 |
| `hp` | int | 生命值 |
| `mana` | int | 法力上限 |

### 3.6 profession_starting_deck.csv — 职业初始牌组

| 列名 | 类型 | 说明 |
|------|------|------|
| `prof_id` | string | 关联 professions.csv |
| `card_id` | string | 关联 cards.csv |
| `count` | int | 该卡牌数量 |

### 3.7 status_effects.csv — 状态效果

| 列名 | 类型 | 说明 |
|------|------|------|
| `status_id` | string | 唯一编号，格式 `S-XXX` |
| `name_zh` | string | 中文名 |
| `name_en` | string | 英文名 |
| `effect_desc_zh` | string | 中文效果描述 |
| `effect_desc_en` | string | 英文效果描述 |
| `duration_type` | enum | `current_turn` / `in_turns` / `permanent` |
| `duration_value` | int | 持续数值 |

### 3.8 equipment_slots.csv — 装备栏规则

| 列名 | 类型 | 说明 |
|------|------|------|
| `key` | string | 规则键 |
| `value_zh` | string | 中文说明 |
| `value_en` | string | 英文说明 |

## 4. 运行时数据结构

### 卡牌对象（由 CSV 构建）
```
{
  id: "C001", name: "攻击", type: "basic", cost: 0,
  rarity: "common", tags: "",
  effects: [
    { type: "damage", value: 10, target: "enemy", timing: "on_play", duration: 0 }
  ],
  // 兼容属性（从首个 effect 推导）
  effectType: "damage", damage: 10, description: "造成10点伤害"
}
```

### 玩家对象
```
{ id:"P001", name:"战士", hp:200, maxHp:200, mana:1, maxMana:1,
  shield:0, deck:[], hand:[], discard:[], equipment:{slot:null}, collection:[] }
```

### 敌人对象
```
{ id:"E001", name:"史莱姆", hp:50, maxHp:50, attack:8, shield:0,
  intents:[{name:"普通攻击",weight:0.6,damage:8}, ...] }
```

## 5. 模块划分
1. **csv-loader** — CSV 解析、数据加载、运行时对象构建
2. **game.js** — 游戏主循环、状态机、全局状态管理
3. **card.js** — 卡牌数据定义、效果执行、牌组管理
4. **enemy.js** — 敌人AI决策、技能执行
5. **ui.js** — 界面渲染、DOM操作
6. **battle.js** — 战斗结算、胜负判定、奖励系统

## 6. 界面布局
- 顶部：敌方信息（名称、血量条、意图提示）
- 中间：战斗区域（技能提示、伤害数字）
- 底部：玩家信息（血量条、法力、护盾）+ 手牌区域
- 右下角：结束回合按钮

## 7. 核心接口定义

### 7.1 CSV 加载层
- `parseCSV(csvText)` → array — 解析 CSV 文本，跳过 `#` 注释行
- `loadCSV(filename)` → Promise(array) — 异步 fetch CSV 并解析
- `buildCardDefinitions()` → void — 从 cards.csv + card_effects.csv 构建
- `buildEnemySkillMap()` → object — 从 enemy_skills.csv 构建
- `buildEnemyData(skillMap)` → object — 从 enemies.csv 构建
- `buildPlayerFromCSV()` → void — 从 professions.csv + profession_starting_deck.csv 构建
- `loadAllGameData()` → Promise(void) — 主加载入口

### 7.2 卡牌系统
- `initializeDeck()` → void
- `playCard(cardId)` → void
- `drawCard(count)` → void
- `discardHand()` → void
- `shuffleDiscardToDeck()` → void
- `equipCard(cardId)` → void
- `unequipCard()` → void
- `addToCollection(card)` → void

## 8. 状态机
| 当前状态 | 实际变量 | 转换条件 | 目标状态 |
|----------|----------|----------|----------|
| 战斗开始 | "battle_start" | 页面加载 → loadAllGameData() 异步加载 CSV → 启动战斗 | "player_turn" |
| 玩家回合 | "player_turn" | 点击结束回合 | "enemy_turn" |
| 玩家回合 | "player_turn" | 打出装备牌 | "player_turn" |
| 敌人回合 | "enemy_turn" | AI执行完毕 | "player_turn" |
| 玩家回合 | "player_turn" | 敌人HP≤0 | "victory" |
| 敌人回合 | "enemy_turn" | 玩家HP≤0 | "defeat" |

## 变更日志
- 2026-06-29 v0.1.0 初始创建
- 2026-06-29 v0.2.0 新增装备栏数据结构、牌组流转接口
- 2026-06-29 v0.2.1 修正 checkBattleEnd 返回类型
- 2026-07-06 v0.3.0 **CSV 数据驱动架构**：新增 §2 CSV 数据架构（设计原则/配置举例/效果速查表）、§3 CSV 文件规范（8张表字段说明）、§7.1 CSV 加载层接口；cards/effects 分离解耦；列名统一小写；`#` 注释行自文档化
- 2026-07-15 源GDD文档链更新：GDD-COMBAT-001（已废弃）→ GDD-BATTLEFIELD-001（权威文档）
