# 卡牌冒险者 (Card Adventurer)

> D&D Spelljammer × Roguelike 卡牌策略游戏 | 已封存

基于 D&D 魔法船宇宙的 Roguelike 卡牌策略游戏，采用「万物皆卡牌」设计哲学。本项目已封存，同时提炼出一套**可复用的 AI 游戏开发工作流框架**。

---

## 项目状态

| 维度 | 状态 |
|------|------|
| 开发阶段 | 原型开发（已封存） |
| GDD 覆盖 | 6系统（核心/角色/战斗/双战场/制作/法师塔） |
| 编号体系 | 23前缀 · 170+元素 · 18废弃 |
| CSV 数据 | 30个数据文件 · 动态架构 v2.0 |
| 代码 | MVP 战斗原型（HTML） |

---

## AI 工作流框架（可复用）

`framework/` 目录包含从本项目中提炼的完整 AI 辅助开发工程体系，可直接部署到任何游戏项目：

```
framework/
├── rules/          # 20条规则（防幻觉/6阶段流程/权限矩阵/上下文管理...）
├── agents/         # 8个Agent配置（三权分立架构）
├── scripts/        # 6个Python自动化校验脚本
├── templates/      # GDD/TDD/PDD/memory/AGENTS 模板
└── data-layer/     # CSV动态架构模板（_schema.csv + _foreign_keys.csv）
```

[→ 框架详细文档](framework/README.md)

### 快速部署

```bash
# 复制规则到新项目
cp -r framework/rules/* 新项目/.trae/rules/
cp -r framework/agents/* 新项目/docs/_agent-configs/
cp -r framework/scripts/* 新项目/scripts/validation/
cp -r framework/templates/* 新项目/docs/
cp -r framework/data-layer/* 新项目/data/csv/
```

---

## 项目结构

```
card-adventurer/
├── framework/              # ★ 可复用AI工作流框架
├── AGENTS.md               # 总纲（8Agent + 规则索引）
├── .trae/rules/            # 20条自动注入规则
├── .changelog.md           # 项目级变更日志
│
├── docs/
│   ├── GDD/                # 游戏设计文档（6系统）
│   │   ├── GDD-CORE-001.md        # 核心玩法架构
│   │   ├── GDD-CHARACTER-001.md   # 角色系统
│   │   ├── GDD-BATTLEFIELD-001.md # 双战场战斗
│   │   ├── GDD-CRAFTING-001.md    # 制作附魔
│   │   ├── GDD-TOWER-001.md       # 法师塔
│   │   ├── ID-REGISTRY.md         # 中央编号注册表
│   │   └── GDD-INDEX.md           # GDD索引
│   ├── TDD/                # 技术设计文档
│   ├── PDD/                # 程序文档
│   ├── _agent-configs/     # Agent配置文件
│   ├── memory.md           # 跨会话记忆
│   ├── improvement-log.md  # 改进追踪
│   └── MOC.md              # 内容地图
│
├── data/csv/               # CSV数据层（30文件）
│   ├── _schema.csv         # 中央元数据注册表
│   ├── _foreign_keys.csv   # 外键关系表
│   ├── cards.csv           # 卡牌数据
│   ├── professions.csv     # 职业数据
│   └── ...
│
└── scripts/
    ├── validation/         # 6个自动化校验脚本
    └── mvp-battle.html     # 战斗MVP原型
```

---

## 核心设计决策

- **三层玩法**：L1地图(AP) → L2网格(EP·5×5翻牌) → L3战斗(CE+职业能量)
- **四职业**：战士(怒气) · 盗贼(连击点) · 法师(法力值) · 牧师(法力值)
- **三文档体系**：GDD（设计意图）→ TDD（技术方案）→ PDD（当前实现）
- **万物皆卡牌**：装备/同伴/事件/地点/资源/技能/敌人 → 统一卡牌格式
- **参考游戏**：《欺诈之地》《命运之手2》《杀戮尖塔》

---

## 工程体系亮点

- **6阶段写入流程**：生成→残留预审→系统校核→人工确认→写入→事后校验
- **三权分立**：提案权 / 校验权 / 写入权 分离，防 AI 幻觉
- **8条防幻觉铁律**：元素清单+ID注册表+数值追溯+禁止清单
- **CSV动态架构**：`_schema.csv` 中央注册 + `_foreign_keys.csv` 外键管理
- **上下文健康度**：称呼心跳 + 三级警报 + 对话蒸馏

---

## 变更日志

参见 [.changelog.md](.changelog.md)