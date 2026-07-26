---
id: PDD-SETTINGS-001
title: 游戏设置系统
type: PDD
source: GDD-CHARACTER-001 §3
version: 1.0.0
status: draft
created: 2026-07-13
---

# PDD-SETTINGS-001：游戏设置系统

> 来源：root.html · 设置菜单 + 游戏设置子面板
> 模块ID：SETTINGS-UI

---

## 1. 模块清单

| 模块 | 位置 | 职责 |
|------|------|------|
| SETTINGS-UI | root.html | 设置齿轮按钮 + 设置弹窗 + 游戏设置子面板 |
| SETTINGS-VOL | root.html | 音量滑块（localStorage持久化） |
| SETTINGS-THEME | root.html | 主题切换（dark/nebula/deep） |
| SETTINGS-DIFF | root.html | 难度调节（0.8/1.0/1.3） |
| SETTINGS-EXIT | root.html | 退出到主菜单 |

---

## 2. 元素清单

### 界面元素

| ID | 类型 | 说明 |
|----|------|------|
| btn-settings | button | fixed定位齿轮按钮，左上角，hover旋转 |
| modal-settings | div.modal-overlay | 设置主弹窗，居中显示 |
| modal-game-settings | div.modal-overlay | 游戏设置子面板 |
| settings-menu | div | 5按钮垂直菜单容器 |
| setting-volume | input[range] | 音量滑块 0-100 |
| setting-theme | select | 主题下拉 dark/nebula/deep |
| setting-diff | select | 难度下拉 0.8/1.0/1.3 |
| vol-label | span | 音量百分比显示 |

---

## 3. 交互流程

```
┌─────────────┐    点击⚙    ┌──────────────────┐
│  游戏界面    │ ──────────→ │  设置主弹窗       │
│ (状态栏⚙)   │             │  ▶继续  💾存档     │
└──────┬──────┘             │  📂读档  🎛️设置    │
       ↑                    │  🚪退出           │
       │ 关闭/继续          └───┬───┬───┬───────┘
       │                       │   │   │
       │            ┌──────────┘   │   └──────────┐
       │            ↓              ↓              ↓
       │      showContinueMenu  openGameSettings exitGame
       │            │              │              │
       │            │     ┌────────┘              │
       │            │     ↓ 游戏设置子面板         │
       │            │     🔊音量 🖥️主题 🖱️难度     │
       │            │     ⌨️快捷键提示              │
       │            │     └────────────┬───────────┘
       │            │                  ↓
       └────────────┴──────────────────┘
```

---

## 4. 函数清单

### 设置系统

| 函数 | 功能 |
|------|------|
| openSettings() | 打开设置弹窗（需角色存在） |
| resumeGame() | 关闭设置弹窗，恢复游戏 |
| saveFromMenu() | 保存到当前槽位，反馈结果 |
| loadFromMenu() | 关闭设置，打开读档界面 |
| openGameSettings() | 打开游戏设置子面板 |
| exitGame() | 确认后清空角色，返回主菜单 |
| loadSettings() | init时从localStorage加载设置 |

### 设置操作

| 函数 | 功能 |
|------|------|
| updateVolume(v) | 更新音量值+localStorage |
| updateTheme(t) | 更新主题+localStorage+apply |
| updateDiff(v) | 更新难度+localStorage |
| applyTheme(t) | 应用主题颜色到body |

---

## 5. localStorage键

| 键 | 类型 | 默认值 | 说明 |
|----|------|--------|------|
| card_adv_volume | string | "80" | 音量 0-100 |
| card_adv_theme | string | "dark" | 主题 dark/nebula/deep |
| card_adv_difficulty | string | "1.0" | 难度系数 |

---

## 6. 变更日志
- 2026-07-13 初始创建
