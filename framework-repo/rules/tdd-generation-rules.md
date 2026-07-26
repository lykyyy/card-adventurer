---
alwaysApply: true
---

# TDD生成规则（HTML/Godot）

## 1. TDD生成前ID校验约束

### 强制规则
1. 生成HTML/Godot TDD前，必须先Read ID-REGISTRY.md，提取所有注册ID
2. TDD中引用的任何ID必须在ID-REGISTRY中存在
3. 若引用未注册ID，立即停止生成并向人工报告
4. TDD生成完成后，verify-lead必须校验TDD中所有ID引用的合法性

### 校验流程
1. Read ID-REGISTRY.md，提取注册ID清单
2. 生成TDD草稿
3. Grep TDD中所有ID引用（C-/E-/P-/S-/ITEM-/EQUIP-等，按项目实际前缀）
4. 逐ID比对ID-REGISTRY
5. 发现未注册ID：停止生成，向人工报告
6. 全部合法：提交verify-lead独立审查

### HTML TDD特殊规则
- HTML原型中的卡牌ID必须来自ID-REGISTRY
- HTML原型中的元素ID必须使用注册编号
- HTML原型中的资源ID必须使用注册编号

### Godot TDD特殊规则
- Godot脚本中的卡牌定义必须引用ID-REGISTRY注册的编号
- Godot脚本中的资源加载必须使用注册编号
- Godot脚本中的数据必须使用注册编号

## 2. TDD行数限制
- 每个TDD文件 ≤ 300行
- 超限必须按模块拆分

## 3. TDD格式规范
- 每个TDD文件必须包含frontmatter（id/title/type/source/related）
- 必须引用来源GDD ID
- 必须包含模块清单和接口定义

## 变更日志
- 2026-07-06 从 wh40k-inquisitor 项目迁移至 card-adventurer（已通用化ID前缀）
