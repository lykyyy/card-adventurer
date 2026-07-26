---
id: ID-REFERENCE-GRAPH
title: 编号引用关系图
type: reference-graph
created: 2026-07-06
updated: 2026-07-06
tags: [reference, graph, id-management]
---

# 编号引用关系图

> 本文件记录编号之间的引用关系，用于残留覆盖预审检测4（跨系统残留检测）。
> 当某编号变更时，按此图查找所有依赖文件并同步更新。

## 1. 系统依赖关系

```
GDD-COMBAT-001（战斗系统）
├── 卡牌 (C-)：定义卡牌
├── 职业 (P-)：定义4个职业
├── 敌人 (E-)：定义5个敌人
├── 状态 (S-)：定义8个状态效果
└── 战斗流程：回合制+状态机

GDD-CHARACTER-001（角色系统）
├── 种族 (RACE-)：定义4个种族
├── 出身 (ORIGIN-)：定义6个出身
├── 技能 (SKILL-)：定义6个技能
├── 通用专长 (FEAT-G-)：定义9个专长
├── 传奇专长 (LFEAT-)：定义8个专长
└── 传奇道途 (PL-)：定义10个等级

GDD-CRAFTING-001（制作系统）
├── 药水 (POTION-)：定义8个药水
├── 卷轴 (SCROLL-)：定义6个卷轴
├── 魔杖 (WAND-)：定义4个魔杖
├── 附魔 (ENCH-)：定义6个附魔
├── 材料 (MAT-)：定义4个材料
└── 工作台 (WB-)：定义3个工作台

GDD-CORE-001（核心系统）
├── 职业专长 (PROF-FEAT-)：定义12个专长
├── 战士武器专长 (W-FEAT-)：定义3个专长
├── 盗贼武器专长 (R-FEAT-)：定义3个专长
├── 装备 (EQUIP-)：定义6个装备
└── 卡牌区间分配 (C-080~099)

GDD-TOWER-001（法师塔系统）
└── 建筑 (TOWER-)：定义1个建筑
```

## 2. 编号跨系统引用清单

| 编号前缀 | 定义系统 | 被引用系统 | 引用方式 |
|----------|----------|------------|----------|
| C- | GDD-CORE-001 | 战斗系统/制作系统 | 卡牌引用 |
| P- | GDD-COMBAT-001 | 战斗系统/职业专长 | 职业引用 |
| E- | GDD-COMBAT-001 | 战斗系统 | 敌人引用 |
| S- | GDD-COMBAT-001 | 战斗系统 | 状态引用 |
| EQUIP- | GDD-CORE-001 | 战斗系统/制作系统 | 装备引用 |
| ITEM- | 待定义 | 待定义 | 道具引用 |
| MAT- | GDD-CRAFTING-001 | 制作系统 | 材料引用 |
| POTION- | GDD-CRAFTING-001 | 制作系统 | 药水引用 |
| SCROLL- | GDD-CRAFTING-001 | 制作系统 | 卷轴引用 |
| WAND- | GDD-CRAFTING-001 | 制作系统 | 魔杖引用 |
| ENCH- | GDD-CRAFTING-001 | 制作系统 | 附魔引用 |
| WB- | GDD-CRAFTING-001 | 制作系统 | 工作台引用 |
| TOWER- | GDD-TOWER-001 | 法师塔系统 | 建筑引用 |
| RACE- | GDD-CHARACTER-001 | 角色系统 | 种族引用 |
| ORIGIN- | GDD-CHARACTER-001 | 角色系统 | 出身引用 |
| SKILL- | GDD-CHARACTER-001 | 角色系统 | 技能引用 |
| FEAT-G- | GDD-CHARACTER-001 | 角色系统 | 专长引用 |
| LFEAT- | GDD-CHARACTER-001 | 角色系统 | 传奇专长引用 |
| PL- | GDD-CHARACTER-001 | 角色系统 | 道途引用 |
| PROF-FEAT- | GDD-CORE-001 | 角色系统/战斗系统 | 职业专长引用 |
| W-FEAT- | GDD-CORE-001 | 战斗系统 | 战士武器专长引用 |
| R-FEAT- | GDD-CORE-001 | 战斗系统 | 盗贼武器专长引用 |

## 3. 各前缀文件引用明细

### C- (卡牌)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| cards.csv | data/csv/cards.csv | 卡牌数据 |
| card_effects.csv | data/csv/card_effects.csv | 卡牌效果数据 |
| GDD-COMBAT-001 | docs/GDD/GDD-COMBAT-001.md | 战斗系统卡牌定义 |
| GDD-CORE-001 | docs/GDD/GDD-CORE-001.md | 核心卡牌区间分配 |
| scripts/index.html | scripts/index.html | HTML原型代码 |

### E- (敌人)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| enemies.csv | data/csv/enemies.csv | 敌人属性数据 |
| enemy_skills.csv | data/csv/enemy_skills.csv | 敌人技能数据 |
| GDD-COMBAT-001 | docs/GDD/GDD-COMBAT-001.md | 战斗系统敌人定义 |

### P- (职业)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| professions.csv | data/csv/professions.csv | 职业属性数据 |
| profession_starting_deck.csv | data/csv/profession_starting_deck.csv | 职业初始牌组 |
| GDD-COMBAT-001 | docs/GDD/GDD-COMBAT-001.md | 战斗系统职业定义 |
| GDD-CORE-001 | docs/GDD/GDD-CORE-001.md | 职业专长关联 |

### S- (状态效果)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| status_effects.csv | data/csv/status_effects.csv | 状态效果数据 |
| GDD-COMBAT-001 | docs/GDD/GDD-COMBAT-001.md | 战斗系统状态定义 |

### EQUIP- (装备)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CORE-001 | docs/GDD/GDD-CORE-001.md | 装备系统定义 |

### ITEM- (物品/道具)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册（预留） |

### MAT- (制作材料)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CRAFTING-001 | docs/GDD/GDD-CRAFTING-001.md | 制作系统材料定义 |

### POTION- (药水)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CRAFTING-001 | docs/GDD/GDD-CRAFTING-001.md | 制作系统药水定义 |

### SCROLL- (卷轴)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CRAFTING-001 | docs/GDD/GDD-CRAFTING-001.md | 制作系统卷轴定义 |

### WAND- (魔杖)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CRAFTING-001 | docs/GDD/GDD-CRAFTING-001.md | 制作系统魔杖定义 |

### ENCH- (附魔效果)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CRAFTING-001 | docs/GDD/GDD-CRAFTING-001.md | 制作系统附魔定义 |

### WB- (工作台)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CRAFTING-001 | docs/GDD/GDD-CRAFTING-001.md | 制作系统工作台定义 |

### TOWER- (法师塔建筑)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-TOWER-001 | docs/GDD/GDD-TOWER-001.md | 法师塔系统定义 |

### RACE- (种族)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| races.csv | data/csv/races.csv | 种族属性数据 |
| GDD-CHARACTER-001 | docs/GDD/GDD-CHARACTER-001.md | 角色系统种族定义 |

### ORIGIN- (出身)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| origins.csv | data/csv/origins.csv | 出身定义数据 |
| GDD-CHARACTER-001 | docs/GDD/GDD-CHARACTER-001.md | 角色系统出身定义 |

### SKILL- (技能)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| skills.csv | data/csv/skills.csv | 技能定义数据 |
| GDD-CHARACTER-001 | docs/GDD/GDD-CHARACTER-001.md | 角色系统技能定义 |

### FEAT-G- (通用专长)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| feats_general.csv | data/csv/feats_general.csv | 通用专长数据 |
| GDD-CHARACTER-001 | docs/GDD/GDD-CHARACTER-001.md | 角色系统专长定义 |

### LFEAT- (传奇专长)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| feats_legendary.csv | data/csv/feats_legendary.csv | 传奇专长数据 |
| GDD-CHARACTER-001 | docs/GDD/GDD-CHARACTER-001.md | 角色系统专长定义 |

### PL- (传奇道途等级)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| legendary_path.csv | data/csv/legendary_path.csv | 传奇道途数据 |
| GDD-CHARACTER-001 | docs/GDD/GDD-CHARACTER-001.md | 角色系统道途定义 |

### PROF-FEAT- (职业专长)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CORE-001 | docs/GDD/GDD-CORE-001.md | 核心系统职业专长定义 |

### W-FEAT- (战士武器专长)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CORE-001 | docs/GDD/GDD-CORE-001.md | 核心系统战士武器专长定义 |

### R-FEAT- (盗贼武器专长)
| 引用位置 | 文件 | 说明 |
|----------|------|------|
| ID-REGISTRY | docs/GDD/ID-REGISTRY.md | 中央注册 |
| GDD-CORE-001 | docs/GDD/GDD-CORE-001.md | 核心系统盗贼武器专长定义 |

## 变更日志
- 2026-07-12 补全所有20个前缀的跨系统引用明细表
- 2026-07-06 初始创建
