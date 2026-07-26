# 核心游戏循环 Spec

## Why
当前MVP原型仅有L3战斗层（mvp-battle.html），缺少L1地图探索和L2网格事件两个层级。需按GDD-CORE-001实现完整的三层架构流转，形成可玩的完整游戏循环。

## What Changes
- **L1地图层**：星域地图·节点网络·路径规划·AP消耗·迷雾揭示·地形差异 **BREAKING**
- **L2网格层**：5×5翻牌·7种卡牌类型·EP消耗·锁定牌·区域任务·全清奖励 **BREAKING**
- **层级流转**：L1→L2→L3→L2→L1 完整循环·状态保存·资源传递 **BREAKING**
- **CSV配置**：补全 L1地图节点/L2网格卡片/L3战斗配置的数据表
- **单文件HTML**：root.html 作为统一入口，集成三层+角色创建+主菜单

## Impact
- Affected specs: mvp-prototype（L3独立→集成入root.html）
- Affected code: scripts/root.html（新建·统一入口）、scripts/mvp-battle.html（作为子组件嵌入）
- Affected CSV: data/csv/map_nodes.csv（新建）、data/csv/grid_cards.csv（新建）
- Affected docs: GDD-CORE-001引用

## MVP范围

### IN scope
- L1地图：1个初期星域·5种节点·4种地形·AP消耗·迷雾·休息恢复
- L2网格：标准5×5·7类型翻牌·EP消耗·4种关联规则·区域任务·自由离开
- L3战斗：嵌入现有mvp-battle.html战斗逻辑
- 层级流转：完整L1→L2→L3→L2→L1循环
- 角色创建→地图→网格→战斗→返回的完整体验
- CSV先行：map_nodes.csv + grid_cards.csv + 现有CSV补全

### OUT scope
- 多星域跨章节（仅实现1个星域）
- 派系声望系统
- 商店/交易系统（留接口·实现存根）
- 事件分支判定（随机结果·不做多分支）
- 角色升级Lv2-20（仅Lv1战斗）
- 制作/附魔/装备强化

---

## ADDED Requirements

### Requirement: 统一游戏入口 root.html
系统 SHALL 提供 root.html 作为游戏唯一入口，集成主菜单→角色创建→核心循环。
- 主菜单"开始冒险"→跳转角色创建
- 角色创建完成→进入L1地图层
- L1/L2/L3在 root.html 内部切换（非页面跳转）

#### Scenario: 完整游戏流程
- **WHEN** 用户打开 root.html
- **THEN** 显示主菜单→选择角色创建→完成创建→进入星域地图→选择区域→进入5×5网格→翻出战斗牌→进入战斗→胜利→返回网格→清空区域→返回地图

### Requirement: L1 地图探索层
系统 SHALL 展示星域地图，包含节点网络、迷雾、AP余额。
- 地图使用Canvas/SVG渲染星域背景+节点连线+迷雾
- 节点类型：🔴战斗·🟡商店·🔵事件·🟣剧情·⬜休息·⬛未知
- 4种地形对AP消耗和风险的影响：商路(1AP/10%)·小行星带(2AP/40%)·未知空域(3AP/70%)·深空裂隙(3AP/90%)
- 已探索节点高亮·当前所在节点脉冲·可到达节点发亮
- AP余额显示·休息节点恢复3AP+30%HP
- 点击可到达节点→消耗AP→移动到该节点→触发节点效果

#### Scenario: 移动与AP消耗
- **WHEN** 玩家点击可到达的战斗节点
- **AND** 该节点位于小行星带地形（2AP）
- **THEN** AP-2·角色移动到该节点·触发战斗→进入L3

### Requirement: L2 5×5网格探索层
系统 SHALL 展示5×5翻牌网格，初始全部隐藏，翻牌消耗EP。
- 25张牌的7类分布（战斗6·商店2·事件4·剧情1·陷阱3·资源5·休息2·锁定2）
- 翻牌渐显动画·未翻面显示背面图案
- EP余额显示·翻牌消耗1EP（剧情0EP）
- 4种关联规则：战场补给/警戒状态/士气鼓舞/商路繁荣
- 区域任务（紫色剧情牌·前置条件·完成后清空网格）
- 自由离开按钮（至少翻1张牌后可用）
- 全清25张额外奖励提示

#### Scenario: 翻牌触发战斗
- **WHEN** 玩家点击翻面一张红色战斗牌
- **THEN** EP-1·卡牌翻面显示红色战斗图标·进入L3战斗层·战斗胜利后返回L2·该牌标记"已完成"(绿色✅)

### Requirement: L3 战斗层集成
系统 SHALL 嵌入当前mvp-battle.html的战斗逻辑，在L2触发战斗后进入。
- 战斗数据接收：角色状态(HP/CE/法力值)·敌人配置(按难度)
- 战斗结果回调：胜利→奖励卡牌+金币·失败→HP-50%·返回L2
- 战斗胜利后角色状态保存（HP/法力值跨战斗持续）

### Requirement: 层级间状态传递
系统 SHALL 在层级切换时保存并传递游戏状态。
- 全局状态：角色HP/CE上限/法力值/金币/牌库
- L2状态：当前网格25张牌状态·已翻位置·EP余额
- L1状态：地图节点探索状态·迷雾·AP余额·当前位置

### Requirement: CSV配置文件
系统 SHALL 在编码前补全以下CSV数据文件：
- data/csv/map_nodes.csv：星域节点定义（node_id/name/type/terrain/connections/reward）
- data/csv/grid_cards.csv：5×5网格卡牌池（card_id/type/name/effect/reward/conditions）
- data/csv/_schema.csv：新增两个文件的注册信息
