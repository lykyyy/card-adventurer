# AI 游戏开发工作流框架 v1.0

> 模块化、可移植的 AI 辅助游戏开发工程体系。从「卡牌冒险者」项目提炼，可部署到任何游戏项目。

---

## 框架概述

本框架提供一套完整的 AI Agent 协作工作流，覆盖游戏开发的**设计→编码→校验→文档→记忆**全链路。核心特征：

- **三权分立**：提案权 / 校验权 / 写入权 分离，防 AI 幻觉
- **6阶段写入流程**：生成→残留预审→系统校核→人工确认→写入→事后校验
- **8 Agent 三层架构**：L1 统筹 → L2 设计/技术/校验/写入 → L3 文档/性能/记忆
- **22 Skill 权限矩阵**：精确控制每个 Agent 的工具使用权限
- **CSV 动态数据架构**：`_schema.csv` 中央注册表 + `_foreign_keys.csv` 外键管理
- **自动化校验**：6个 Python 脚本（ID格式/CSV Schema/外键/废弃编号/别名图）
- **上下文健康度**：称呼心跳 + 三级警报 + 对话蒸馏

---

## 目录结构

```
framework/
├── README.md                    # 本文件
├── rules/                       # 20条规则文件（直接复制到新项目 .trae/rules/）
│   ├── collaboration-protocol.md    # 协作协议（最高优先级）
│   ├── 防幻觉规则.md                 # 8条防幻觉铁律
│   ├── write-pipeline.md            # 6阶段写入流程
│   ├── residual-coverage-check.md   # 5类残留检测
│   ├── context-verify.md            # 设计前背景验证
│   ├── skill-permissions.md         # 22 Skill × 8 Agent 权限矩阵
│   ├── id-management.md             # 编号管理规则
│   ├── csv-data-management.md       # CSV动态架构v2.0
│   ├── pdd自动维护规则.md            # PDD自动更新触发
│   ├── 文档关联规则id绑定要求.md      # GDD↔TDD↔PDD链
│   ├── 五步验收sop.md                # 5步验收标准流程
│   ├── agent-config-consistency.md   # Agent配置一致性
│   ├── alias-graph-maintenance.md    # ID别名与引用图维护
│   ├── automation-validation.md      # 自动化校验工具规范
│   ├── rule-index-integrity.md       # 规则索引完整性
│   ├── session-startup.md            # 会话启动强制读取
│   ├── 上下文健康度规则.md            # 称呼心跳+记忆模糊检测
│   ├── 对话蒸馏规则.md               # 自动提取用户画像
│   ├── 编程行为准则 — 八荣八耻.md     # 8条编程准则
│   ├── tdd-generation-rules.md       # TDD生成规范
│   └── ...                          # 其他规则
│
├── agents/                      # 8个Agent配置文件（复制到 docs/_agent-configs/）
│   ├── 01-project-director.md
│   ├── 02-gdd-lead.md
│   ├── 03-tech-lead.md
│   ├── 04-verify-lead.md
│   ├── 05-doc-engineer.md
│   ├── 06-perf-expert.md
│   ├── 07-memory-keeper.md
│   └── 08-writer-agent.md
│
├── scripts/                     # 6个自动化校验脚本（复制到 scripts/validation/）
│   ├── id-format-check.py
│   ├── csv-schema-check.py
│   ├── id-registry-check.py
│   ├── foreign-key-check.py
│   ├── deprecated-id-check.py
│   └── alias-graph-check.py
│
├── templates/                   # 项目模板文件
│   ├── AGENTS-template.md           # AGENTS.md 总纲模板
│   ├── GDD-template.md              # GDD 设计文档模板
│   ├── TDD-HTML-template.md         # HTML TDD 模板
│   ├── TDD-Godot-template.md        # Godot TDD 模板
│   ├── PDD-template.md              # PDD 程序文档模板
│   └── memory-template.md           # 跨会话记忆模板
│
└── data-layer/                  # 数据管理模板
    ├── _schema.csv                   # 中央元数据注册表模板
    └── _foreign_keys.csv             # 跨文件外键关系表模板
```

---

## 快速部署（3步）

### 步骤1：复制框架文件到新项目

```bash
# 复制规则（如果你的 IDE 是 TRAE）
cp -r framework/rules/* 新项目/.trae/rules/

# 复制 Agent 配置
cp -r framework/agents/* 新项目/docs/_agent-configs/

# 复制校验脚本
cp -r framework/scripts/* 新项目/scripts/validation/

# 复制模板
cp -r framework/templates/* 新项目/docs/

# 复制数据管理模板
cp -r framework/data-layer/* 新项目/data/csv/
```

### 步骤2：修改项目锚点

以下文件需要替换为新项目内容：

| 文件 | 修改内容 |
|------|----------|
| `AGENTS.md` | 项目概述、GDD索引、禁止清单（用 AGENTS-template.md 填充） |
| `防幻觉规则.md` | 元素清单引用、禁止清单 |
| `ID-REGISTRY.md` | 编号前缀定义（如 `C-`→`ITEM-`, `E-`→`ENEMY-`） |
| `_schema.csv` | 按新项目系统注册CSV文件 |
| `context-verify.md` | 背景设定查询路径 |
| `上下文健康度规则.md` | 称呼设置 |

### 步骤3：创建第一个 GDD → TDD → PDD 链

1. 创建 `docs/GDD/GDD-INDEX.md` 索引
2. 创建 `docs/GDD/ID-REGISTRY.md` 编号注册表
3. 创建第一个 GDD 文档 → 生成 TDD → 生成 PDD
4. 运行 `python scripts/validation/id-format-check.py` 验证

---

## Agent 架构速览

```
L1: project-director（统筹分发·不写代码/文档）
    │
    ├── L2: gdd-lead       → GDD修改提案
    ├── L2: tech-lead      → TDD + 代码提案
    ├── L2: verify-lead    → 唯一校验者（不生成内容）
    ├── L2: writer-agent   → 唯一写入者（不决策）
    │
    ├── L3: doc-engineer   → PDD格式校验
    ├── L3: perf-expert    → 性能优化
    └── L3: memory-keeper  → 跨会话经验沉淀
```

### 三权分立

| 权力 | 拥有者 | 边界 |
|------|--------|------|
| 提案权 | gdd-lead / tech-lead / doc-engineer / perf-expert / memory-keeper | 生成提案，不直接写入 |
| 校验权 | verify-lead（唯一） | 不生成内容，只检查 |
| 写入权 | writer-agent（唯一） | 不决策，只执行校验通过+人工确认的写入 |

---

## 6阶段写入流程

```
阶段1: 生成（提案者）
  → 阶段2: 残留覆盖预审（writer-agent·5类检测）
    → 阶段3: 系统校核（verify-lead）
      → 阶段4: 人工确认（用户·执行/修改/不改）
        → 阶段5: 写入（writer-agent·Edit+Read验证）
          → 阶段6: 事后校验（verify-lead·最终复审）
```

---

## 校验脚本

| 脚本 | 功能 | 优先级 |
|------|------|--------|
| `id-format-check.py` | ID格式正则校验 | P0 |
| `csv-schema-check.py` | CSV-Schema一致性 | P0 |
| `id-registry-check.py` | ID注册状态校验 | P1 |
| `foreign-key-check.py` | 外键完整性 | P1 |
| `deprecated-id-check.py` | 废弃编号引用检测 | P1 |
| `alias-graph-check.py` | ID-ALIAS/ID-REFERENCE-GRAPH完整性 | P2 |

所有脚本从项目根目录运行，输出统一格式报告。

---

## 适配不同 IDE

本框架当前基于 TRAE IDE 的规则系统（`.trae/rules/` 自动注入）。适配其他 IDE：

| IDE | 规则加载方式 | 适配方法 |
|-----|-------------|----------|
| TRAE | `.trae/rules/` 自动注入 | 直接复制（无需修改） |
| Cursor | `.cursorrules` 单文件 | 合并所有规则到 `.cursorrules` |
| Windsurf | `.windsurfrules` | 合并关键规则到 `.windsurfrules` |
| Claude Code | `CLAUDE.md` | 合并到 `CLAUDE.md` |
| 通用 CLI | 手动加载 | 粘贴规则到系统提示词 |

---

## 从卡牌冒险者项目中学习

完整参考项目位于本仓库根目录：
- `docs/GDD/` — 6个系统的完整GDD设计文档
- `docs/TDD/` — TDD技术设计文档
- `docs/PDD/` — PDD程序文档
- `data/csv/` — 30个CSV数据文件（含完整数据）
- `docs/参考/` — D&D 参考材料（已从Git排除，仅本地保留）
- `.changelog.md` — 全项目变更日志
- `docs/memory.md` — 跨会话经验记录

---

## 变更日志

| 日期 | 内容 |
|------|------|
| 2026-07-15 | v1.0 从「卡牌冒险者」项目提炼，打包为独立框架 |