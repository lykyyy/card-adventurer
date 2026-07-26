---
id: TDDH-{系统}-{序号}
title: {系统名称}技术设计（HTML原型）
type: TDD-HTML
system: {系统名}
version: 0.1.0
status: draft
source_gdd: "[[GDD-{系统}-{序号}]]"
related_pdd: "[[PDD-{系统}-{序号}]]"
created: YYYY-MM-DD
author: tech-lead
reviewer: human
---

# {系统名称}技术设计（HTML原型）

## 1. 技术方案
- 单文件HTML（内联CSS+JavaScript）
- 无外部依赖，浏览器直接打开运行
- Vanilla JS，不用框架

## 2. 数据结构（字段固定，不得自行新增）
### 玩家对象
{ id:"P001", name:"战士", hp:200, maxHp:200, mana:1, maxMana:1,
  shield:0, deck:[], hand:[], discard:[], equipment:[] }

### 卡牌对象
{ id:"C001", name:"攻击", type:"基本", cost:0, damage:10,
  description:"造成10点伤害" }

### 敌人对象
{ id:"E001", name:"史莱姆", hp:50, maxHp:50, attack:8,
  intents:[{name:"普通攻击",weight:0.6,damage:8},
           {name:"跳跃攻击",weight:0.3,damage:15},
           {name:"分裂",weight:0.1,heal:5}] }

## 3. 模块划分
1. game.js — 游戏主循环、状态机
2. card.js — 卡牌数据与效果执行
3. enemy.js — 敌人AI决策
4. ui.js — 界面渲染
5. battle.js — 战斗结算

## 4. 界面布局
- 顶部：敌方信息（名称、血量条、意图提示）
- 中间：战斗区域（技能提示、伤害数字）
- 底部：玩家信息（血量条、法力、护盾）+ 手牌区域（横排5张）
- 右下角：结束回合按钮

## 5. 开发顺序
1. HTML结构 + 血量/法力显示 + 回合切换
2. 卡牌数据和手牌渲染
3. 出牌逻辑和效果结算
4. 敌人AI和胜负判定
5. 选卡奖励和视觉打磨

## 变更日志
- [日期] v0.1.0 初始创建
- [日期] v0.2.0 [变更内容]
