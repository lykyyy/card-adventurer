---
tags: [MOC, navigation]
date: 2026-07-06
---

# 卡牌冒险者 — 内容地图（MOC）

> 本文件是项目的导航枢纽，所有文档通过 wikilink 关联，形成知识网络。

---

## 📁 文档体系

### 设计文档（GDD）
- [[GDD/GDD-INDEX]] — GDD 系统索引（全局禁止清单）
- [[GDD/GDD-COMBAT-001]] — 战斗系统设计
- [[GDD/GDD-template]] — GDD文档模板
- [[GDD/GDD-CORE-001]] — 核心玩法架构（三层玩法·资源体系）
- [[GDD/GDD-CHARACTER-001]] — 角色系统设计（三阶段10步创建）
- [[GDD/GDD-BATTLEFIELD-001]] — 双战场战斗系统
- [[GDD/GDD-CRAFTING-001]] — 制作与附魔系统
- [[GDD/GDD-TOWER-001]] — 法师塔建设与升级
- [[GDD/deprecated-designs]] — 废弃设计归档

### 编号系统
- [[GDD/ID-REGISTRY]] — 元素编号注册表（唯一权威源）
- [[GDD/ID-ALIAS]] — 编号别名注册表
- [[GDD/ID-REFERENCE-GRAPH]] — 编号引用关系图

### 技术文档（TDD）
- [[TDD/TDDH-COMBAT-001]] — 战斗系统技术设计（HTML原型）
- [[TDD/TDDG-COMBAT-001]] — 战斗系统技术设计（Godot版）
- [[TDD/TDD-Godot-template]] — Godot TDD模板
- [[TDD/TDD-HTML-template]] — HTML TDD模板

### 程序文档（PDD）
- [[PDD/PDD-COMBAT-001]] — 战斗系统程序设计文档（自动维护）
- [[PDD/PDD-template]] — PDD文档模板

### Agent 配置
- [[_agent-configs/01-project-director|project-director]] — 项目总监（L1）
- [[_agent-configs/02-gdd-lead|gdd-lead]] — 设计负责人（L2）
- [[_agent-configs/03-tech-lead|tech-lead]] — 技术负责人（L2）
- [[_agent-configs/04-verify-lead|verify-lead]] — 校验负责人（L2）
- [[_agent-configs/05-doc-engineer|doc-engineer]] — 文档工程师（L3）
- [[_agent-configs/06-perf-expert|perf-expert]] — 性能专家（L3）
- [[_agent-configs/07-memory-keeper|memory-keeper]] — 记忆管理师（L3）
- [[_agent-configs/08-writer-agent|writer-agent]] — 写入执行者（L2·唯一写入者）

### 工程管理
- [[memory]] — 跨会话记忆文档
- [[improvement-log]] — 持续改进日志
- [[user-communication-profile]] — 用户沟通画像
- [[DESIGN-SUMMARY-20260709]] — 2026-07-09 会话设计总结

---

## 🔗 文档关联图

```
GDD-INDEX ←── GDD-COMBAT-001 ←──→ TDDH-COMBAT-001 ←──→ PDD-COMBAT-001
    │              ↓                    ↓
    │       TDDG-COMBAT-001 ────────────┘
    │
    ├── ID-REGISTRY ←── 所有GDD引用
    ├── ID-ALIAS ←── 残留检测3
    └── ID-REFERENCE-GRAPH ←── 残留检测4
```

---

## 📌 快速导航

| 类别 | 文档 | 用途 |
|------|------|------|
| 设计 | [[GDD/GDD-INDEX]] | GDD系统索引、全局禁止清单 |
| 设计 | [[GDD/GDD-COMBAT-001]] | 游戏规则、元素清单、数值表 |
| 编号 | [[GDD/ID-REGISTRY]] | 元素编号唯一权威源 |
| 技术 | [[TDD/TDDH-COMBAT-001]] | HTML原型实现方案 |
| 技术 | [[TDD/TDDG-COMBAT-001]] | Godot实现方案 |
| 程序 | [[PDD/PDD-COMBAT-001]] | 当前代码状态、函数清单 |
| 记忆 | [[memory]] | 历史经验、教训沉淀 |
| 改进 | [[improvement-log]] | 待处理/已完成改进项 |

---

## 🎯 项目状态

- **当前版本**: v0.2.0
- **状态**: 工程体系已完善，原型开发中
- **核心系统**: 战斗系统
- **规则体系**: 14条规则、8个Agent、10个Skill、6阶段写入流程

## 变更日志
- 2026-07-15 补充缺失的GDD/Agent/工程文件索引条目
- 2026-07-06 工程体系迁移完成：新增GDD基础设施、6个规则文件、详细版AGENTS.md
- 2026-06-29 初始创建
