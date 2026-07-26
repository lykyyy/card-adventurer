---
id: TDD-CHARACTER-001
title: 角色创建系统技术设计
type: TDD
source: GDD-CHARACTER-001
version: 1.0.0
status: draft
created: 2026-07-13
html_dependency:
  - scripts/character-create.html
  - scripts/root.html
csv_dependency:
  - data/csv/races.csv
  - data/csv/professions.csv
  - data/csv/origins.csv
  - data/csv/skills.csv
  - data/csv/cards.csv
  - data/csv/background_feats.csv
  - data/csv/profession_starting_deck.csv
---

# TDD-CHARACTER-001：角色创建系统技术设计

> 来源：GDD-CHARACTER-001 v2.0.0
> 实现文件：`scripts/character-create.html`

---

## 1. 模块清单

| 模块 | 文件 | 职责 |
|------|------|------|
| CC-UI | character-create.html | 三阶段10步创建流程UI和交互 |
| CC-Data | character-create.html (const) | 种族/职业/出身/事件数据定义 |
| CC-Calc | character-create.html (calcFinal) | 属性/HP/法力/牌库计算引擎 |
| ROOT-Import | root.html (loadCharFromUrl) | 接收URL参数加载角色数据到全局状态 |

---

## 2. 全局数据常量

| 常量名 | 类型 | 说明 |
|--------|------|------|
| RACES | Array(4) | 种族数据：id/name/6属性/被动/固定技能 |
| PROFESSIONS | Array(4) | 职业数据：id/name/hp/ce/能量/核心牌×3 |
| PROF_SKILLS | Object{4} | 职业→可选技能池映射（4选2） |
| PROF_FEATS | Object{4} | 职业→职业专长选项（3选1） |
| ORIGINS | Array(6) | 出身数据：id/name/金币/特性/战略牌/出身技能/剧情 |
| CHILDHOOD | Array(3) | 童年事件：3选项，每项含标签/卡牌/背景专长/属性加成 |
| YOUTH | Array(3) | 青年事件：同上结构 |
| AWAKENING | Array(3) | 觉醒事件：同上结构 |
| CARDS | Object{26} | 卡牌数据库：card_id→{name,type,cost,effect,emoji} |
| SKILLS | Array(6) | 技能数据：id/name/attrs |

---

## 3. 状态机

### 3.1 创建状态 s

```
s = {
  step: 1-10,            // 当前步骤
  race: null|RACE_ID,    // 步骤1选择
  prof: null|PROF_ID,    // 步骤2选择
  points: 0-8,           // 步骤3点数余额
  attrs: {6属性},        // 步骤3属性值
  skills: [SKILL_ID],    // 步骤4已选技能(最多2)
  feat: null|FEAT_ID,    // 步骤5选择
  origin: null|ORIGIN_ID,// 步骤6选择
  childhood: null|key,   // 步骤7选择(A/B/C)
  youth: null|key,       // 步骤8选择
  awakening: null|key,   // 步骤9选择
  deckParams: null|Object // 步骤10计算结果
}
```

### 3.2 步骤转换

```
步骤1(选种族) → 步骤2(选职业) → 步骤3(属性分配)
→ 步骤4(选技能) → 步骤5(选专长) → 步骤6(选出身)
→ 步骤7(童年) → 步骤8(青年) → 步骤9(觉醒)
→ 步骤10(总览起航)
```

### 3.3 导航规则

| 规则 | 说明 |
|------|------|
| 上一步 | 任意步骤可回退（步骤1除外），回退不丢失已选数据 |
| 下一步 | 必需选择完成后才能前进 |
| 步骤→种族重置 | 步骤1/2切换时调用 resetAttrs() 重置属性为种族基础值+8点 |

---

## 4. 接口定义

### 4.1 前端内部接口

| 函数 | 签名 | 说明 |
|------|------|------|
| init() | → void | 页面初始化，构建进度条+渲染步骤1 |
| buildProgress() | → void | 渲染10步进度条，更新阶段标签和叙事文本 |
| renderStep() | → void | 根据s.step分发到对应渲染函数 |
| goNext() | → void | 验证当前步骤选择，推进到下一步 |
| goPrev() | → void | 回退到上一步（s.step>1） |
| resetAttrs() | → void | 将attrs重置为选中种族的基础值，points=8 |
| renderRace(ct) | → void | 步骤1：种族选择卡片 |
| renderProf(ct) | → void | 步骤2：职业选择卡片 |
| renderAttr(ct) | → void | 步骤3：属性点购UI（6行+/−按钮） |
| renderSkills(ct) | → void | 步骤4：复选框技能选择（职业限定池） |
| renderFeat(ct) | → void | 步骤5：专长3选1卡片 |
| renderOrigin(ct) | → void | 步骤6：出身6选1卡片（含战略牌/技能预览） |
| renderChildhood(ct) | → void | 步骤7：童年3选1 |
| renderYouth(ct) | → void | 步骤8：青年3选1 |
| renderAwaken(ct) | → void | 步骤9：觉醒3选1 |
| renderLifeStep(ct,opts,sel,title,setter) | → void | 步骤7-9通用渲染（参数化） |
| calcFinal() | → void | 计算最终角色数据：属性+bonus→mods→hp/ce/mana→牌库→专长→技能 |
| renderFinal(ct) | → void | 步骤10：称号+属性面板+牌库分区展示 |
| launch() | → void | 跳转到root.html并传递角色数据 |
| attrInc(kk) | → void | 属性+1（最多16，消耗1点） |
| attrDec(kk) | → void | 属性−1（不低于种族基础值） |
| toggleSkill(id) | → void | 切换技能选中（最多2个） |
| mod(v) | → int | DND调整值公式：floor((v-10)/2) |

### 4.2 跨文件接口（character-create.html → root.html）

| 传递方向 | 方式 | 格式 |
|----------|------|------|
| character-create → root | URL参数 `?char={json}` | JSON序列化的 deckParams 对象 |

**deckParams 结构**：

```
{
  title: "出身·标签/标签/标签·职业",  // 称号
  prof: "战士|法师|盗贼|牧师",         // 中文职业名
  hp: Number, ce: Number,             // 基础HP/CE
  mana: Number|null,                   // 法力值（法/牧）
  stats: {str,dex,con,intel,wis,cha}, // 最终6属性
  modifiers: {str,dex,con,intel...},  // 6属性调整值
  feats: [FEAT_ID],                   // 专长ID列表
  deck: [CARD_ID],                    // 牌库ID列表
  skills: [SKILL_ID],                 // 技能ID列表
  gold: Number,                        // 起始金币
  tags: [String],                      // 人生标签
  narrative: String                    // 背景叙事
}
```

### 4.3 root.html 接收接口

**loadCharFromUrl()** — 在 init() 末尾调用：

1. 解析 `window.location.search` 中的 `?char=` 参数
2. JSON.parse 解码
3. 填充 `GS.char` 全局状态（name/hp/ce/prof/energy/mana/stats/skills/gold/deck）
4. 初始化 GS 其他字段（ap/resources/skillTree/equipment/achievements）
5. 调用 `enterMap()` 进入地图
6. `history.replaceState()` 清除URL参数（防刷新重复加载）

---

## 5. 数据流

```
character-create.html                    root.html
┌─────────────────────┐                ┌─────────────────┐
│ s (10步状态)          │                │ GS (全局状态)     │
│   ↓                  │                │   ↓              │
│ calcFinal()          │                │ loadCharFromUrl()│
│   ↓                  │  URL ?char=    │   ↓              │
│ s.deckParams ────────┼── JSON ───────→│ GS.char ← 角色数据│
│   ↓                  │                │   ↓              │
│ launch() ────────────┼── redirect ──→│ enterMap()       │
└─────────────────────┘                └─────────────────┘
```

---

## 6. 属性关联规则实现

| 攻击类型 | 主属性 | 公式（JS实现） |
|----------|--------|---------------|
| 近战物理 | STR | `damage = base + mod_str` |
| 敏捷攻击 | DEX | `damage = base + Math.floor(mod_dex * 0.8)` |
| 法术攻击 | INT | `damage = base + mod_int` |
| 神圣攻击 | WIS | `damage = base + mod_wis` |
| 护盾生成 | CON | `shield = base + mod_con * 2` |
| 治疗恢复 | WIS | `heal = base + Math.floor(mod_wis * 1.5)` |
| 控制持续 | CHA | `rounds = base + Math.floor(mod_cha / 2)` |
| 增益强度 | CHA | `bonus = base + Math.floor(mod_cha / 3)` |
| 抽牌 | INT | `draw = base + Math.ceil(mod_int / 2)` |
| DOT/流血 | — | `固定层数` |

---

## 7. 测试用例

### 7.1 创建流程测试

| 用例 | 步骤 | 预期结果 |
|------|------|----------|
| TC01-种族 | 步骤1选择精灵 | 进度条更新，下一步可用 |
| TC02-职业 | 步骤2选择法师 | 属性重置为精灵10/12/10/11/10/10，下一步可用 |
| TC03-属性 | 步骤3分配8点到各属性 | 加号/减号限制正确（上限16/下限种族值），点数扣减 |
| TC04-技能 | 步骤4在法师池4选2 | 复选框最多勾选2个，超限禁用 |
| TC05-专长 | 步骤5选择塑能师 | 下一步可用 |
| TC06-出身 | 步骤6选择学院学者 | 显示战略牌C-082+学识技能预览 |
| TC07-童年 | 步骤7选择A街头求生 | 标签好斗者+C-090+DEX+1 |
| TC08-青年 | 步骤8选择C神殿侍奉 | 标签信徒+C-051+WIS+1 |
| TC09-觉醒 | 步骤9选择B求知之旅 | 标签求道者+C-033+INT+1 |
| TC10-总览 | 步骤10 | 称号正确、牌库8+1张、属性含人生加成 |

### 7.2 牌库计算测试

| 用例 | 输入 | 预期战斗库 | 预期战略库 |
|------|------|-----------|-----------|
| TC11-战士 | P-001 + ORIGIN-001 + 7A/8A/9A | C-010/C-011/C-012/C-004/C-072/C-090/C-091/C-092 = 8张 | C-080 = 1张 |
| TC12-法师 | P-002 + ORIGIN-002 + 7B/8B/9B | C-030/C-031/C-033/C-004/C-072/C-072/C-094/C-033 = 8张 | C-082 = 1张 |
| TC13-盗贼 | P-003 + ORIGIN-003 + 7C/8C/9C | C-020/C-021/C-022/C-004/C-072/C-093/C-051/C-032 = 8张 | C-083 = 1张 |
| TC14-牧师 | P-004 + ORIGIN-004 + 7A/8B/9A | C-050/C-051/C-052/C-004/C-072/C-090/C-094/C-092 = 8张 | C-081 = 1张 |

### 7.3 跨文件传递测试

| 用例 | 操作 | 预期 |
|------|------|------|
| TC15-跳转 | 步骤10点击"踏上冒险" | 跳转到root.html?char={json} |
| TC16-加载 | root.html解析?char参数 | GS.char填充正确，自动进入地图 |
| TC17-清参 | 加载完成后 | URL中?char参数被清除 |

---

## 8. 变更日志
- 2026-07-13 初始创建，对应 GDD-CHARACTER-001 v2.0.0
