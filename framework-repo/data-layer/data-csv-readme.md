# CSV 数据表索引

> 本目录存放所有列举性游戏数据，供 Godot/HTML 游戏引擎直接读取。
> **文件编码**：UTF-8（Excel 打开时需导入 UTF-8）
> **分隔符**：逗号(,)
> **注释约定**：每个 CSV 首行以 `#` 开头，描述各字段含义和可选值。解析器自动跳过 `#` 行。
> **列名规范**：全小写下划线格式（如 `card_id`, `effect_type`）
> **配置指南**：详见 [[TDDH-COMBAT-001]] §2-§3

## 文件清单

| 文件 | 内容 | 对应 TDD 章节 | 行数 |
|------|------|-------------|------|
| cards.csv | 卡牌元数据（身份信息） | TDDH §3.1 | 8 |
| card_effects.csv | 卡牌效果（★核心，一卡多行=任意效果组合） | TDDH §3.2 | 8 |
| enemies.csv | 敌人基础属性 | TDDH §3.3 | 7 |
| enemy_skills.csv | 敌人技能概率表（含 shield/buff 字段） | TDDH §3.4 | 18 |
| professions.csv | 职业基础属性 | TDDH §3.5 | 4 |
| profession_starting_deck.csv | 职业初始牌组（count 列替代变长行） | TDDH §3.6 | 4 |
| status_effects.csv | 状态效果定义 | TDDH §3.7 | 5 |
| equipment_slots.csv | 装备栏规则 | TDDH §3.8 | 7 |
| localization/element_names.csv | 全部元素名称（中/英） | 全 GDD §2 | 16 |
| localization/skill_texts.csv | 技能效果文本模板（中/英） | 全 GDD §2.2 | 7 |
| races.csv | 种族属性初始值 | GDD-CHARACTER-001 §2.1 | 6 |
| origins.csv | 出身定义（特性/金币/剧情钩子） | GDD-CHARACTER-001 §2.2 | 8 |
| skills.csv | 技能定义（双属性/系数/战斗加成） | GDD-CHARACTER-001 §2.3 | 8 |
| feats_general.csv | 通用专长（9项） | GDD-CHARACTER-001 §2.5 | 11 |
| feats_legendary.csv | 传奇专长（8项） | GDD-CHARACTER-001 §2.5 | 10 |
| leveling.csv | 等级成长表（Lv1-20） | GDD-CHARACTER-001 §4 | 22 |
| legendary_path.csv | 传奇道途等级表（PL1-10） | GDD-CHARACTER-001 §9 | 12 |

## 快速配置示例

### 新增一张卡牌
1. `cards.csv` 加一行：`C007,火球,Fireball,skill,2,uncommon,`
2. `card_effects.csv` 加效果行：`C007,damage,20,enemy,on_play,0`
3. 刷新页面即生效

### 新增一个敌人
1. `enemies.csv` 加一行：`E006,龙,Dragon,200,20`
2. `enemy_skills.csv` 加技能行（可多行）：
   ```
   E006,火焰吐息,Fire Breath,0.50,25,0,0,,造成25点伤害
   E006,龙鳞护体,Dragon Scales,0.30,0,0,15,,获得15点护盾
   E006,再生,Regenerate,0.20,0,30,0,,恢复30点生命值
   ```

### 修改职业初始牌组
编辑 `profession_starting_deck.csv`，修改 count 值或添加新行即可。

## 引擎读取说明

### Godot
```gdscript
var file = FileAccess.open("res://data/csv/cards.csv", FileAccess.READ)
while not file.eof_reached():
    var line = file.get_csv_line()
    if line[0].begins_with("#"): continue  # 跳过注释行
```

### HTML/JavaScript
```javascript
// fetch 自动加载，parseCSV 自动跳过 # 行
fetch('../data/csv/cards.csv')
  .then(r => r.text())
  .then(csv => parseCSV(csv))
```

## 多语言支持
- localization/ 目录下的 CSV 作为语言键值对
- 切换语言时加载对应列（NAME_ZH / NAME_EN）
- 扩展语言时新增列（如 NAME_JA, NAME_DE）

## 变更日志
- 2026-07-07 v0.3.0 **角色系统CSV迁移**：新增 races/origins/skills/feats_general/feats_legendary/leveling/legendary_path 共7个CSV文件（GDD-CHARACTER-001）
- 2026-07-06 v0.2.0 **CSV 架构重构**：cards/effects 分离解耦；新增 card_effects.csv + profession_starting_deck.csv；全部 CSV 添加 `#` 注释行；列名统一小写；enemy_skills 新增 shield/buff 字段
- 2026-07-06 v0.1.0 初始创建
