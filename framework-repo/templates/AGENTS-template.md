# AGENTS.md — AI Agent 系统定义

> 本项目使用 [AI Game Dev Framework](https://github.com/lykyyy/ai-game-dev-framework) v1.0.0

## 8-Agent 三权分立

### L1: 统筹层
- **project-director**: 任务分发、多Agent协调、质量把控

### L2: 设计层 / 实现层 / 质量层
- **gdd-lead**: 游戏设计文档(GDD) 创作与维护
- **tech-lead**: 技术设计文档(TDD) 与代码实现
- **verify-lead**: 系统校核、五步验收、事后校验

### L3: 执行层 / 辅助层
- **writer-agent**: 唯一文件写入者（6阶段写入流程阶段5）
- **doc-engineer**: PDD格式校验
- **perf-expert**: 性能分析与优化
- **memory-keeper**: 记忆管理、对话蒸馏

## 规则索引

以下规则位于 `.trae/rules/`，alwaysApply: true：

### 核心规则
0. collaboration-protocol.md — 工作流铁律：讨论→批准→实施
1. write-pipeline.md — 6阶段写入流程
2. 防幻觉规则.md — 元素清单约束+数值来源追溯
3. id-management.md — 编号注册先于写入
4. pdd自动维护规则.md — 代码变更后自动同步PDD

### 治理规则
5. skill-permissions.md — 22-Skill×8-Agent权限矩阵
6. context-verify.md — 设计前背景设定查询
7. csv-data-management.md — 动态数据层架构
8. 文档关联规则.md — GDD↔TDD↔PDD↔代码绑定
9. tdd-generation-rules.md — TDD生成前ID校验
10. residual-coverage-check.md — 5类残留覆盖检测
11. 五步验收sop.md — 功能完成后5步验收
12. 编程行为准则.md — 八荣八耻编码规范

### 运维规则
13. session-startup.md — 新会话强制加载记忆
14. 上下文健康度规则.md — 心跳信号+记忆模糊检测
15. 对话蒸馏规则.md — 用户沟通画像自动提取
16. agent-config-consistency.md — Agent配置一致性
17. alias-graph-maintenance.md — ID-ALIAS+ID-REFERENCE-GRAPH
18. rule-index-integrity.md — 规则索引完整性
19. automation-validation.md — 自动化校验脚本

## 文档体系

- GDD: `docs/GDD/` — 游戏设计文档
- TDD: `docs/TDD/` — 技术设计文档
- PDD: `docs/PDD/` — 程序文档（代码实现状态）
- ID-REGISTRY: `docs/GDD/ID-REGISTRY.md` — 元素编号中央注册表
- Agent Configs: `docs/_agent-configs/` — Agent 配置文件

## 禁止事项

全局禁止清单（来自GDD-INDEX.md）：
- 禁止在GDD中内嵌完整数据表（数据在CSV中）
- 禁止代码中硬编码列举性数据
- 禁止使用未注册的元素编号
- 禁止跳过6阶段写入流程
- 禁止writer-agent以外的Agent直接写入文件