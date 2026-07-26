---
alwaysApply: true
---

# Skill权限矩阵（22 Skill × 8 Agent）

## 22 Skill × 8 Agent权限矩阵

| Skill | project-director | gdd-lead | tech-lead | verify-lead | writer-agent | doc-engineer | perf-expert | memory-keeper |
|-------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| obsidian-read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| obsidian-write | ❌ | ❌ | ❌ | ⚠️仅报告 | ✅唯一 | ❌ | ❌ | ❌ |
| obsidian-search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| file-read | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| file-write | ❌ | ❌ | ❌ | ❌ | ✅唯一 | ❌ | ❌ | ❌ |
| code-search | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| web-research | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| agent-dispatch | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| doc-management | ❌ | ❌ | ❌ | ❌ | ✅ | ⚠️格式校验 | ❌ | ❌ |
| residual-check | ❌ | ❌ | ❌ | ⚠️复审 | ✅唯一执行 | ❌ | ❌ | ❌ |
| TRAE-code-review | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| TRAE-security-review | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| TRAE-debugger | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| game-design | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| game-deconstruction | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| godot-game-development | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| godot-single-script-workflow | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| godot-code-explainer | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| generating-game-tdd-from-gdd | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| generating-game-html-from-figma | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| frontend-design | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| web-dev | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

## 权限缩写
- ✅自由：Agent可自主使用该Skill
- ⚠️需确认/部分权限：Agent在特定条件下可使用
- ❌禁止：Agent不得使用该Skill

## 最小权限原则
1. writer-agent是唯一拥有obsidian-write和file-write的Agent
2. verify-lead是唯一拥有系统校验权的Agent（residual-check由writer-agent执行预审，verify-lead执行复审）
3. project-director没有任何写入权限（仅统筹分发）
4. memory-keeper没有文件读写权限（只通过提案）

## Skill详细说明

### 1. obsidian-read
读取Obsidian库中的笔记内容。

### 2. obsidian-write
写入Obsidian库中的笔记。**唯一拥有者：writer-agent**。verify-lead仅限对话输出（校验报告不写入磁盘文件）。

### 3. obsidian-search
搜索Obsidian库中的笔记。

### 4. file-read
读取项目文件。memory-keeper禁止（不读取代码文件）。

### 5. file-write
写入项目文件。**唯一拥有者：writer-agent**。

### 6. code-search
搜索代码内容。memory-keeper禁止。

### 7. web-research
网络检索（WebSearch/WebFetch）。writer-agent和doc-engineer禁止（不参与研究）。

### 8. agent-dispatch
调度其他Agent。仅project-director/tech-lead/verify-lead可用。

### 9. doc-management
文档管理（GDD/TDD/PDD写入+格式校验）。**主要拥有者：writer-agent**。doc-engineer仅限PDD格式校验。

### 10. residual-check
残留覆盖完整性预审（5类检测）。**预审执行者：writer-agent**。verify-lead执行复审。

### 11. TRAE-code-review
代码审查任务，检查代码质量、正确性和最佳实践。

### 12. TRAE-security-review
代码安全扫描，检查安全漏洞和风险。

### 13. TRAE-debugger
运行时调试，收集日志和复现Bug。

### 14. game-design
游戏策划案编写，GDD内容生成。

### 15. game-deconstruction
游戏深度拆解与分析。

### 16. godot-game-development
Godot Engine 4.6 游戏开发。

### 17. godot-single-script-workflow
Godot单脚本增量生成工作流。

### 18. godot-code-explainer
Godot代码五维解释教学。

### 19. generating-game-tdd-from-gdd
从GDD自动生成TDD。

### 20. generating-game-html-from-figma
Figma设计转HTML原型。

### 21. frontend-design
生产级前端界面设计。

### 22. web-dev
创建Web网站/应用/游戏。

## 变更日志
- 2026-07-15 扩展权限矩阵：新增12个TRAE内置Skill的行权限定义
- 2026-07-06 从 wh40k-inquisitor 项目迁移至 card-adventurer
