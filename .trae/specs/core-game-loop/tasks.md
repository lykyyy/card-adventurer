# 核心游戏循环 任务清单

## 阶段0：CSV配置先行

- [x] Task 0.1：创建 map_nodes.csv ✅ 14节点·6类型·4地形
- [x] Task 0.2：创建 grid_cards.csv ✅ 25张·7类型齐全
- [x] Task 0.3：更新 _schema.csv ✅ 注册2新文件

## 阶段1：root.html 统一入口

- [x] Task 1.1：创建 root.html 框架 ✅ 5场景·fadeIn动画·gameState
- [x] Task 1.2：集成主菜单 ✅ 星空粒子·开始冒险→角色创建
- [x] Task 1.3：集成角色创建 ✅ cr*函数族·7步流程完整嵌入

## 阶段2：L1 地图层实现

- [x] Task 2.1：Canvas星域地图渲染 ✅ 14节点·连线·迷雾·星空
- [x] Task 2.2：地图交互逻辑 ✅ 点击节点·AP消耗·地形差异
- [x] Task 2.3：节点效果触发 ✅ combat→L3·event→L2·rest恢复·shop商店

## 阶段3：L2 网格层实现

- [x] Task 3.1：5×5网格渲染 ✅ CSS Grid·每格70px·EP余额
- [x] Task 3.2：翻牌交互 ✅ 7类型·即时奖励·陷阱二选一·剧情任务
- [x] Task 3.3：关联规则实现 ✅ 4种相邻提示(💰半价/⚠EP+1/敌HP-10%/+50%)
- [x] Task 3.4：区域完成与离开 ✅ 离开确认·全清奖励·返回L1

## 阶段4：L3 战斗集成

- [x] Task 4.1：战斗模块封装 ✅ launchBattle新窗口·模拟胜利/失败
- [x] Task 4.2：战斗→L2返回 ✅ 返回网格·标记完成·继续翻牌

# 任务依赖

- Task 1.2/1.3 依赖 Task 1.1（root.html框架）
- Task 2.1-2.3 依赖 Task 0.1（map_nodes.csv）+ Task 1.1
- Task 3.1-3.4 依赖 Task 0.2（grid_cards.csv）+ Task 1.1
- Task 4.1-4.2 依赖 Task 3.1（L2网格实现后战斗才能触发）
- Task 5.1-5.2 依赖 Task 0-4全部完成
