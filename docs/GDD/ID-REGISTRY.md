---
id: ID-REGISTRY
title: 元素编号注册表
type: registry
created: 2026-07-06
updated: 2026-07-12
tags: [registry, id-management, card-adventurer]
---

# 元素编号注册表

> 所有元素的编号必须在此注册，未注册的编号视为非法。
> 本注册表是编号一致性的唯一权威来源。

## 中央数据库声明

> 本文件是项目的**唯一中央数据库**，所有游戏元素的权威定义均在此处。
> GDD文件中的元素引用必须以本文件为准，GDD文件不得独立定义元素。

### 数据源原则
1. **唯一数据源**：每个ID的唯一权威定义仅存在于本文件
2. **引用模式**：GDD文件引用ID时，必须使用`[[ID-REGISTRY|ID-XXX 定义]]`内部链接
3. **定义源标记**：每个ID的"定义源文件"字段标记其设计意图来源（GDD-XXX）
4. **修改优先**：修改任何ID定义时，必须先修改本文件，再传播到GDD文件

---

## 编号管理机制

### 核心铁律：注册先于写入

> **任何新元素必须先在此注册表中获得编号并验证通过，方可写入任何GDD文件。**

### 新增编号标准流程（4步）

1. **申请**：设计者提交编号申请（元素类型/名称/定义源文件/数量/功能描述）
2. **验证**：验证5项（前缀合法/序号未占用/非废弃/格式合规/预留空间）
3. **分配**：验证通过后在ID-REGISTRY中注册，标记"✅已注册"
4. **写入**：编号分配完成后，方可使用该编号在GDD文件中写入内容

---

## 编号格式规范

| 前缀 | 含义 | 格式 | 示例 | 定义源文件 |
|------|------|------|------|-----------|
| C- | 卡牌 | C-{3位序号} | C-001 | GDD-COMBAT-001 |
| P- | 职业 | P-{3位序号} | P-001 | GDD-COMBAT-001 |
| E- | 敌人 | E-{3位序号} | E-001 | GDD-COMBAT-001 |
| S- | 状态效果 | S-{3位序号} | S-001 | GDD-COMBAT-001 |
| ITEM- | 物品/道具 | ITEM-{3位序号} | ITEM-001 | 待定义 |
| EQUIP- | 装备 | EQUIP-{3位序号} | EQUIP-001 | 待定义 |
| RACE- | 种族 | RACE-{3位序号} | RACE-001 | GDD-CHARACTER-001 |
| ORIGIN- | 出身 | ORIGIN-{3位序号} | ORIGIN-001 | GDD-CHARACTER-001 |
| SKILL- | 技能 | SKILL-{2位序号} | SKILL-01 | GDD-CHARACTER-001 |
| FEAT-G- | 通用专长 | FEAT-G-{2位序号} | FEAT-G-01 | GDD-CHARACTER-001 |
| LFEAT- | 传奇专长 | LFEAT-{2位序号} | LFEAT-01 | GDD-CHARACTER-001 |
| PL- | 传奇道途等级 | PL{1位序号} | PL1 | GDD-CHARACTER-001 |
| POTION- | 药水 | POTION-{3位序号} | POTION-001 | GDD-CRAFTING-001 |
| SCROLL- | 卷轴 | SCROLL-{3位序号} | SCROLL-001 | GDD-CRAFTING-001 |
| WAND- | 魔杖 | WAND-{3位序号} | WAND-001 | GDD-CRAFTING-001 |
| ENCH- | 附魔效果 | ENCH-{3位序号} | ENCH-001 | GDD-CRAFTING-001 |
| MAT- | 制作材料 | MAT-{3位序号} | MAT-001 | GDD-CRAFTING-001 |
| WB- | 工作台 | WB-{3位序号} | WB-001 | GDD-CRAFTING-001 |
| TOWER- | 法师塔建筑 | TOWER-{3位序号} | TOWER-001 | GDD-TOWER-001 |
| PROF-FEAT- | 职业专长 | PROF-FEAT-{3位序号} | PROF-FEAT-001 | GDD-CORE-001 |
| W-FEAT- | 战士武器专长 | W-FEAT-{3位序号} | W-FEAT-001 | GDD-CORE-001 |
| R-FEAT- | 盗贼武器专长 | R-FEAT-{3位序号} | R-FEAT-001 | GDD-CORE-001 |
| BG-FEAT- | 背景专长 | BG-FEAT-{3位序号} | BG-FEAT-001 | GDD-CHARACTER-001 |

---

## 注册统计表

| 前缀 | 含义 | 已注册数 | 预留区间 | 状态 |
|------|------|----------|----------|------|
| C- | 卡牌 | 27 (活跃) + 19 (废弃→9复用) | 001-099 | ✅活跃 |
| P- | 职业 | 4 | 001-009 | ✅活跃 |
| E- | 敌人 | 5 | 001-099 | ✅活跃 |
| S- | 状态效果 | 8 | 001-009 | ✅活跃 |
| ITEM- | 物品 | 0 | 001-099 | 🔒预留 |
| EQUIP- | 装备 | 6 | 001-099 | ✅活跃 |
| RACE- | 种族 | 4 | 001-009 | ✅活跃 |
| ORIGIN- | 出身 | 6 | 001-009 | ✅活跃 |
| SKILL- | 技能 | 6 | 01-09 | ✅活跃 |
| FEAT-G- | 通用专长 | 9 | 01-99 | ✅活跃 |
| LFEAT- | 传奇专长 | 8 | 01-99 | ✅活跃 |
| PL- | 传奇道途等级 | 10 | 1-9 | ✅活跃 |
| PROF-FEAT- | 职业专长 | 12 | 001-099 | ✅活跃 |
| W-FEAT- | 战士武器专长 | 3 | 001-009 | ✅活跃 |
| R-FEAT- | 盗贼武器专长 | 3 | 001-009 | ✅活跃 |
| POTION- | 药水 | 8 | 001-099 | ✅活跃 |
| SCROLL- | 卷轴 | 6 | 001-099 | ✅活跃 |
| WAND- | 魔杖 | 4 | 001-099 | ✅活跃 |
| ENCH- | 附魔效果 | 6 | 001-099 | ✅活跃 |
| MAT- | 制作材料 | 4 | 001-099 | ✅活跃 |
| WB- | 工作台 | 3 | 001-099 | ✅活跃 |
| BG-FEAT- | 背景专长 | 9 | 001-099 | ✅活跃 |
| TOWER- | 法师塔建筑 | 1 | 001-009 | ✅活跃 |

---

## 已注册编号清单

### 职业 (P-)

| ID | 名称 | 定义源文件 | CSV数据文件 | 状态 |
|----|------|-----------|------------|------|
| P-001 | 战士 | GDD-COMBAT-001 | data/csv/professions.csv | ✅已注册 |
| P-002 | 法师 | GDD-CORE-001 | data/csv/professions.csv | ✅已注册 |
| P-003 | 盗贼 | GDD-CORE-001 | data/csv/professions.csv | ✅已注册 |
| P-004 | 牧师 | GDD-CORE-001 | data/csv/professions.csv | ✅已注册 |

### 卡牌 (C-)

| ID | 名称 | 类型 | 定义源文件 | CSV数据文件 | 状态 |
|----|------|------|-----------|------------|------|
| C-001 | 攻击 | 基本牌 | GDD-COMBAT-001 | data/csv/cards.csv | ❌已废弃 → 装备·C-080 |
| C-002 | 防御 | 基本牌 | GDD-COMBAT-001 | data/csv/cards.csv | ❌已废弃 → 防具系统+技能 |
| C-003 | 重击 | 技能牌 | GDD-COMBAT-001 | data/csv/cards.csv | ❌已废弃 → 武器专精牌 |
| C-004 | 急救 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（保留为通用辅助牌·急救） |
| C-005 | 护甲 | 装备牌 | GDD-COMBAT-001 | data/csv/cards.csv | ❌已废弃 → 防具系统(EQUIP-006) |
| C-006 | 武器 | 装备牌 | GDD-COMBAT-001 | data/csv/cards.csv | ❌已废弃 → 武器系统(EQUIP-001~005) |
| C-007 | 斩击 | 技能牌 | GDD-COMBAT-001 | data/csv/cards.csv | ❌已废弃 → C-081(长剑基础) |
| C-008 | 连斩 | — | — | — | ❌已废弃 → C-083(长剑专精) |
| C-009 | 全力一击 | — | — | — | ❌已废弃 → 职业终极牌 |
| C-010 | 蓄力斩 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（战士核心牌） |
| C-011 | 格挡反击 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（战士核心牌） |
| C-012 | 怒意爆发 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（战士核心牌） |
| C-013 | 战斗狂热 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（战士核心牌） |
| C-014 | 毁灭之握 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（战士核心牌） |
| C-020 | 双重打击 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（盗贼核心牌） |
| C-021 | 烟雾掩护 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（盗贼核心牌） |
| C-022 | 刺骨 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（盗贼核心牌） |
| C-023 | 暗影预备 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（盗贼核心牌） |
| C-024 | 死亡莲华 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（盗贼核心牌） |
| C-030 | 奥术飞弹 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（法师戏法） |
| C-031 | 魔法护盾 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（法师戏法） |
| C-032 | 烈焰风暴 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（法师戏法） |
| C-033 | 魔力回流 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（法师戏法） |
| C-034 | 星辰陨落 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（法师戏法） |
| C-050 | 圣光击 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（牧师核心牌） |
| C-051 | 治疗祷言 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（牧师核心牌） |
| C-052 | 光耀之盾 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（牧师核心牌） |
| C-053 | 公正审判 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（牧师核心牌） |
| C-054 | 净化 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（牧师核心牌） |
| C-072 | 战备 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（通用辅助） |
| C-073 | 专注 | 技能牌 | GDD-CORE-001 | data/csv/cards.csv | ✅已注册（通用辅助） |
| C-076 | 战术集火 | 技能牌 | GDD-BATTLEFIELD-001 | data/csv/cards.csv | ✅已注册（团队卡牌） |
| C-077 | 防御阵型 | 技能牌 | GDD-BATTLEFIELD-001 | data/csv/cards.csv | ✅已注册（团队卡牌） |
| C-078 | 战术撤退 | 技能牌 | GDD-BATTLEFIELD-001 | data/csv/cards.csv | ✅已注册（团队卡牌） |
| C-079 | 集中火力 | 技能牌 | GDD-BATTLEFIELD-001 | data/csv/cards.csv | ✅已注册（团队卡牌） |
| C-080 | 星图导航 | 战略牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（战略卡·出身奖励） |
| C-081 | 贸易协定 | 战略牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（战略卡·出身奖励） |
| C-082 | 情报网络 | 战略牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（战略卡·出身奖励） |
| C-083 | 紧急维修 | 战略牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（战略卡·出身奖励） |
| C-090 | 精准打击 | 技能牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（通用攻击·属性关联） |
| C-091 | 战术指挥 | 技能牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（通用辅助·属性关联） |
| C-092 | 绝境反击 | 技能牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（通用攻击·残血加成） |
| C-093 | 灵活闪避 | 技能牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（通用防御·属性关联） |
| C-094 | 快速包扎 | 技能牌 | GDD-CHARACTER-001 | data/csv/cards.csv | ✅已注册（通用辅助·属性关联） |

### 敌人 (E-)

| ID | 名称 | 定义源文件 | CSV数据文件 | 状态 |
|----|------|-----------|------------|------|
| E-001 | 史莱姆 | GDD-COMBAT-001 | data/csv/enemies.csv | ✅已注册 |
| E-002 | 哥布林 | GDD-COMBAT-001 | data/csv/enemies.csv | ✅已注册 |
| E-003 | 骷髅兵 | GDD-COMBAT-001 | data/csv/enemies.csv | ✅已注册 |
| E-004 | 狼人 | GDD-COMBAT-001 | data/csv/enemies.csv | ✅已注册 |
| E-005 | 暗影领主 | GDD-COMBAT-001 | data/csv/enemies.csv | ✅已注册 |

### 状态效果 (S-)

| ID | 名称 | 定义源文件 | CSV数据文件 | 状态 |
|----|------|-----------|------------|------|
| S-001 | 护盾 | GDD-COMBAT-001 | data/csv/status_effects.csv | ✅已注册 |
| S-002 | 狂暴 | GDD-COMBAT-001 | data/csv/status_effects.csv | ✅已注册 |
| S-003 | 虚弱 | GDD-COMBAT-001 | data/csv/status_effects.csv | ✅已注册 |
| S-004 | 流血 | GDD-CORE-001 | - | ✅已注册 |
| S-005 | 灼烧 | GDD-CORE-001 | - | ✅已注册 |
| S-006 | 减速 | GDD-CORE-001 | - | ✅已注册 |
| S-007 | 致盲 | GDD-CORE-001 | - | ✅已注册 |
| S-008 | 标记 | GDD-CORE-001 | - | ✅已注册 |

### 种族 (RACE-)

| ID | 名称 | 定义源文件 | 状态 |
|----|------|-----------|------|
| RACE-001 | 人类 | GDD-CHARACTER-001 | ✅已注册 |
| RACE-002 | 精灵 | GDD-CHARACTER-001 | ✅已注册 |
| RACE-003 | 矮人 | GDD-CHARACTER-001 | ✅已注册 |
| RACE-004 | 兽人 | GDD-CHARACTER-001 | ✅已注册 |

### 出身 (ORIGIN-)

| ID | 名称 | 定义源文件 | 状态 |
|----|------|-----------|------|
| ORIGIN-001 | 星舰之子 | GDD-CHARACTER-001 | ✅已注册 |
| ORIGIN-002 | 学院学者 | GDD-CHARACTER-001 | ✅已注册 |
| ORIGIN-003 | 拾荒游民 | GDD-CHARACTER-001 | ✅已注册 |
| ORIGIN-004 | 商团代理 | GDD-CHARACTER-001 | ✅已注册 |
| ORIGIN-005 | 殖民地开拓者 | GDD-CHARACTER-001 | ✅已注册 |
| ORIGIN-006 | 星界孤儿 | GDD-CHARACTER-001 | ✅已注册 |

### 技能 (SKILL-)

| ID | 名称 | 主属性 | 副属性 | 定义源文件 | 状态 |
|----|------|--------|--------|-----------|------|
| SKILL-01 | 运动 | STR | CON | GDD-CHARACTER-001 | ✅已注册 |
| SKILL-02 | 灵巧 | DEX | STR | GDD-CHARACTER-001 | ✅已注册 |
| SKILL-03 | 调查 | INT | WIS | GDD-CHARACTER-001 | ✅已注册 |
| SKILL-04 | 学识 | INT | CHA | GDD-CHARACTER-001 | ✅已注册 |
| SKILL-05 | 洞察 | WIS | INT | GDD-CHARACTER-001 | ✅已注册 |
| SKILL-06 | 交涉 | CHA | WIS | GDD-CHARACTER-001 | ✅已注册 |

### 通用专长 (FEAT-G-)

| ID | 名称 | 条件 | 定义源文件 | 状态 |
|----|------|------|-----------|------|
| FEAT-G-01 | 警觉 | Lv4, WIS≥13 | GDD-CHARACTER-001 | ✅已注册 |
| FEAT-G-02 | 健壮 | Lv4, CON≥13 | GDD-CHARACTER-001 | ✅已注册 |
| FEAT-G-03 | 博学 | Lv4, INT≥13 | GDD-CHARACTER-001 | ✅已注册 |
| FEAT-G-04 | 魅力 | Lv4, CHA≥13 | GDD-CHARACTER-001 | ✅已注册 |
| FEAT-G-05 | 巧手 | Lv4, DEX≥13 | GDD-CHARACTER-001 | ✅已注册 |
| FEAT-G-06 | 猛力攻击 | Lv8, STR≥16 | GDD-CHARACTER-001 | ✅已注册 |
| FEAT-G-07 | 战地医疗 | Lv8, WIS≥16 | GDD-CHARACTER-001 | ✅已注册 |
| FEAT-G-08 | 双持客 | Lv8, DEX≥16 | GDD-CHARACTER-001 | ✅已注册 |
| FEAT-G-09 | 法术反制 | Lv12, INT≥16 | GDD-CHARACTER-001 | ✅已注册 |

### 传奇专长 (LFEAT-)

| ID | 名称 | 前提 | 定义源文件 | 状态 |
|----|------|------|-----------|------|
| LFEAT-01 | 传奇健壮 | PL1, CON≥20 | GDD-CHARACTER-001 | ✅已注册 |
| LFEAT-02 | 传奇战技 | PL1, STR或DEX≥20 | GDD-CHARACTER-001 | ✅已注册 |
| LFEAT-03 | 伤害减免 | PL2, CON≥22 | GDD-CHARACTER-001 | ✅已注册 |
| LFEAT-04 | 传奇施法 | PL2, INT/WIS/CHA≥22 | GDD-CHARACTER-001 | ✅已注册 |
| LFEAT-05 | 完美双持 | PL3, DEX≥24 | GDD-CHARACTER-001 | ✅已注册 |
| LFEAT-06 | 传奇武器专精 | PL3, STR或DEX≥24 | GDD-CHARACTER-001 | ✅已注册 |
| LFEAT-07 | 超越极限 | PL5 | GDD-CHARACTER-001 | ✅已注册 |
| LFEAT-08 | 不朽灵魂 | PL7 | GDD-CHARACTER-001 | ✅已注册 |

### 职业专长 (PROF-FEAT-)

| ID | 名称 | 职业 | 定义源文件 | 状态 |
|----|------|------|-----------|------|
| PROF-FEAT-001 | 狂战士 | P-001 战士 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-002 | 守护者(战士) | P-001 战士 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-003 | 战术家 | P-001 战士 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-004 | 刺客 | P-003 盗贼 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-005 | 诡术师 | P-003 盗贼 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-006 | 斥候 | P-003 盗贼 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-007 | 塑能师 | P-002 法师 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-008 | 奥术师 | P-002 法师 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-009 | 控场师 | P-002 法师 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-010 | 治疗者 | P-004 牧师 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-011 | 审判官 | P-004 牧师 | GDD-CORE-001 | ✅已注册 |
| PROF-FEAT-012 | 守护者(牧师) | P-004 牧师 | GDD-CORE-001 | ✅已注册 |

### 战士武器专长 (W-FEAT-)

| ID | 名称 | 定义源文件 | 状态 |
|----|------|-----------|------|
| W-FEAT-001 | 处刑者 | GDD-CORE-001 | ✅已注册 |
| W-FEAT-002 | 角斗士 | GDD-CORE-001 | ✅已注册 |
| W-FEAT-003 | 武器大师 | GDD-CORE-001 | ✅已注册 |

### 盗贼武器专长 (R-FEAT-)

| ID | 名称 | 定义源文件 | 状态 |
|----|------|-----------|------|
| R-FEAT-001 | 毒师 | GDD-CORE-001 | ✅已注册 |
| R-FEAT-002 | 幻影 | GDD-CORE-001 | ✅已注册 |
| R-FEAT-003 | 伏击者 | GDD-CORE-001 | ✅已注册 |

### 背景专长 (BG-FEAT-)

| ID | 名称 | 解锁步骤 | 效果 | 定义源文件 | 状态 |
|----|------|----------|------|-----------|------|
| BG-FEAT-001 | 街头智慧 | 步骤7-A | 偷窃成功率+20%，陷阱侦测+1 | GDD-CHARACTER-001 | ✅已注册 |
| BG-FEAT-002 | 学院教育 | 步骤7-B | 知识检定优势，额外理解1种古代语言 | GDD-CHARACTER-001 | ✅已注册 |
| BG-FEAT-003 | 流浪直觉 | 步骤7-C | 航行时多1航路选项，随机事件预知 | GDD-CHARACTER-001 | ✅已注册 |
| BG-FEAT-004 | 老兵韧性 | 步骤8-A | 战斗结束后恢复5HP | GDD-CHARACTER-001 | ✅已注册 |
| BG-FEAT-005 | 工匠精神 | 步骤8-B | 制作/修理费用-10%，鉴定免费 | GDD-CHARACTER-001 | ✅已注册 |
| BG-FEAT-006 | 信仰之力 | 步骤8-C | 每场战斗1次，免伤5点 | GDD-CHARACTER-001 | ✅已注册 |
| BG-FEAT-007 | 复仇意志 | 步骤9-A | 对精英/Boss敌人伤害+15% | GDD-CHARACTER-001 | ✅已注册 |
| BG-FEAT-008 | 渊博学识 | 步骤9-B | 每等级额外获得1张法术牌选项 | GDD-CHARACTER-001 | ✅已注册 |
| BG-FEAT-009 | 命运眷顾 | 步骤9-C | 战利品稀有度提升1档（上限稀有） | GDD-CHARACTER-001 | ✅已注册 |

### 装备 (EQUIP-)

| ID | 名称 | 定义源文件 | 状态 |
|----|------|-----------|------|
| EQUIP-001 | 武器装备(长剑) | GDD-CORE-001 | ✅已注册 |
| EQUIP-002 | 武器装备(短剑) | GDD-CORE-001 | ✅已注册 |
| EQUIP-003 | 武器装备(法杖) | GDD-CORE-001 | ✅已注册 |
| EQUIP-004 | 武器装备(锤) | GDD-CORE-001 | ✅已注册 |
| EQUIP-005 | 武器装备(弓) | GDD-CORE-001 | ✅已注册 |
| EQUIP-006 | 防具装备(护甲) | GDD-CORE-001 | ✅已注册 |

### 药水 (POTION-)

| ID | 名称 | 稀有度 | 定义源文件 | 状态 |
|----|------|--------|-----------|------|
| POTION-001 | 初级法力药剂 | 常见 | GDD-CRAFTING-001 | ✅已注册 |
| POTION-002 | 以太药剂 | 常见 | GDD-CRAFTING-001 | ✅已注册 |
| POTION-003 | 治疗药剂 | 常见 | GDD-CRAFTING-001 | ✅已注册 |
| POTION-004 | AP充能 | 罕见 | GDD-CRAFTING-001 | ✅已注册 |
| POTION-005 | EP电池 | 罕见 | GDD-CRAFTING-001 | ✅已注册 |
| POTION-006 | CE催化剂 | 罕见 | GDD-CRAFTING-001 | ✅已注册 |
| POTION-007 | 大法力药剂 | 稀有 | GDD-CRAFTING-001 | ✅已注册 |
| POTION-008 | 全效药剂 | 传奇 | GDD-CRAFTING-001 | ✅已注册 |

### 卷轴 (SCROLL-)

| ID | 名称 | 法术等级 | 定义源文件 | 状态 |
|----|------|----------|-----------|------|
| SCROLL-001 | 火球术卷轴 | 1级 | GDD-CRAFTING-001 | ✅已注册 |
| SCROLL-002 | 冰霜新星卷轴 | 1级 | GDD-CRAFTING-001 | ✅已注册 |
| SCROLL-003 | 闪电链卷轴 | 2级 | GDD-CRAFTING-001 | ✅已注册 |
| SCROLL-004 | 石肤术卷轴 | 2级 | GDD-CRAFTING-001 | ✅已注册 |
| SCROLL-005 | 传送卷轴 | 1级 | GDD-CRAFTING-001 | ✅已注册 |
| SCROLL-006 | 陨石术卷轴 | 3级 | GDD-CRAFTING-001 | ✅已注册 |

### 魔杖 (WAND-)

| ID | 名称 | 充能 | 定义源文件 | 状态 |
|----|------|------|-----------|------|
| WAND-001 | 魔法飞弹魔杖 | 3 | GDD-CRAFTING-001 | ✅已注册 |
| WAND-002 | 护盾魔杖 | 2 | GDD-CRAFTING-001 | ✅已注册 |
| WAND-003 | 火球魔杖 | 2 | GDD-CRAFTING-001 | ✅已注册 |
| WAND-004 | 奥术风暴魔杖 | 4 | GDD-CRAFTING-001 | ✅已注册 |

### 附魔效果 (ENCH-)

| ID | 名称 | 效果 | 定义源文件 | 状态 |
|----|------|------|-----------|------|
| ENCH-001 | 法力强化 | 法力上限+1 | GDD-CRAFTING-001 | ✅已注册 |
| ENCH-002 | 护盾共鸣 | 战斗开始时获得5护盾 | GDD-CRAFTING-001 | ✅已注册 |
| ENCH-003 | 生命纽带 | HP上限+15 | GDD-CRAFTING-001 | ✅已注册 |
| ENCH-004 | 锋锐 | 攻击伤害+3 | GDD-CRAFTING-001 | ✅已注册 |
| ENCH-005 | 精准 | 全部伤害+2 | GDD-CRAFTING-001 | ✅已注册 |
| ENCH-006 | 元素防护 | 受到伤害-2 | GDD-CRAFTING-001 | ✅已注册 |

### 制作材料 (MAT-)

| ID | 名称 | 稀有度 | 获取途径 | 定义源文件 | 状态 |
|----|------|--------|----------|-----------|------|
| MAT-001 | 星尘 | 常见 | L2网格·资源牌/商店30G | GDD-CRAFTING-001 | ✅已注册 |
| MAT-002 | 以太精华 | 罕见 | 战斗奖励(法师敌人)/L2事件牌 | GDD-CRAFTING-001 | ✅已注册 |
| MAT-003 | 魔晶碎片 | 稀有 | Boss掉落/L2锁定宝箱 | GDD-CRAFTING-001 | ✅已注册 |
| MAT-004 | 远古遗物 | 传奇 | 主线剧情/传奇试炼 | GDD-CRAFTING-001 | ✅已注册 |

### 工作台 (WB-)

| ID | 名称 | 场景主题 | 制作加成 | 定义源文件 | 状态 |
|----|------|----------|----------|-----------|------|
| WB-001 | 星港工坊 | 银蓝金属网格+扫描线 | 基础无加成 | GDD-CRAFTING-001 | ✅已注册 |
| WB-002 | 船载实验室 | 橙金暗舱壁+脉冲光 | 制作速度+20% | GDD-CRAFTING-001 | ✅已注册 |
| WB-003 | 法师塔炼金台 | 紫金魔法符文+粒子 | 制作检定+2/大成功DC-3 | GDD-CRAFTING-001 | ✅已注册 |

### 法师塔建筑 (TOWER-)

| ID | 名称 | 说明 | 定义源文件 | 状态 |
|----|------|------|-----------|------|
| TOWER-001 | 法师塔 | 法师专属局外成长建筑，Lv1-5逐步解锁研究/炼金/附魔/转化/塔灵功能 | GDD-TOWER-001 | ✅已注册 |

---

## 已废弃编号

| 编号 | 废弃日期 | 原因 | 替代编号 |
|------|----------|------|----------|
| C-001 | 2026-07-09 | 攻击牌归入装备系统 | C-080拳击 / 各武器基础牌 |
| C-002 | 2026-07-09 | 防御牌归入防具+技能系统 | 防具系统 + 技能·灵巧·影袭 |
| C-003 | 2026-07-09 | 重击归入武器专精 | C-082猛击(长剑熟练) 等 |
| C-005 | 2026-07-09 | 护甲归入防具装备 | EQUIP-006 |
| C-006 | 2026-07-09 | 武器归入武器装备 | EQUIP-001~005 |
| C-007 | 2026-07-09 | 斩击与武器牌重复 | C-081斩击(长剑基础) |
| C-008 | 2026-07-09 | 连斩与专精牌重复 | C-083连斩(长剑专精) |
| C-009 | 2026-07-09 | 全力一击由职业终极牌替代 | 各职业终极牌 |
| C-070 | 2026-07-12 | MVP补注册，暂不启用 | — |
| C-071 | 2026-07-12 | MVP补注册，暂不启用 | — |
| C-074 | 2026-07-12 | MVP补注册，暂不启用 | — |
| C-075 | 2026-07-12 | MVP补注册，暂不启用 | — |
| C-084 | 2026-07-12 | MVP补注册，暂不启用 | — |
| C-085 | 2026-07-12 | MVP补注册，暂不启用 | — |
| C-086 | 2026-07-12 | MVP补注册，暂不启用 | — |

> 注：C-080~C-083已于2026-07-13复用为战略卡牌（GDD-CHARACTER-001 v2.0），不再废弃。

---

## 变更日志
- 2026-07-13 注册 BG-FEAT- 前缀 + BG-FEAT-001~009背景专长；复用C-080~C-083为战略卡牌；新增C-090~C-094通用卡牌（GDD-CHARACTER-001 v2.0）
- 2026-07-12 注册PROF-FEAT-/W-FEAT-/R-FEAT-前缀，补注册S-004~S-008/EQUIP-001~006/职业专长12个/武器专长6个
- 2026-07-12 注册 P-002(法师) / P-003(盗贼) / P-004(牧师)（DEC-20260712-02，来源GDD-CRAFTING-001）
- 2026-07-08 新增 TOWER- 前缀并注册 TOWER-001（GDD-TOWER-001）
- 2026-07-08 新增 POTION-/SCROLL-/WAND-/ENCH-/MAT-/WB- 前缀并注册31个新元素（GDD-CRAFTING-001）
- 2026-07-07 新增 RACE-/ORIGIN-/SKILL-/FEAT-G-/LFEAT-/PL- 前缀并注册33个新元素（GDD-CHARACTER-001）
- 2026-07-06 GDD重构：所有注册元素新增 CSV数据文件 列
- 2026-07-06 初始创建，从 GDD-COMBAT-001 提取已有元素并注册
