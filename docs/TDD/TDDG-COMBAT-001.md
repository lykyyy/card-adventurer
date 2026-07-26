---
id: TDDG-COMBAT-001
title: 战斗系统技术设计（Godot原型）
type: TDD-Godot
system: combat
version: 0.1.0
status: draft
source_gdd: "[[GDD-COMBAT-001]]"
related_pdd: "[[PDD-COMBAT-001]]"
created: 2026-06-29
author: tech-lead
reviewer: human
---

# 战斗系统技术设计（Godot原型）

## 1. 技术方案
- 引擎：Godot 4.6
- 语言：GDScript
- 场景结构：主场景 → 战斗场景 → UI层
- 数据持久化：Resource + JSON文件

## 2. 节点结构
```
Main (Node2D)
├── BattleScene (Node2D)
│   ├── EnemyArea (Node2D)
│   │   ├── EnemySprite (Sprite2D)
│   │   ├── EnemyHPBar (ProgressBar)
│   │   ├── EnemyName (Label)
│   │   └── EnemyIntent (Label)
│   ├── PlayerArea (Node2D)
│   │   ├── PlayerHPBar (ProgressBar)
│   │   ├── ManaBar (ProgressBar)
│   │   ├── ShieldLabel (Label)
│   │   └── PlayerName (Label)
│   ├── HandArea (HBoxContainer)
│   │   └── CardSlot×5 (TextureButton)
│   ├── EndTurnButton (Button)
│   └── BattleEffects (Node2D)
│       └── DamageNumber (Label)
└── UI (CanvasLayer)
    ├── VictoryScreen (Panel)
    └── DefeatScreen (Panel)
```

## 3. 数据结构

### 玩家资源（Resource）
```gdscript
class_name PlayerData extends Resource
@export var id: String = "P001"
@export var name: String = "战士"
@export var hp: int = 200
@export var max_hp: int = 200
@export var mana: int = 1
@export var max_mana: int = 1
@export var shield: int = 0
@export var deck: Array[CardData] = []
@export var hand: Array[CardData] = []
@export var discard: Array[CardData] = []
@export var equipment: Array[CardData] = []
@export var collection: Array[CardData] = []
```

### 卡牌资源（Resource）
```gdscript
class_name CardData extends Resource
@export var id: String = "C001"
@export var name: String = "攻击"
@export var card_type: String = "基本"  # "基本" / "技能" / "装备"
@export var cost: int = 0
@export var damage: int = 0
@export var heal: int = 0
@export var shield: int = 0
@export var description: String = ""
@export var effect_type: String = "damage"  # "damage" / "heal" / "shield" / "equipment_shield" / "equipment_damage"
@export var equipment_bonus: int = 0
```

### 敌人资源（Resource）
```gdscript
class_name EnemyData extends Resource
@export var id: String = "E001"
@export var name: String = "史莱姆"
@export var hp: int = 50
@export var max_hp: int = 50
@export var attack: int = 8
@export var intents: Array[Dictionary] = []
```

## 4. 核心脚本
1. **game_manager.gd** — 游戏主循环、状态机管理、全局状态
2. **card_system.gd** — 卡牌数据与效果执行、牌组管理
3. **enemy_ai.gd** — 敌人AI决策、技能执行
4. **battle_ui.gd** — 战斗界面渲染、事件监听
5. **turn_manager.gd** — 回合切换逻辑、状态转换
6. **reward_system.gd** — 选卡奖励界面、卡牌收集

## 5. 信号定义（事件系统）
```gdscript
signal on_damage(target: String, amount: int)
signal on_heal(target: String, amount: int)
signal on_shield(target: String, amount: int)
signal on_turn_end()
signal on_battle_end(result: String)
signal on_card_play(card: CardData)
signal on_deck_empty()
```

## 6. 核心接口定义

### 6.1 卡牌系统
- `play_card(card: CardData)` → void — 打出卡牌，执行效果
- `draw_card(count: int)` → void — 抽指定数量卡牌
- `discard_hand()` → void — 弃置所有手牌
- `shuffle_discard_to_deck()` → void — 洗入弃牌堆
- `add_to_collection(card: CardData)` → void — 添加到收集册

### 6.2 战斗系统
- `start_battle(battle_number: int)` → void — 开始第N场战斗
- `end_player_turn()` → void — 结束玩家回合
- `execute_enemy_turn()` → void — 执行敌人回合
- `check_battle_end()` → bool — 检查战斗是否结束

### 6.3 玩家系统
- `take_damage(amount: int)` → void — 受到伤害
- `heal(amount: int)` → void — 恢复生命
- `add_shield(amount: int)` → void — 获得护盾
- `set_mana(amount: int)` → void — 设置法力值

## 7. 状态机实现
| 当前状态 | 实际变量 | 转换条件 | 目标状态 |
|----------|----------|----------|----------|
| 战斗开始 | "battle_start" | 场景加载 | "player_turn" |
| 玩家回合 | "player_turn" | 点击结束回合 | "enemy_turn" |
| 敌人回合 | "enemy_turn" | AI执行完毕 | "player_turn" |
| 玩家回合 | "player_turn" | 敌人HP≤0 | "victory" |
| 敌人回合 | "enemy_turn" | 玩家HP≤0 | "defeat" |

## 8. 开发顺序
1. 场景搭建 + 节点结构 + 基础UI
2. 数据资源定义（CardData, PlayerData, EnemyData）
3. 卡牌系统（抽牌、出牌、弃牌）
4. 战斗结算（伤害、护盾、治疗）
5. 敌人AI（概率选择技能）
6. 回合管理与胜负判定
7. 选卡奖励界面
8. 多场战斗递进和Boss战

## 变更日志
- 2026-06-29 v0.1.0 初始创建
