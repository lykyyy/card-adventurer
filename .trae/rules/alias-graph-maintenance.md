---
alwaysApply: true
---

# ID-ALIAS与ID-REFERENCE-GRAPH维护规则

## 核心原则
ID-ALIAS.md和ID-REFERENCE-GRAPH.md是残留覆盖预审的基础设施，必须随ID变更同步维护。

## 强制维护规则

### ID-ALIAS.md维护
每次ID变更时，必须同步更新ID-ALIAS.md：
1. **新增ID**：无需更新别名表
2. **废弃ID**：必须在ID-ALIAS.md记录旧编号→新编号（替代编号）的映射
3. **重命名ID**：必须在ID-ALIAS.md记录旧编号→新编号的映射
4. **合并ID**：必须在ID-ALIAS.md记录被合并编号→目标编号的映射

### ID-REFERENCE-GRAPH.md维护
每次ID变更或新增前缀时，必须同步更新ID-REFERENCE-GRAPH.md：
1. **新增前缀**：必须记录新前缀的跨系统引用关系
2. **新增ID**：必须记录该ID在哪些系统/文件中被引用
3. **废弃ID**：必须更新引用该ID的所有系统/文件
4. **跨系统引用变更**：必须更新引用图

## 维护流程
1. ID-REGISTRY.md变更时，同步检查ID-ALIAS.md
2. ID-REGISTRY.md变更时，同步检查ID-REFERENCE-GRAPH.md
3. 每周执行一次ID-ALIAS和ID-REFERENCE-GRAPH完整性审计
4. 审计结果记录在变更日志中

## 完整性校验
- ID-ALIAS.md：每个废弃编号必须有对应的别名映射
- ID-REFERENCE-GRAPH.md：每个注册前缀必须有跨系统引用记录

## 禁止事项
| 禁止 | 说明 |
|------|------|
| ❌ 废弃ID不记录别名 | 废弃ID必须在ID-ALIAS.md记录替代编号 |
| ❌ 新增前缀不更新引用图 | 新增前缀必须在ID-REFERENCE-GRAPH.md记录 |
| ❌ ID-ALIAS为空 | ID-ALIAS.md必须维护，不得为空 |

## 变更日志
- 2026-07-12 初始创建
