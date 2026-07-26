---
alwaysApply: true
---

# Agent配置一致性规则

## 核心原则
Agent配置文件必须与skill-permissions.md权限矩阵和AGENTS.md定义保持一致。

## 强制规则
1. Agent配置文件中的权限声明必须与skill-permissions.md权限矩阵一致
2. Agent配置文件中的职责定义必须与AGENTS.md中的SOUL/ROLE定义一致
3. Agent配置文件必须包含6阶段写入流程的引用（不得跳过流程）
4. 每个Agent必须有对应的配置文件（_agent-configs/目录）

## 配置文件规范
- 位置：`docs/_agent-configs/{编号}-{agent名}.md`
- 格式：frontmatter（id/level/role/priority）+ 角色定位 + 核心职责 + 工作流程 + 完整Prompt
- 必须引用6阶段写入流程（write-pipeline.md）
- 必须明确权限边界（自主放行/人工确认后启用/永久禁止）

## 一致性校验
每次修改Agent配置文件时，必须校验：
1. 配置文件声称的权限是否与skill-permissions.md一致
2. 配置文件声称的职责是否与AGENTS.md一致
3. 配置文件是否引用6阶段写入流程
4. 配置文件是否包含权限边界声明

## 禁止事项
| 禁止 | 说明 |
|------|------|
| ❌ 配置文件声称直接写入 | 除writer-agent外，所有Agent配置不得声称直接写入 |
| ❌ 配置文件跳过6阶段流程 | 所有Agent配置必须引用6阶段写入流程 |
| ❌ 配置文件与权限矩阵矛盾 | 配置文件权限声明必须与skill-permissions.md一致 |

## 变更日志
- 2026-07-12 初始创建
