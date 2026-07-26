---
id: TDDG-{系统}-{序号}
title: {系统名称}技术设计（Godot原型）
type: TDD-Godot
system: {系统名}
version: 0.1.0
status: draft
source_gdd: "[[GDD-{系统}-{序号}]]"
related_pdd: "[[PDD-{系统}-{序号}]]"
created: YYYY-MM-DD
author: tech-lead
reviewer: human
---

# {系统名称}技术设计（Godot原型）

## 1. 技术方案
- 引擎：Godot 4.x
- 语言：GDScript
- 场景结构：主场景 → 战斗场景 → UI层

## 2. 节点结构
```
Main (Node2D)
├── BattleScene (Node2D)
│   ├── EnemyArea (Node2D)
│   │   ├── EnemySprite (Sprite2D)
│   │   ├── EnemyHPBar (ProgressBar)
│   │   └── EnemyIntent (Label)
│   ├── PlayerArea (Node2D)
│   │   ├── PlayerHPBar (ProgressBar)
│   │   ├── ManaBar (ProgressBar)
│   │   └── ShieldLabel (Label)
│   └── HandArea (HBoxContainer)
│       └── CardSlot×5 (TextureButton)
│   └── EndTurnButton (Button)
└── UI (CanvasLayer)
```

## 3. 数据结构
### 玩家资源（Resource）
```
player_data.gd:
- id: String
- name: String
- hp: int
- max_hp: int
- mana: int
- max_mana: int
- shield: int
- deck: Array[CardData]
- hand: Array[CardData]
- discard: Array[CardData]
```

### 卡牌资源（Resource）
```
card_data.gd:
- id: String
- name: String
- type: String  # "基本" / "装备"
- cost: int
- damage: int
- description: String
```

## 4. 核心脚本
1. game_manager.gd — 游戏主循环、状态机管理
2. card_system.gd — 卡牌数据与效果执行
3. enemy_ai.gd — 敌人AI决策
4. battle_ui.gd — 战斗界面渲染
5. turn_manager.gd — 回合切换逻辑

## 5. 信号定义（事件系统）
```
signal on_damage(target, amount)
signal on_heal(target, amount)
signal on_shield(target, amount)
signal on_turn_end()
signal on_battle_end(result)
```

## 6. 开发顺序
1. 场景搭建 + 节点结构 + 基础UI
2. 数据资源定义（CardData, PlayerData）
3. 卡牌系统（抽牌、出牌、弃牌）
4. 战斗结算（伤害、护盾、治疗）
5. 敌人AI（概率选择技能）
6. 回合管理与胜负判定
7. 选卡奖励界面

## 变更日志
- [日期] v0.1.0 初始创建
