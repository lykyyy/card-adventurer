---
id: PDD-COMBAT-001
title: 战斗系统程序设计文档
type: PDD
system: combat
version: 0.10.0
status: draft
source_gdd: "[[GDD-COMBAT-001]]"
source_tdd: "[[TDDH-COMBAT-001]]"
created: 2026-06-29
updated: 2026-07-06
auto_maintained_by: .trae/rules/pdd 自动维护规则.md
---

# 战斗系统程序设计文档

## 1. 模块清单
- game — 游戏主循环、状态机、全局状态管理（内联于 scripts/index.html）
- ui — 界面渲染、DOM操作、动画效果（内联于 scripts/index.html）
- enemy — 敌人AI决策、技能执行（内联于 scripts/index.html）
- battle — 战斗结算、胜负判定（内联于 scripts/index.html）
- csv-loader — CSV 数据加载与解析层（内联于 scripts/index.html），异步从 data/csv/ 目录加载全部游戏数据

## 2. 全局变量
- player: object — 玩家对象，由 professions.csv + profession_starting_deck.csv 填充
- enemy: object — 敌人对象，由 enemies.csv + enemy_skills.csv 填充
- gameState: object — 游戏状态对象
- cardDefinitions: object — 卡牌数据定义集合，由 cards.csv（元数据） + card_effects.csv（效果）合并构建，每张卡含 effects[] 数组
- enemyDataMap: object — 敌人数据映射 {enemy_id: 敌人对象}
- csvData: object — CSV 原始数据缓存，含 cards/cardEffects/enemies/enemySkills/professions/profStartingDeck/statusEffects/equipmentSlots 八个数组
- effectDescMap: object — 效果类型 → 描述生成函数映射表
- currentEnemyIntent: object|null — 当前敌人预选意图对象

## 3. 函数清单（只记签名，不记函数体）
- parseCSV(csvText) → array — 解析 CSV 文本为对象数组，跳过 `#` 注释行
- loadCSV(filename) → Promise(array) — 异步 fetch 单个 CSV 文件并解析
- buildCardDefinitions() → void — 两阶段构建：Step1 从 csvData.cards 建元数据（id/name/type/cost/rarity/tags/effects[]），Step2 从 csvData.cardEffects 逐行合并效果到 effects[] 并推导兼容属性（effectType/damage/shield/heal/description 等）
- buildEnemySkillMap() → object — 从 csvData.enemySkills 构建 {enemy_id: [技能对象]}，直接使用 shield/buff 列（不再从 desc 正则提取），buff=berserk→isBerserk，buff=flee→isFlee
- buildEnemyData(skillMap) → object — 从 csvData.enemies + 技能映射构建 enemyDataMap
- buildPlayerFromCSV() → void — 从 csvData.professions[0] 填充玩家基础属性，从 csvData.profStartingDeck 按 prof_id 匹配 + count 循环填充初始 collection
- loadAllGameData() → Promise(void) — 主加载入口：加载8个CSV→buildCardDefinitions→buildEnemySkillMap→buildEnemyData→buildPlayerFromCSV→启动战斗
- renderPlayerStats() → void
- renderEnemyStats() → void
- renderHand() → void
- playCard(cardId) → void
- endPlayerTurn() → void
- equipCard(cardId) → void
- unequipCard() → void
- renderEquipment() → void
- addShield(amount) → void
- shuffleArray(array) → void
- initializeDeck() → void
- shuffleDiscardToDeck() → void
- drawCard(count) → void
- discardHand() → void
- selectIntent() → object
- executeIntent(intent) → void — 执行敌人技能意图，新增 isBerserk 处理（伤害=敌人攻击力×2）
- takeDamage(amount) → void
- checkBattleEnd() → void
- addToCollection(card) → void
- showRewardScreen() → void
- showEnemyIntent(intent) → void
- hideEnemyIntent() → void
- renderPileInfo() → void
- startBattle(battleNumber) → void — 从 enemyDataMap 按顺序取敌人（深拷贝），普通敌人动态计算HP，Boss保持CSV定义HP

★ 铁律：此处绝对禁止出现 function、{、}、return、var、let、const

## 4. 状态机
| 当前状态 | 实际变量 | 转换条件 | 目标状态 |
|----------|----------|----------|----------|
| 战斗开始 | "battle_start" | 页面加载 → loadAllGameData() 异步加载6个CSV → buildCardDefinitions/builEnemySkillMap/buildEnemyData/buildPlayerFromCSV → Object.assign(enemy, enemyDataMap['E001']) → initializeDeck() + drawCard(5) + showEnemyIntent(selectIntent()) | "player_turn" |
| 玩家回合 | "player_turn" | 点击结束回合按钮 → discardHand() | "enemy_turn" |
| 玩家回合 | "player_turn" | 点击手牌 | 执行卡牌效果 |
| 玩家回合 | "player_turn" | 打出装备牌 | "player_turn"（equipCard，装备栏更新） |
| 玩家回合 | "player_turn" | 点击装备栏 | "player_turn"（unequipCard，装备移入弃牌堆） |
| 玩家回合 | "player_turn" | 敌人HP≤0 | "victory"（1200ms后调用showRewardScreen显示选卡奖励，选卡后1500ms→startBattle(battleNumber+1)） |
| 敌人回合 | "enemy_turn" | 0.8秒延迟后：hideEnemyIntent→executeIntent→checkBattleEnd→护盾清零/装备效果/法力重置/drawCard(5)→selectIntent预选→showEnemyIntent显示 | "player_turn" |
| 敌人回合 | "enemy_turn" | 玩家HP≤0 | "defeat" |

## 5. 事件清单
| 事件名 | 注册位置 | 监听者 | 回调函数 |
|--------|----------|--------|----------|
| on_turn_end | scripts/index.html | end-turn-btn | endPlayerTurn() |
| on_card_play | scripts/index.html | .card | playCard(cardId) |
| on_equip | scripts/index.html | playCard（装备牌分支） | equipCard(cardId) |
| on_unequip | scripts/index.html | equipment-slot | unequipCard() |
| on_reward_select | scripts/index.html | .reward-cards .card | addToCollection(card) + 关闭遮罩 + 1500ms延迟startBattle(battleNumber+1) |

## 6. 模块依赖
- gameState → player, enemy（游戏状态依赖玩家和敌人数据）
- csv-loader → fetch API, parseCSV, cardDefinitions, enemyDataMap, csvData, player, enemy（CSV加载层依赖网络请求/解析器/全局数据对象/玩家/敌人）
- cardDefinitions → csvData.cards（卡牌定义依赖 CSV 数据）
- enemyDataMap → csvData.enemies, csvData.enemySkills（敌人数据依赖 CSV 数据）
- player.collection → csvData.professions, cardDefinitions（牌库初始化依赖职业CSV和卡牌定义）
- renderPlayerStats → player（渲染依赖玩家数据）
- renderEnemyStats → enemy（渲染依赖敌人数据）
- renderHand → player.hand, DOM, renderPileInfo（手牌渲染依赖手牌数据/DOM元素/牌堆计数渲染）
- playCard → player, enemy, gameState, equipCard, checkBattleEnd
- endPlayerTurn → discardHand, gameState, selectIntent, executeIntent, checkBattleEnd, drawCard, player, player.equipment, showEnemyIntent, renderPileInfo
- addShield → player
- initializeDeck → player.collection, player.deck, shuffleArray
- drawCard → player.deck, player.hand, shuffleDiscardToDeck, renderHand
- shuffleDiscardToDeck → player.discard, player.deck, shuffleArray
- discardHand → player.hand, player.discard, renderHand
- equipCard → player.hand, player.equipment, player.discard, renderPlayerStats, renderEnemyStats, renderHand, renderEquipment
- unequipCard → player.equipment, player.discard, renderPlayerStats, renderEnemyStats, renderHand, renderEquipment
- renderEquipment → player.equipment, DOM
- shuffleArray → 无依赖（纯工具函数）
- selectIntent → enemy.intents
- executeIntent → enemy, takeDamage, DOM（新增 isBerserk 时计算 enemy.attack×2）
- takeDamage → player
- checkBattleEnd → gameState, enemy, player, DOM, showRewardScreen
- addToCollection → player.collection, cardDefinitions
- showRewardScreen → cardDefinitions, shuffleArray, addToCollection, DOM
- showEnemyIntent → currentEnemyIntent, DOM
- hideEnemyIntent → DOM
- renderPileInfo → player.deck, player.discard, DOM
- startBattle → enemyDataMap, gameState, player, initializeDeck, drawCard, selectIntent, showEnemyIntent, renderPlayerStats, renderEnemyStats, renderEquipment, renderPileInfo, DOM

## 变更日志
- 2026-06-29 v0.0.1 初始创建（空白）
- 2026-06-29 v0.1.0 创建 scripts/index.html，实现基础界面和回合切换
- 2026-06-29 v0.2.0 实现攻击卡牌（C001）出牌功能，新增 playCard、renderHand、cardDefinitions
- 2026-06-29 v0.3.0 实现防御卡牌（C002）出牌功能，新增 addShield，更新 renderPlayerStats 支持护盾显示
- 2026-06-29 v0.3.1 修订轻微问题：统一 playCard 参数名、添加 PDD ID 头部注释、补充完整状态机
- 2026-06-29 v0.4.0 实现牌组流转系统：新增 shuffleArray/initializeDeck/shuffleDiscardToDeck/drawCard/discardHand；重写 endPlayerTurn 加入弃牌→护盾清零→法力重置→抽牌循环；player 对象新增 collection 牌库（攻击×3+防御×1）
- 2026-06-29 v0.5.0 实现装备系统：player.equipment 从 [] 改为 {slot:null}；新增 equipCard/unequipCard/renderEquipment 函数；playCard 补全 heal/equipment_shield/equipment_damage 分支及武器伤害加成；endPlayerTurn 加入装备效果触发（护甲每回合+护盾）；新增装备栏 HTML/CSS 及 renderEquipment 渲染
- 2026-06-29 v0.6.0 实现敌人AI与胜负判定：新增 selectIntent/executeIntent/takeDamage/checkBattleEnd 四个函数；重写 endPlayerTurn 集成真实敌人AI（加权随机选意图→执行→胜负判定）；playCard 末尾添加 checkBattleEnd 调用；敌人物件新增 shield 属性；战斗消息初始文本动态显示敌人名称；模块清单新增 enemy 和 battle 模块
- 2026-06-29 v0.7.0 实现选卡奖励系统：新增 addToCollection/showRewardScreen 两个函数；修改 checkBattleEnd 添加 1200ms 延迟触发奖励界面；新增 reward-overlay HTML 遮罩层及对应 CSS 样式；新增 on_reward_select 事件
- 2026-06-29 v0.8.0 Bug修复+新功能：三区域布局CSS修复；敌人意图显示系统；选牌后进入下一场战斗（新增 startBattle 函数含5种敌人完整数据映射）；牌组/弃牌堆实时显示
- 2026-07-06 v0.9.0 CSV 数据驱动改造：新增 csv-loader 模块（parseCSV/loadCSV/buildCardDefinitions/buildEnemySkillMap/buildEnemyData/buildPlayerFromCSV/loadAllGameData 7个函数）；cardDefinitions/enemy/player 初始数据全部改为从 CSV 文件异步加载；startBattle 中硬编码敌人数据替换为 enemyDataMap 动态查找；executeIntent 新增 isBerserk 处理（伤害=敌人攻击力×2）；底部同步初始化改为 loadAllGameData() 异步启动
- 2026-07-06 v0.10.0 CSV 架构重构：cards/effects 分离为 cards.csv + card_effects.csv（一卡多行=多效果）；professions.csv 去除变长列，新增 profession_starting_deck.csv（count 列）；全部 CSV 添加 `#` 注释行；列名统一小写（CARD_ID→card_id 等）；parseCSV 跳过 `#` 注释行；enemy_skills 新增 shield/buff 独立字段（不再从描述提取）；新增 effectDescMap 效果描述映射表；csvData 从 6 个数组扩展为 8 个
