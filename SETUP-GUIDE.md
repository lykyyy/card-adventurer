# TRAE IDE + Obsidian 集成配置指南

## 架构总览

```
card-adventurer/                    ← TRAE IDE 打开此文件夹作为工作区
├── .trae/
│   ├── rules/                      ← 6个规则文件（alwaysApply自动注入）
│   └── skills/                     ← 18个Skill定义 + 权限总表
├── AGENTS.md                       ← 项目级AI行为引导（自动读取）
├── docs/                           ← ★ 同时是 Obsidian Vault 和 TRAE 文档集源
│   ├── .obsidian/                  ← Obsidian配置（Vault识别标记）
│   ├── MOC.md                      ← 内容地图（Obsidian导航枢纽）
│   ├── GDD/GDD-COMBAT-001.md       ← 游戏设计文档
│   ├── TDD/TDDH-COMBAT-001.md      ← 技术设计（HTML版）
│   ├── TDD/TDDG-COMBAT-001.md      ← 技术设计（Godot版）
│   ├── PDD/PDD-COMBAT-001.md       ← 程序设计文档
│   ├── memory.md                   ← 跨会话记忆
│   └── _agent-configs/             ← Agent配置参考（不加入文档集）
└── scripts/                        ← 代码目录
```

---

## 配置步骤

### 步骤1：在 TRAE IDE 中打开项目

1. 打开 TRAE IDE
2. 文件 > 打开文件夹 > 选择 `card-adventurer/`
3. 等待 TRAE IDE 完成项目索引（右下角会显示索引进度）

### 步骤2：确认规则文件生效

1. 新建一个对话
2. 输入：`你知道哪些规则文件？请列出名称和核心内容。`
3. 预期 AI 能列出全部 6 个规则：
   - maintain-pdd.md — PDD自动维护
   - no-hallucination.md — 防幻觉+8条铁律
   - review-sop.md — 五步验收SOP
   - doc-linkage.md — 文档关联规则
   - code-of-conduct.md — 八荣八耻
   - context-health.md — 上下文健康度（称呼心跳+记忆模糊检测）

如果 AI 不知道规则 → 检查 `.trae/rules/` 下每个文件第一行是否有 `alwaysApply: true`

### 步骤3：配置 TRAE 文档集（★关键）

这一步让你的 GDD/TDD/PDD 文档被 TRAE IDE 索引，对话时可以用 `#Doc` 引用。

1. 打开 TRAE IDE 设置（Ctrl+, 或 左下角齿轮）
2. 进入 **索引与文档** 设置页
3. 在 **文档集** 部分，点击 **添加文档集**
4. 选择 **从本地文件添加**
5. 选择 `card-adventurer/docs/` 目录下的所有 `.md` 文件
   - `docs/MOC.md`
   - `docs/GDD/GDD-COMBAT-001.md`
   - `docs/TDD/TDDH-COMBAT-001.md`
   - `docs/TDD/TDDG-COMBAT-001.md`
   - `docs/PDD/PDD-COMBAT-001.md`
   - `docs/memory.md`
   - **不要**添加 `docs/_agent-configs/` 下的文件（那是Agent配置参考，不是对话上下文）
6. 命名文档集为「卡牌冒险者设计文档」
7. 等待 TRAE 完成向量索引（索引完成后状态显示为"就绪"）

### 步骤4：验证文档集

1. 新建对话
2. 在输入框输入 `#` → 选择 `#Doc`
3. 选择「卡牌冒险者设计文档」
4. 输入问题：`战斗系统有哪些卡牌？列出每个卡牌的ID和数值。`
5. 预期 AI 从文档集中检索到 GDD 的卡牌列表并准确回答

### 步骤5：配置 Obsidian Vault（可选但推荐）

1. 打开 Obsidian
2. 打开其他 Vault > 打开文件夹作为 Vault
3. 选择 `card-adventurer/docs/` 文件夹
4. Obsidian 会识别 `.obsidian/` 配置并加载 Vault
5. 打开 `MOC.md` 作为首页
6. 按 Ctrl+G 打开图谱视图，查看文档间关系

### 步骤6：配置 Obsidian Local REST API（可选，用于MCP）

如果你想用 AI 通过 MCP 自动读写 Obsidian 文档：

1. 在 Obsidian 中安装 "Local REST API" 插件
2. 设置 > Local REST API > 启用
3. 记录端口号（默认 27123）和 API 密钥
4. 在 TRAE IDE 设置中配置 Obsidian MCP 连接：
   - URL: `https://127.0.0.1:27123`
   - Authorization: `Bearer {你的API密钥}`
5. 配置完成后，AI 的 obsidian-read/obsidian-write 等 Skill 就能通过 MCP 读写文档

---

## 日常使用方式

### 开发新功能时
在 TRAE IDE 对话框中输入：
```
#Doc 请实现"攻击"卡牌（C001）的出牌功能：
1. 玩家点击手牌中的"攻击"卡
2. 对敌人造成10点伤害
3. 卡牌从手牌移入弃牌堆
完成后按防幻觉规则输出自检报告。
```
`#Doc` 会自动从文档集中检索相关的 GDD/TDD/PDD 内容作为上下文。

### 精确引用某个文档时
```
#File 选择 GDD-COMBAT-001.md
#File 选择 TDDH-COMBAT-001.md
#File 选择 PDD-COMBAT-001.md

请实现"防御"卡牌（C002）的出牌逻辑。
```

### 引用整个文件夹时
```
#Folder 选择 docs/ 文件夹
请根据文档实现敌人AI决策逻辑。
```

### 防幻觉验证时
```
#File 选择 GDD-COMBAT-001.md

请为游戏添加新敌人"暗影领主"：
- HP: 200
- 攻击力: 25
实现这个敌人的战斗逻辑。
```
预期 AI 拒绝并引用禁止清单。

### 非黑箱审查时
```
#File 选择 PDD-COMBAT-001.md

不要读代码文件。只根据 PDD 回答：
1. 当前程序有哪些函数？
2. 战斗状态机有哪几个状态？
```

### 在 Obsidian 中浏览
1. 打开 `MOC.md` 查看导航
2. 点击 wikilink（如 `[[GDD-COMBAT-001]]`）跳转关联文档
3. Ctrl+G 查看图谱，了解文档间关系
4. 修改文档后，TRAE 文档集会自动更新索引

---

## 7个Agent的创建

Agent 配置文件在 `docs/_agent-configs/` 目录下，按以下顺序在 TRAE IDE Agent 管理面板创建：

1. `05-doc-engineer.md` → Agent ID: doc-engineer（L3，先创建底层）
2. `06-perf-expert.md` → Agent ID: perf-expert（L3）
3. `07-memory-keeper.md` → Agent ID: memory-keeper（L3）
4. `02-gdd-lead.md` → Agent ID: gdd-lead（L2）
5. `03-tech-lead.md` → Agent ID: tech-lead（L2）
6. `04-verify-lead.md` → Agent ID: verify-lead（L2）
7. `01-project-director.md` → Agent ID: project-director（L1，最后创建顶层）

每个 Agent 创建时：
- 将 .md 文件中 `## 完整 Prompt` 下的代码块复制到 Prompt 输入框
- 勾选 L2/L3 Agent 的"可被其他Agent调用"
- 按 `.trae/skills/skill-permissions.md` 中的权限矩阵配置 Skill 访问
