---
alwaysApply: true
---

# 自动化校验工具规则

## 核心原则
项目必须提供自动化校验工具，确保规则从"文档型"升级为"执行型"。

## 必须提供的校验脚本

| 脚本名 | 校验内容 | 实现优先级 |
|--------|----------|----------|
| id-registry-check.py | ID-REGISTRY注册状态校验 | P0 |
| id-format-check.py | ID格式正则校验（`^[A-Z]+(-[0-9]+)+$`） | P0 |
| csv-schema-check.py | CSV-Schema一致性校验 | P0 |
| foreign-key-check.py | 外键完整性校验 | P1 |
| deprecated-id-check.py | 废弃编号引用检测 | P1 |
| tdd-pdd-coverage.py | TDD/PDD覆盖完整性校验 | P1 |
| version-sync-check.py | 版本号同步校验 | P2 |
| alias-graph-check.py | ID-ALIAS/ID-REFERENCE-GRAPH完整性校验 | P2 |

## 脚本位置
`scripts/validation/`

## 执行时机
1. **Git pre-commit hook**：每次提交前执行所有校验脚本
2. **手动执行**：用户可随时执行校验
3. **verify-lead调用**：verify-lead在校验时可调用这些脚本

## 校验报告格式
```
## 自动化校验报告
- 执行时间：{日期时间}
- 执行脚本：{脚本列表}
- 校验结果：
  - {脚本名}：✅通过 / ❌{N}个错误
  - {错误清单：文件:行号 + 问题描述}
- 总结：{N}个脚本通过 / {N}个脚本失败
```

## 失败处理
- 校验脚本失败时，必须修正后才能提交
- 校验报告必须记录在变更日志中

## 变更日志
- 2026-07-12 初始创建
