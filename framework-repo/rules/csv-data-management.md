---
alwaysApply: true
---

# CSV 数据管理规则（动态架构 v2.0）

## 核心原则

> **所有列举性数据通过 CSV 集中管理。数据类型通过中央注册表动态定义，新增系统无需修改规则文件。**

---

## 一、动态架构概述

### 三层体系

```
┌──────────────────────────────────────┐
│  _schema.csv    中央元数据注册表       │  ← 定义"有哪些数据、字段结构、校验规则"
│  _foreign_keys.csv  跨文件引用关系     │  ← 定义"数据之间如何关联"
├──────────────────────────────────────┤
│  races.csv / skills.csv / ...         │  ← 实际数据文件
│  (按需创建，注册即生效)                │
├──────────────────────────────────────┤
│  csv-data-management.md (本规则)      │  ← 定义"如何注册、如何校验、如何同步"
└──────────────────────────────────────┘
```

### 核心理念

| 旧架构（静态） | 新架构（动态） |
|---------------|---------------|
| 规则文件列出所有 CSV 名称 | 规则只定义注册流程，文件列表在 `_schema.csv` 中维护 |
| 新增系统需修改规则 | 新增系统只需：创建CSV → 注册到 `_schema.csv` → 完成 |
| 字段结构散落在各 CSV 注释中 | 字段结构集中在 `_schema.csv`，可编程校验 |
| 跨文件引用靠人工记忆 | `_foreign_keys.csv` 记录引用关系，支持自动校验 |

---

## 二、中央注册表：`_schema.csv`

### 2.1 位置

`data/csv/_schema.csv`

### 2.2 字段定义

| 列名 | 类型 | 说明 |
|------|------|------|
| `file_name` | string | CSV 文件名（含 `.csv` 扩展名） |
| `system` | enum | 所属系统（`combat` / `character` / `base` / `event` / `profession` / 自定义） |
| `gdd_section` | string | 对应的 GDD 章节编号 |
| `version` | semver | 当前版本号（如 `1.0.0`） |
| `status` | enum | 状态（`active` / `draft` / `reserved`） |
| `dependency` | string | 依赖的其他 CSV（`|` 分隔），无则留空 |
| `columns` | string | 列定义列表（格式见 2.3） |

### 2.3 列定义格式

```
列名:类型:约束, 列名:类型:约束, ...
```

| 元素 | 格式 | 示例 |
|------|------|------|
| 列名 | `lower_snake_case` | `card_id`, `required_level` |
| 类型 | `int` / `float` / `string` / `bool` / `enum(v1-v2)` | `int`, `enum(yes-no)` |
| 约束 | 多个约束以 `\|` 分隔 | `unique`, `range(1-20)`, `ref(cards.csv.card_id)` |

**支持的约束类型**：

| 约束 | 语法 | 说明 |
|------|------|------|
| `required` | `required` | 不可为空 |
| `optional` | `optional` | 可为空 |
| `unique` | `unique` | 值在文件中唯一 |
| `range` | `range(min-max)` | 数值范围 |
| `enum` | `enum(v1-v2-v3)` | 枚举值列表 |
| `ref` | `ref(file.column)` | 外键引用 |
| `regex` | `regex(pattern)` | 正则匹配 |

### 2.4 新增数据类型流程

**示例：未来新增「基地运营」系统的 `base_facilities.csv`**

```
步骤1：创建 CSV 文件（遵循格式规范）
  data/csv/base_facilities.csv

步骤2：在 _schema.csv 中追加一行注册
  base_facilities.csv,base,GDD-BASE-001,0.1.0,draft,,
  facility_id:string:unique,name_zh:string:required,...

步骤3：如有外键引用，在 _foreign_keys.csv 注册关系
  base_facilities.csv,required_skill,skills.csv,skill_id,restrict,restrict

步骤4：在 data/csv/README.md 添加索引条目

步骤5：完成 — 无需修改本规则文件
```

---

## 三、跨文件引用：`_foreign_keys.csv`

### 3.1 位置

`data/csv/_foreign_keys.csv`

### 3.2 字段定义

| 列名 | 说明 |
|------|------|
| `source_file` | 引用发起方 CSV |
| `source_column` | 发起方的列名 |
| `target_file` | 引用目标 CSV |
| `target_column` | 目标方的列名 |
| `on_delete` | 目标被删行为（`cascade` 级联删 / `restrict` 禁止删 / `set_null` 置空） |
| `on_update` | 目标被改行为（`cascade` 级联更新 / `restrict` 禁止改） |

### 3.3 使用场景

- **数据校验**：校验工具读取此文件，自动验证所有外键引用完整性
- **级联更新**：修改 `cards.csv` 中某卡牌 ID 时，自动搜索引用方并提示同步
- **依赖分析**：删除某个 CSV 前，查看有哪些文件引用它

---

## 四、CSV 文件格式规范

### 4.1 基本格式

```
# 字段说明行（以 # 开头，描述各字段含义和可选值）
# column1: 字段含义 (可选值: A/B/C)
# column2: 字段含义 (格式/范围)
column1,column2,column3
value1,value2,value3
```

**强制要求不变**：
- 编码：UTF-8
- 分隔符：逗号(`,`)
- 首行为 `#` 注释行
- 列名全小写下划线格式
- 解析器自动跳过 `#` 行

### 4.2 保留文件前缀

以 `_` 开头的 CSV 文件为**元数据文件**，不包含游戏数据，仅用于数据治理：

| 文件 | 用途 |
|------|------|
| `_schema.csv` | 中央数据目录 + 字段定义 |
| `_foreign_keys.csv` | 跨文件引用关系表 |

---

## 五、GDD 与 CSV 同步机制

### 5.1 GDD 引用格式

```markdown
### X.X 种族列表
> **数据文件**：`data/csv/races.csv`
> **设计说明**：种族定义6属性初始值和种族特色。
> **当前元素**：RACE-001~RACE-004
> **使用方式**：创建角色时读取 CSV，设置玩家属性。
```

### 5.2 同步检查清单

每次新增或修改数据时，必须：

| 步骤 | 操作 | 校验方法 |
|------|------|----------|
| 1 | 修改/创建对应的 CSV 文件 | 确保格式合规（首行 `#`，UTF-8） |
| 2 | 更新 `_schema.csv` 中该文件的版本号 | 版本号 `+0.0.1` |
| 3 | 如有新增外键引用，更新 `_foreign_keys.csv` | 确认 `target_file.target_column` 存在 |
| 4 | 更新 GDD 引用该 CSV 的章节 | 确保元素清单数量与 CSV 行数一致 |
| 5 | 更新 `data/csv/README.md` | 如是新文件则追加索引条目 |

### 5.3 自动化校验（强制）

以下校验**必须执行**，可在 CI/CD 或 Git Hook 中实现，未通过校验不得提交：

| 校验项 | 说明 |
|--------|------|
| Schema 一致性 | CSV 列名与 `_schema.csv` 定义一致 |
| 外键完整性 | `_foreign_keys.csv` 中所有引用目标存在 |
| 唯一性约束 | `unique` 列无重复值 |
| 枚举合规 | `enum` 列的值均在允许范围内 |
| 范围合规 | `range` 列的值在 min-max 之间 |
| 版本一致性 | GDD 引用的版本号与 `_schema.csv` 一致 |

**强制要求**：
1. 每次CSV修改必须执行校验
2. 未通过校验不得提交
3. 校验报告必须记录在变更日志中

---

## 六、禁止事项

| 禁止 | 说明 |
|------|------|
| ❌ GDD 内嵌完整数据表 | 数据集中在 CSV，GDD 仅描述设计意图 |
| ❌ CSV 与 `_schema.csv` 版本不同步 | 每次修改 CSV 结构必须更新 schema 版本号 |
| ❌ 代码中硬编码列举性数据 | 代码必须从 CSV 读取 |
| ❌ CSV 使用非 UTF-8 编码 | 统一 UTF-8 |
| ❌ CSV 列名使用中文或驼峰 | 统一小写下划线 |
| ❌ 在规则文件中定义具体 CSV 名称 | 文件清单在 `_schema.csv` 中维护 |
| ❌ 跳过 `_schema.csv` 注册直接创建数据文件 | 未注册的 CSV 视为不被系统识别的孤立文件 |

---

## 七、目录结构

```
data/csv/
├── _schema.csv          # ★ 中央元数据注册表（动态架构核心）
├── _foreign_keys.csv    # ★ 跨文件外键关系表
├── README.md            # 目录说明 + 快速配置示例
│
├── cards.csv            # 卡牌元数据
├── card_effects.csv     # 卡牌效果
├── enemies.csv          # 敌人属性
├── enemy_skills.csv     # 敌人技能
├── professions.csv      # 职业属性
├── profession_starting_deck.csv  # 职业初始牌组
├── status_effects.csv   # 状态效果
├── equipment_slots.csv  # 装备栏
├── races.csv            # 种族属性
├── origins.csv          # 出身定义
├── skills.csv           # 技能定义
├── feats_general.csv    # 通用专长
├── feats_legendary.csv  # 传奇专长
├── leveling.csv         # 等级成长
├── legendary_path.csv   # 传奇道途
│
└── localization/
    ├── element_names.csv    # 元素名称多语言
    └── skill_texts.csv      # 技能文本模板
```

> 新增系统的 CSV 文件直接放入此目录，注册到 `_schema.csv` 即可。

---

## 八、扩展示例

### 示例A：新增「职业」系统

```
1. 创建 data/csv/classes.csv
2. 在 _schema.csv 追加：
   classes.csv,profession,GDD-PROFESSION-001,0.1.0,draft,skills.csv,
   class_id:string:unique,name_zh:string:required,primary_attr:string:enum(str-dex-con-int-wis-cha),...
3. 在 _foreign_keys.csv 追加外键（如引用 skills.csv）
4. 完成 — 系统识别此为新数据模块
```

### 示例B：新增「基地运营」系统

```
1. 创建 data/csv/base_buildings.csv、base_upgrades.csv
2. 在 _schema.csv 追加两行注册（system=base）
3. 在 _foreign_keys.csv 注册建筑与升级的引用关系
4. 完成
```

### 示例C：修改现有字段

```
1. 修改 races.csv（如新增 passive_trait 列）
2. 更新 _schema.csv 中 races.csv 的 columns 字段和 version
3. 更新 GDD-CHARACTER-001 元素清单
4. 如 passive_trait 引用其他数据，追加 _foreign_keys.csv
```

---

## 变更日志
- 2026-07-07 v2.0 动态架构：新增 `_schema.csv` + `_foreign_keys.csv`；规则从静态文件清单升级为动态注册体系
- 2026-07-07 v1.0 初始创建，基于 GDD-CHARACTER-001 设计阶段总结
