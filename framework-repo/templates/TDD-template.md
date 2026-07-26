# TDD 模板

> 每个 TDD 文件必须有唯一 ID：`TDD-{系统}-{序号}`
> 必须引用来源 GDD ID

## 模板结构

```markdown
---
id: TDD-{系统}-{序号}
title: {系统名称} 技术设计
type: tdd
source_gdd: GDD-{系统}-{序号}
related: []
version: 0.1.0
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

# {系统名称} 技术设计

## 1. 技术方案
- 技术栈：
- 架构模式：
- 关键依赖：

## 2. 模块清单
- 模块A：{职责描述}
- 模块B：{职责描述}

## 3. 接口定义
- `functionName(param1, param2)` → {返回值描述}

## 4. 数据流
- 输入 → 处理 → 输出

## 5. 性能要求
- 帧率：
- 内存：
- 加载时间：

## 变更日志
- {YYYY-MM-DD} 初始创建
```