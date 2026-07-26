# IDE 操作方案 C：TRAE + Obsidian MCP 全自动方案

> **执行方式**：在 TRAE IDE 中打开本文件，对 AI 说"请执行这个操作方案"。
>
> **方案定位**：最完整方案。TRAE IDE 负责 AI 交互和代码开发，Obsidian 负责文档管理，Obsidian Local REST API 让 AI 通过 MCP 编程式读写文档。18 个 Skill 全部激活。适合追求全自动化工作流的用户。
>
> **与方案B的关系**：本方案包含方案B的全部内容，并增加 Obsidian Local REST API + MCP 连接配置。4 个 Obsidian Skill 从"半激活"升级为"完全激活"。

---

## 前置条件

- 已安装 TRAE IDE
- 已安装 Obsidian（https://obsidian.md）
- Obsidian 社区插件中可安装 "Local REST API" 插件

## 架构总览

```
card-adventurer/
├── .trae/
│   ├── rules/                      ← 6个规则（alwaysApply 自动注入）
│   └── skills/                     ← 18个Skill（全部活跃）+ 权限总表
├── AGENTS.md                       ← 项目级AI行为引导
├── docs/                           ← Obsidian Vault + TRAE文档集 + MCP读写目标
│   ├── .obsidian/                  ← Obsidian配置
│   ├── MOC.md                      ← wikilink导航枢纽
│   ├── GDD/GDD-COMBAT-001.md
│   ├── TDD/TDDH-COMBAT-001.md
│   ├── TDD/TDDG-COMBAT-001.md
│   ├── PDD/PDD-COMBAT-001.md
│   ├── memory.md
│   └── _agent-configs/
└── scripts/
```

**方案C数据流**：
```
人工 ──→ Obsidian编辑文档 ──→ docs/*.md ──→ TRAE #Doc语义检索
                                    ↕
AI ←── MCP读写 ←── Obsidian REST API ←── docs/*.md
```

**方案C与方案B的差异**：
| 差异项 | 方案B | 方案C |
|--------|-------|-------|
| Obsidian Local REST API | 未安装 | 已安装并启用 |
| TRAE MCP 连接 | 无 | 已配置 |
| obsidian-read Skill | 半激活 | 完全活跃（MCP自动调用） |
| obsidian-write Skill | 半激活 | 完全活跃（MCP自动调用，需确认） |
| obsidian-search Skill | 半激活 | 完全活跃（MCP自动调用） |
| obsidian-verify-links | 半激活 | 完全活跃（MCP自动调用） |
| AI 编程式读写文档 | 不能 | 能 |
| 自动记忆更新 | 不能 | 能 |
| 自动文档校验 | 需手动触发 | 可自动触发 |

---

## 步骤 1-5：创建项目结构、规则、Agent、Skill、文档

> **以下内容与方案B完全相同：**
> - 步骤1：创建目录结构（同方案B）
> - 步骤2：创建6个规则文件（同方案A/B，含context-health.md）
> - 步骤3：创建AGENTS.md（同方案B，含Obsidian集成说明）
> - 步骤4：创建7个Agent（同方案A/B）
> - 步骤5：创建18个Skill目录（同方案B结构）
> - 步骤6：创建Obsidian配置文件（同方案B）
> - 步骤7：创建6个文档文件（同方案B，wikilink版）
>
> 请按方案B的步骤1-7完成以上所有内容的创建。

---

## 步骤 5-补充：更新 4 个 Obsidian Skill 为完全激活版 ★方案C核心

在方案B基础上，将 4 个 obsidian-* Skill 的 SKILL.md 更新为完全激活版本（包含 MCP 调用细节）：

### 文件：`.trae/skills/obsidian-read/SKILL.md`（完全激活版）

```markdown
---
name: obsidian-read
description: "通过 Obsidian Local REST API 读取知识库中的笔记内容。当需要查看 GDD/TDD/PDD/记忆文档时激活。"
user-invocable: false
disable-model-invocation: false
---

# Obsidian 读取 Skill

## 功能说明
通过 Obsidian Local REST API 读取知识库中的笔记内容，支持按文件名读取和按 ID 定位。

## 使用场景
- 编码前读取 GDD 元素清单和禁止清单
- 设计前读取现有 TDD 技术方案
- 审查时读取 PDD 函数清单
- 任何需要获取文档内容的场景

## 调用方式（MCP）
通过 Obsidian MCP 工具读取笔记：
1. 按文件路径读取：`GET /vault/{path}` — 获取指定路径的笔记内容
2. 按 ID 定位读取：先搜索 frontmatter 中的 `id` 字段，再读取对应文件

## 输入参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file_path | string | 是 | 笔记在 vault 中的相对路径，如 `docs/GDD/GDD-COMBAT-001.md` |
| note_id | string | 否 | 笔记的 frontmatter ID，如 `GDD-COMBAT-001` |

## 输出格式
返回笔记的完整 Markdown 内容，包括 frontmatter 元数据和正文。

## 使用规则
1. 读取后必须记录文档 ID 和版本号，用于后续引用
2. 如果文档不存在，明确报告"文档 XXX 不存在"，不得编造内容
3. 读取的内容必须原样引用，不得篡改或"补全"
4. 每次读取后在输出末尾记录：`[工具调用] obsidian-read: {file_path}`

## 配套 Agent
| Agent | 权限 |
|-------|------|
| 全部 Agent | ✅ 自由调用 |

## MCP 配置要求
- Obsidian 已安装 Local REST API 插件并启用
- 端口：27123（默认）
- API 密钥已配置到 TRAE IDE MCP 连接中
- Vault 路径：项目目录下的 `docs/` 文件夹
```

### 文件：`.trae/skills/obsidian-write/SKILL.md`（完全激活版）

```markdown
---
name: obsidian-write
description: "通过 Obsidian Local REST API 写入/修改知识库中的笔记。需人工确认。"
user-invocable: false
disable-model-invocation: false
---

# Obsidian 写入 Skill

## 功能说明
通过 Obsidian Local REST API 写入或修改知识库中的笔记内容。

## 使用场景
- gdd-lead 创建/修改 GDD 文档
- tech-lead 创建/修改 TDD 文档
- tech-lead 维护 PDD 文档（maintain-pdd 规则触发）
- memory-keeper 更新记忆文档
- verify-lead 更新文档验证标记

## 调用方式（MCP）
1. 写入笔记：`PUT /vault/{path}` — 创建或覆盖笔记
2. 追加内容：`POST /vault/{path}` — 在笔记末尾追加内容
3. 修改内容：先读取原文件，修改后写入完整内容

## 使用规则
1. **写入前必须先读取原文件**（铁律3：禁止局部覆盖导致信息丢失）
2. 写入前必须展示修改范围，等待人工确认
3. 写入后必须验证内容已正确保存
4. 每次写入后在输出末尾记录：`[工具调用] obsidian-write: {file_path}`

## 配套 Agent
| Agent | 权限 |
|-------|------|
| project-director | ❌ 禁止 |
| gdd-lead | ⚠️ 需确认（仅GDD） |
| tech-lead | ⚠️ 需确认（仅TDD/PDD） |
| verify-lead | ⚠️ 需确认（仅验证标记） |
| doc-engineer | ⚠️ 需确认（仅PDD格式修正） |
| perf-expert | ❌ 禁止 |
| memory-keeper | ⚠️ 需确认（仅memory.md） |
```

### 文件：`.trae/skills/obsidian-search/SKILL.md`（完全激活版）

```markdown
---
name: obsidian-search
description: "通过 Obsidian Local REST API 语义检索知识库笔记。"
user-invocable: false
disable-model-invocation: false
---

# Obsidian 检索 Skill

## 功能说明
通过 Obsidian Local REST API 检索知识库中的笔记内容，支持全文搜索和标签过滤。

## 调用方式（MCP）
1. 全文搜索：`POST /search/simple/` — 按关键词搜索
2. 按标签搜索：`GET /search/{tag}` — 按标签过滤

## 使用场景
- 查找包含特定关键词的文档
- 按 GDD/TDD/PDD 标签过滤文档
- 查找引用了某个 ID 的所有文档

## 配套 Agent
| Agent | 权限 |
|-------|------|
| 全部 Agent | ✅ 自由调用 |
```

### 文件：`.trae/skills/obsidian-verify-links/SKILL.md`（完全激活版）

```markdown
---
name: obsidian-verify-links
description: "通过 Obsidian Local REST API 校验文档间的 wikilink 双向链接完整性。"
user-invocable: false
disable-model-invocation: false
---

# Obsidian 链接校验 Skill

## 功能说明
扫描知识库中所有 wikilink，检查双向链接是否完整，标记断链和缺失链接。

## 校验流程
1. 读取所有文档
2. 提取所有 wikilink（如 `[[GDD-COMBAT-001]]`）
3. 检查每个 wikilink 目标是否存在
4. 检查反向链接是否已建立
5. 输出校验报告

## 使用场景
- verify-lead 执行四层校验中的"绑定校验"
- 新增文档后检查链接完整性
- 文档删除后检查是否有断链

## 配套 Agent
| Agent | 权限 |
|-------|------|
| verify-lead | ✅ 核心使用场景 |
| project-director | ✅ |
| tech-lead | ✅ |
| doc-engineer | ✅ |
```

### Skill 权限总表更新

将 `.trae/skills/skill-permissions.md` 中 4 个 Obsidian Skill 的状态从"半激活"改为"活跃"：

```markdown
| # | Skill 名称 | 分类 | 功能 | 方案C状态 |
|---|-----------|------|------|-----------|
| 1 | obsidian-read | Obsidian MCP | 读取笔记 | 活跃（MCP） |
| 2 | obsidian-write | Obsidian MCP | 写入笔记 | 活跃（MCP，需确认） |
| 3 | obsidian-search | Obsidian MCP | 检索笔记 | 活跃（MCP） |
| 4 | obsidian-verify-links | Obsidian MCP | 校验链接 | 活跃（MCP） |
| 5-18 | （同方案A/B） | 各分类 | 同方案A | 活跃 |

## 方案C说明
- 全部 18 个 Skill 活跃
- Obsidian Skill 通过 MCP 自动调用
- AI 可编程式读写文档
- 配合规则文件实现自动记忆、自动校验
```

---

## 步骤 8：配置 TRAE 文档集

> 同方案B步骤8。

1. TRAE IDE 设置 > 索引与文档
2. 添加 docs/ 下 6 个 .md 文件为文档集
3. 命名「卡牌冒险者设计文档」
4. 等待索引完成

---

## 步骤 9：配置 Obsidian Vault

> 同方案B步骤9。

1. Obsidian > 打开其他 Vault > 打开文件夹作为 Vault
2. 选择 `card-adventurer/docs/`
3. 打开 MOC.md 作为首页
4. Ctrl+G 查看图谱

---

## 步骤 10：安装 Obsidian Local REST API 插件 ★方案C核心步骤

1. 打开 Obsidian > 设置 > 第三方插件
2. 关闭"安全模式"
3. 点击"浏览" > 搜索 "Local REST API"
4. 安装并启用
5. 进入 Local REST API 插件设置：
   - 确认端口号（默认 27123）
   - 复制 API 密钥（一长串字符）
   - 确认 HTTPS 证书已生成（插件自动生成自签名证书）

### 验证 REST API 可用

在终端执行：
```bash
curl -k -H "Authorization: Bearer 你的API密钥" https://127.0.0.1:27123/
```
预期返回 Obsidian Vault 信息。

---

## 步骤 11：配置 TRAE IDE MCP 连接 ★方案C核心步骤

1. 打开 TRAE IDE 设置
2. 进入 **MCP** 或 **工具连接** 设置页
3. 添加 MCP 连接，配置如下：
   - **名称**：Obsidian Local REST API
   - **URL**：`https://127.0.0.1:27123`
   - **Authorization**：`Bearer {你的API密钥}`
   - **协议**：HTTPS（接受自签名证书）
4. 保存并测试连接
5. 连接成功后，4 个 obsidian-* Skill 自动激活

### MCP 连接验证

在 TRAE IDE 对话框中输入：
```
请通过 Obsidian MCP 读取 GDD-COMBAT-001 文档的前10行。
```
预期 AI 通过 MCP 调用 `obsidian-read` Skill，返回 GDD 文档内容。

---

## 步骤 12：验证清单

| # | 验证项 | 方法 | 预期结果 |
|---|--------|------|----------|
| 1 | 规则文件生效 | 问"你知道哪些规则？" | AI列出6个规则 |
| 2 | 文档集可用 | `#Doc` | 列出文档集 |
| 3 | 语义检索 | `#Doc 战斗系统有哪些卡牌？` | AI检索到6张卡牌 |
| 4 | 防幻觉防线 | `#File GDD 添加暗影领主` | AI拒绝 |
| 5 | Obsidian Vault | Obsidian打开docs/ | 成功加载 |
| 6 | wikilink跳转 | 点击[[GDD-COMBAT-001]] | 跳转 |
| 7 | 图谱视图 | Ctrl+G | 显示关系网络 |
| 8 | REST API可用 | curl测试 | 返回Vault信息 |
| 9 | MCP连接 | AI通过MCP读取GDD | 返回文档内容 |
| 10 | MCP写入 | AI通过MCP更新memory.md | 写入成功 |
| 11 | Agent可用 | Agent面板 | 7个Agent存在 |
| 12 | 全Skill活跃 | 检查skill-permissions.md | 18个全部活跃 |

---

## 方案C高级工作流 ★方案C独有

### 工作流1：AI 自动读写文档（MCP驱动）

```
#Doc 请实现"攻击"卡牌（C001）的出牌功能。
AI 将：
1. 通过 #Doc 检索 GDD/TDD/PDD 相关内容
2. 通过 MCP（obsidian-read）读取 GDD 元素清单
3. 编写代码
4. 通过 MCP（obsidian-write）更新 PDD 文档
5. 通过 MCP（obsidian-verify-links）检查文档关联
6. 输出自检报告
```

### 工作流2：自动记忆更新

```
会话结束时，memory-keeper Agent 自动：
1. 通过 MCP 读取 docs/memory.md
2. 提取本次会话的关键信息（幻觉、决策、教训）
3. 通过 MCP 追加到 memory.md
4. 下次会话开始时自动读取并提供历史经验
```

### 工作流3：自动文档校验

```
verify-lead Agent 可自动：
1. 通过 MCP 读取全部 GDD/TDD/PDD
2. 通过 MCP（obsidian-verify-links）检查双向链接
3. 通过 MCP（obsidian-search）搜索断链
4. 输出一致性校验报告
5. 通过 MCP 更新文档验证标记
```

### 工作流4：AI 直接修改文档（需确认）

```
@gdd-lead 请为战斗系统新增"防御姿态"状态效果。
gdd-lead 将：
1. 通过 MCP 读取 GDD-COMBAT-001.md
2. 在元素清单中添加 S002 防御姿态
3. 从禁止清单中移除（如果存在）
4. 通过 MCP 写入修改后的 GDD（展示修改范围，等待确认）
5. 确认后通过 MCP 检查关联的 TDD/PDD 是否需要更新
```

---

## 日常使用示例

### MCP 增强版功能开发
```
#Doc 请实现"攻击"卡牌（C001）的出牌功能：
1. 玩家点击手牌中的"攻击"卡
2. 对敌人造成10点伤害
3. 卡牌从手牌移入弃牌堆
完成后：
- 通过 MCP 更新 PDD
- 通过 MCP 校验文档关联
- 输出自检报告
```

### MCP 驱动的非黑箱审查
```
请通过 MCP 读取 PDD-COMBAT-001.md，
不读代码文件，只根据 PDD 回答：
1. 当前程序有哪些函数？
2. 战斗状态机有哪几个状态？
```

### MCP 驱动的防幻觉校验
```
@verify-lead 请通过 MCP 执行防幻觉校验：
1. 读取 GDD 元素清单
2. 读取全部代码
3. 比对元素一致性
4. 通过 MCP 更新校验报告
```

---

## 方案对比总览

| 维度 | 方案A | 方案B | 方案C |
|------|-------|-------|-------|
| TRAE IDE | ✅ | ✅ | ✅ |
| 规则文件 | ✅ 5个 | ✅ 5个 | ✅ 5个 |
| Agent团队 | ✅ 7个 | ✅ 7个 | ✅ 7个 |
| Skill定义 | ✅ 18个 | ✅ 18个 | ✅ 18个 |
| TRAE文档集 | ✅ | ✅ | ✅ |
| Obsidian Vault | ❌ | ✅ | ✅ |
| wikilink跳转 | ❌ | ✅ | ✅ |
| 图谱视图 | ❌ | ✅ | ✅ |
| Obsidian Skill | 预留 | 半激活 | 完全活跃 |
| MCP连接 | ❌ | ❌ | ✅ |
| AI编程式读写 | ❌ | ❌ | ✅ |
| 自动记忆 | ❌ | ❌ | ✅ |
| 自动校验 | ❌ | ❌ | ✅ |
| 前置依赖 | 仅TRAE | TRAE+Obsidian | TRAE+Obsidian+REST API |
| 搭建难度 | 低 | 中 | 高 |
| 自动化程度 | 低 | 中 | 高 |

### 推荐选择
- **快速启动 / 初学者** → 方案A
- **需要可视化文档管理** → 方案B
- **追求全自动化工作流** → 方案C
