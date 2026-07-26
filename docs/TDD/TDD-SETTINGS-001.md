---
id: TDD-SETTINGS-001
title: 设置系统测试设计
type: TDD
source: PDD-SETTINGS-001
version: 1.0.0
status: draft
created: 2026-07-13
---

# TDD-SETTINGS-001：设置系统测试

> 实现文件：scripts/root.html | 设置菜单 + 游戏设置子面板

---

## 1. 单元测试

### 1.1 设置入口

| ID | 测试项 | 前置条件 | 操作 | 预期 |
|----|--------|----------|------|------|
| UT-S01 | openSettings无角色 | GS.char=null | 点击⚙ | 不打开弹窗 |
| UT-S02 | openSettings有角色 | GS.char存在 | 点击⚙ | 打开modal-settings |
| UT-S03 | resumeGame | modal-settings打开 | 点击继续 | 弹窗关闭，游戏恢复 |
| UT-S04 | saveFromMenu成功 | currentSlot=0,GS.char存在 | 点击存档 | 保存到localStorage，显示"存档成功" |
| UT-S05 | saveFromMenu无槽位 | currentSlot=null | 点击存档 | 显示"无法存档"提示 |
| UT-S06 | saveFromMenu无角色 | GS.char=null | 点击存档 | 显示"无法存档"提示 |
| UT-S07 | loadFromMenu | modal-settings打开 | 点击读档 | 关闭设置弹窗，打开存档选择弹窗 |

### 1.2 游戏设置子面板

| ID | 测试项 | 前置条件 | 操作 | 预期 |
|----|--------|----------|------|------|
| UT-S08 | openGameSettings | modal-settings打开 | 点击🎛️设置 | 关闭设置弹窗，打开modal-game-settings |
| UT-S09 | 音量滑块 | modal-game-settings打开 | 拖动到50 | vol-label显示"50%"，localStorage保存50 |
| UT-S10 | 主题切换 | modal-game-settings打开 | 选"星云紫" | body背景变为#1a1a24，localStorage保存nebula |
| UT-S11 | 难度调整 | modal-game-settings打开 | 选"简单" | GS.difficulty=0.8，localStorage保存0.8 |
| UT-S12 | loadSettings恢复 | localStorage有volume=50,theme=nebula | 页面加载 | applyTheme("nebula")，GS.difficulty=0.8 |

### 1.3 退出游戏

| ID | 测试项 | 前置条件 | 操作 | 预期 |
|----|--------|----------|------|------|
| UT-S13 | exitGame确认 | modal-settings打开 | 点击退出→确认 | GS.char=null,GS.scene='menu',菜单显示 |
| UT-S14 | exitGame取消 | modal-settings打开 | 点击退出→取消 | 弹窗消失，游戏状态保持 |

### 1.4 主题应用

| ID | 测试项 | 操作 | 预期 |
|----|--------|------|------|
| UT-S15 | applyTheme(dark) | applyTheme('dark') | body.background='#1a1a2e' |
| UT-S16 | applyTheme(nebula) | applyTheme('nebula') | body.background='#1a1a24' |
| UT-S17 | applyTheme(deep) | applyTheme('deep') | body.background='#0a1628' |

---

## 2. 集成测试

| ID | 测试项 | 流程 | 预期 |
|----|--------|------|------|
| IT-S01 | 角色创建→设置→存档 | 创建角色→游戏内→⚙→存档 | 自动保存成功提示 |
| IT-S02 | 退出→主菜单→继续 | 游戏中→⚙→退出→确认→主菜单→继续游戏 | 显示存档槽位，可加载 |
| IT-S03 | 设置→游戏设置→音量 | ⚙→🎛️→调音量→刷新页面→再打开设置 | 音量值持久化恢复 |
| IT-S04 | 设置→主题→保存 | ⚙→🎛️→改主题→存档→退出→重新加载 | 主题颜色保持 |

## 3. UI测试

| ID | 测试项 | 预期 |
|----|--------|------|
| UI-S01 | ⚙按钮位置 | 状态栏最左侧，fixed定位 |
| UI-S02 | ⚙按钮hover | 旋转30°+颜色变金黄 |
| UI-S03 | 设置弹窗居中 | 遮罩覆盖全屏，弹窗居中 |
| UI-S04 | 5按钮布局 | 垂直排列，带图标 |
| UI-S05 | 退出按钮样式 | 红色hover效果 |
| UI-S06 | ESC关闭 | 按ESC关闭所有弹窗 |

---

## 4. 变更日志
- 2026-07-13 初始创建，19条测试用例
