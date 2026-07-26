# AI Game Dev Framework

模块化 AI 游戏开发工作流框架 — 可在任何游戏项目中快速部署的 AI 协作体系。

## 架构概览

```
┌──────────────────────────────────────────────────────┐
│                    L1: 统筹层                          │
│              project-director (1个)                    │
│         任务分发 · 多Agent协调 · 质量把控               │
├──────────────┬──────────────┬─────────────────────────┤
│ L2: 设计层    │ L2: 实现层    │ L2: 质量层               │
│ gdd-lead     │ tech-lead    │ verify-lead             │
│ 游戏设计      │ 技术实现      │ 系统校验                 │
├──────────────┴──────────────┼─────────────────────────┤
│         L3: 执行层           │ L3: 辅助层               │
│  writer-agent (唯一写入者)    │ doc-engineer             │
│  perf-expert                │ memory-keeper            │
└─────────────────────────────┴─────────────────────────┘
```

## 核心体系

| 体系 | 说明 | 文件 |
|------|------|------|
| **8-Agent 三权分立** | 设计权/实现权/校验权分离，writer-agent 唯一写入 | `agents/` |
| **6阶段写入流程** | 生成→预审→校核→确认→写入→校验 | `rules/write-pipeline.md` |
| **22-Skill 权限矩阵** | 每个 Agent 的技能权限精确控制 | `rules/skill-permissions.md` |
| **20+ 规则文件** | 防幻觉、ID管理、PDD维护、CSV数据管理等 | `rules/` |
| **6 校验脚本** | ID注册、格式、Schema、外键、废弃检测、别名 | `scripts/` |
| **动态数据层** | `_schema.csv` + `_foreign_keys.csv` 中央注册 | `data-layer/` |
| **模板文件** | GDD/TDD/PDD/ID-REGISTRY 等模板 | `templates/` |

## 快速开始

### 在新项目中使用

```bash
# 1. 克隆框架
git clone https://github.com/lykyyy/ai-game-dev-framework.git

# 2. 复制到新项目
cp -r ai-game-dev-framework/rules .trae/rules/
cp -r ai-game-dev-framework/agents docs/_agent-configs/
cp -r ai-game-dev-framework/scripts scripts/validation/
cp -r ai-game-dev-framework/data-layer data/csv/
cp -r ai-game-dev-framework/templates docs/templates/

# 3. 初始化数据层
# 编辑 data/csv/_schema.csv 注册你的数据文件
# 编辑 data/csv/_foreign_keys.csv 注册外键关系

# 4. 创建 AGENTS.md（引用规则索引）
# 参考 templates/AGENTS-template.md
```

### 前置要求

- TRAE IDE 或支持 `.trae/rules/` 规则注入的 IDE
- Python 3.8+（运行校验脚本）
- 理解 GDD/TDD/PDD 三层文档体系

## 规则体系

### 核心规则（P0）

| 规则 | 功能 |
|------|------|
| `collaboration-protocol.md` | 工作流铁律：讨论→批准→实施 |
| `write-pipeline.md` | 6阶段写入流程 |
| `防幻觉规则.md` | 元素清单约束 + 数值来源追溯 |
| `id-management.md` | 编号注册先于写入 |
| `pdd自动维护规则.md` | 代码变更后自动同步PDD |

### 治理规则（P1）

| 规则 | 功能 |
|------|------|
| `skill-permissions.md` | 22-Skill × 8-Agent 权限矩阵 |
| `context-verify.md` | 设计前背景设定查询 |
| `csv-data-management.md` | 动态数据层架构 |
| `文档关联规则.md` | GDD↔TDD↔PDD↔代码 绑定 |
| `tdd-generation-rules.md` | TDD 生成前 ID 校验 |
| `residual-coverage-check.md` | 5类残留覆盖检测 |
| `五步验收sop.md` | 功能完成后5步验收 |
| `编程行为准则.md` | 八荣八耻编码规范 |

### 运维规则（P2）

| 规则 | 功能 |
|------|------|
| `session-startup.md` | 新会话强制加载记忆 |
| `上下文健康度规则.md` | 心跳信号 + 记忆模糊检测 |
| `对话蒸馏规则.md` | 用户沟通画像自动提取 |
| `agent-config-consistency.md` | Agent 配置一致性校验 |
| `alias-graph-maintenance.md` | ID-ALIAS + ID-REFERENCE-GRAPH 维护 |
| `rule-index-integrity.md` | 规则索引完整性 |
| `automation-validation.md` | 自动化校验脚本规范 |

## Agent 体系

| Agent | 层级 | 职责 |
|-------|------|------|
| `project-director` | L1 | 任务分发、多Agent协调 |
| `gdd-lead` | L2 | 游戏设计、GDD维护 |
| `tech-lead` | L2 | 技术实现、TDD维护 |
| `verify-lead` | L2 | 系统校验、质量把控 |
| `writer-agent` | L3 | 唯一文件写入者 |
| `doc-engineer` | L3 | PDD格式校验 |
| `perf-expert` | L3 | 性能分析优化 |
| `memory-keeper` | L3 | 记忆管理、对话蒸馏 |

## 校验脚本

```bash
python scripts/id-registry-check.py      # ID注册状态校验
python scripts/id-format-check.py        # ID格式正则校验
python scripts/csv-schema-check.py       # CSV-Schema一致性
python scripts/foreign-key-check.py      # 外键完整性
python scripts/deprecated-id-check.py    # 废弃编号引用检测
python scripts/alias-graph-check.py      # ID-ALIAS/ID-REFERENCE-GRAPH
```

## 版本

v1.0.0 — 从 card-adventurer 项目提取，2026-07-26

## 许可

MIT