---
tags: [memory, experience]
date: 2026-07-15
---

# 卡牌冒险者 — 跨会话记忆文档

> 本文件记录项目开发过程中的经验教训、决策记录和关键发现，供后续会话参考。

---

## 一、硬约束（Hard Constraints）

### 1.1 战斗系统
- 敌人血量递增规则：50 + 20*(战斗次数-1)
- Boss战（第5场）使用暗影领主（E005），HP=150，攻击力=15
- 所有卡牌必须在持久化收集册中追踪，不得凭空产生或丢失
- 战斗专用卡牌数据（牌组/弃牌堆/装备）必须是收集册的深拷贝
- 战斗结束重置时清空所有临时卡牌数据（牌组/弃牌堆/装备）

### 1.2 程序设计
- 卡牌数据存储在 cardDefinitions 数组中，包含 type, cost, damage, description
- 游戏状态在 gameState 对象中管理，包含 player/enemy 状态和卡牌堆
- UI渲染函数以 render 开头命名（renderHand, renderPlayerStats）
- 装备卡牌打出后移到装备槽，不加入弃牌堆

### 1.3 文档体系（2026-07-06确立）
- 三文档体系：GDD（人工维护）→ TDD（AI生成·人工确认）→ PDD（IDE自动维护）
- 6阶段写入流程：生成→残留预审→系统校核→人工确认→写入→事后校验
- 三权分立：提案权（gdd-lead/tech-lead等）·校验权（verify-lead唯一）·写入权（writer-agent唯一）
- ID-REGISTRY.md 为编号体系唯一权威源
- CSV动态架构v2.0：_schema.csv中央注册表 + _foreign_keys.csv外键关系

### 1.4 Agent治理
- 8 Agent三层架构：L1 project-director / L2 gdd-lead,tech-lead,verify-lead,writer-agent / L3 doc-engineer,perf-expert,memory-keeper
- 10 Skill × 8 Agent权限矩阵
- agent-config-consistency.md：_agent-configs/必须与AGENTS.md一致

---

## 二、经验教训（Lessons Learned）

### 2.1 技术教训
- 牌组为空条件需要将弃牌堆洗入牌组
- setTimeout 定时器必须在游戏重置时清除，防止状态冲突
- koa-connect 包装器导致 ctx 泄漏，需要原生 Koa 重写（来自历史项目）
- CSV数据层：cards与card_effects分离解耦，一卡可多行效果任意组合

### 2.2 设计教训
- 防幻觉规则要求所有元素必须在 GDD 元素清单中存在
- 禁止清单中的元素绝对不得出现在代码中
- 所有数值必须来自 GDD 数值表，不得自行编造
- GDD-COMBAT-001（单角色通用战斗）已被GDD-BATTLEFIELD-001（多角色双战场）取代，文档链需同步清理

### 2.3 工程教训（2026-07-15系统审计发现）
- _agent-configs/配置文件必须与AGENTS.md保持同步，否则Agent将使用过时定义
- 自动化校验脚本必须实际存在，否则规则沦为"文档型"空文
- memory.md必须及时更新，否则跨会话经验丢失
- improvement-log.md激活后需持续维护，不可空置

---

## 三、决策记录（Decisions）

### 3.1 架构决策
- 采用三文档体系：GDD → TDD → PDD
- HTML原型使用单文件方案（内联CSS+JavaScript）
- Godot原型使用 Resource 系统管理数据
- CSV数据驱动架构：所有列举性数据从CSV加载，GDD仅描述设计意图

### 3.2 技术决策
- 优先开发 HTML 原型验证玩法
- 后续同步到 Godot 平台
- 使用 localStorage 存储持久化数据

### 3.3 设计决策（2026-07-08~07-12）

**DEC-20260712-01** MAT名称冲突裁定：以ID-REGISTRY为准（MAT-003=魔晶碎片, MAT-004=远古遗物）
**DEC-20260712-02** P-002~P-004职业注册：法师/盗贼/牧师正式注册（来源GDD-CRAFTING-001）
**DEC-20260712-03** 禁止清单矛盾裁定：以GDD-CORE-001为准，法师为4基础职业之一，非禁止元素
**DEC-20260712-04** ID格式统一：全项目统一为C-001带连字符格式
**DEC-20260712-06** MVP预设角色：跳过角色创建流程，使用固定属性预设4角色

### 3.4 核心玩法架构（GDD-CORE-001 v1.3.0）
- 三层玩法：L1地图层(AP) → L2网格层(EP·5×5翻牌) → L3战斗层(CE+职业能量)
- 四职业能量：战士(怒气)·盗贼(连击点)·法师(法力值)·牧师(法力值)
- 参考游戏：《欺诈之地》《命运之手2》《杀戮尖塔》

### 3.5 角色系统（GDD-CHARACTER-001 v2.0.0·2026-07-13）
- 三阶段10步创建流程：机械创建(拥王者式) → 人生叙事(骑砍2式) → 终局确认
- 两大卡牌库：战斗卡牌库 + 战略卡牌库
- 背景专长 BG-FEAT-001~009（步骤7-9分叉选择）
- 通用卡牌 C-090~C-094（属性关联通用牌）

---

## 四、待确认事项（Pending）

### 4.1 设计待确认
- TDD-BATTLEFIELD-001/PDD-BATTLEFIELD-001 待创建（双战场系统）
- TDD-CRAFTING-001/PDD-CRAFTING-001 待创建（制作附魔系统）
- PDD-CHARACTER-001 待创建（角色系统）

### 4.2 技术待确认
- scripts/validation/ 校验脚本需接入Git pre-commit hook
- _foreign_keys.csv 外键引用需补全（当前仅5条记录）
- GDD-COMBAT-001废弃后TDDH-COMBAT-001/PDD-COMBAT-001引用链需更新

---

## 五、项目当前状态

### 5.1 基本信息
- 最后更新：2026-07-15
- 当前阶段：原型开发
- GDD覆盖：核心/战斗/战场/角色/制作/法师塔（6系统·1废弃）
- 编号体系：23前缀·170+注册元素·18废弃编号

### 5.2 已完成系统
| 系统 | GDD | TDD | PDD | 代码 |
|------|-----|-----|-----|------|
| 核心玩法 | GDD-CORE-001 v1.3.0 | — | — | — |
| 战斗(MVP) | GDD-COMBAT-001(废弃) | TDDH-COMBAT-001 | PDD-COMBAT-001 | scripts/mvp-battle.html |
| 双战场 | GDD-BATTLEFIELD-001 v0.6.0 | TDD-BATTLEFIELD-001-html | — | — |
| 角色 | GDD-CHARACTER-001 v2.0.0 | TDD-CHARACTER-001 | — | — |
| 制作 | GDD-CRAFTING-001 v0.8.0 | — | — | — |
| 法师塔 | GDD-TOWER-001 draft | — | — | — |

### 5.3 进行中任务
- 系统审计修复（2026-07-15）

### 5.4 已知阻塞问题
- GDD-COMBAT-001废弃后文档链未完全清理
- 自动化校验脚本已创建但发现22+62+4个数据问题待修复

---

## 六、上下文健康度（Context Health）

### 6.1 称呼设置
- 当前称呼：先生
- 上次更新：2026-06-29

### 6.2 规则提醒
- maintain-pdd：代码修改后必须更新 PDD
- no-hallucination：所有元素必须来自 GDD 清单 + 8条防幻觉铁律
- review-sop：功能完成后执行五步验收
- doc-linkage：文档ID绑定规则 + ID变更传播4步流程
- code-of-conduct：八荣八耻编程准则
- context-health：称呼心跳与记忆模糊检测（三级警报）
- auto-distillation：每10轮对话自动蒸馏
- session-startup：新会话强制读取记忆5件套
- write-pipeline：6阶段写入流程（三权分立）
- residual-check：5类残留覆盖检测
- csv-management：CSV动态架构v2.0

---

## 变更日志

| 日期 | 内容 | 来源会话 |
|------|------|----------|
| 2026-07-15 | v2.0大更新：补充2026-07-06~07-13全部决策记录、项目状态表、架构约束、工程教训 | 系统审计会话 |
| 2026-06-29 | 初始创建，记录项目硬约束和经验教训 | 配置会话 |
