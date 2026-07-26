# 太空船管理系统 检查清单

## 阶段0：CSV配置

### spaceship_templates.csv
- [ ] 至少1条飞船模板记录
- [ ] 字段齐全：template_id/name/description/build_cost/hull/shield/energy/engine_speed/weapon_damage/crew_slots

### spaceship_upgrades.csv
- [ ] 5组件×3级=15条记录
- [ ] 字段齐全：upgrade_id/component/level/cost_materials/cost_gold/stat_bonus/description
- [ ] 升级消耗递增合理（Lv1→Lv3消耗翻倍）

### crew_members.csv
- [ ] 10条船员记录（5岗位×2人）
- [ ] 字段齐全：crew_id/name/role/skill_level/bonus_desc

## 阶段1：太空船HUD

- [ ] HUD面板在L1地图左上角可见
- [ ] 5条状态条实时更新
- [ ] 面板不阻挡地图点击
- [ ] 受伤时HP缩退动画

## 阶段2：星港建造与升级

- [ ] 星港触发后显示建造界面
- [ ] 升级树5选项卡可切换
- [ ] 升级确认弹窗显示消耗+预览
- [ ] 资源不足时升级按钮disabled
- [ ] 资源余额实时更新

## 阶段3：船员管理

- [ ] 5岗位面板完整展示
- [ ] 每岗位2个可选船员
- [ ] 分配/更换交互正常
- [ ] 空岗警告显示
- [ ] 岗位效果描述文字清晰

## 阶段4：角色装备面板

- [ ] 12槽布局完整·视觉清晰
- [ ] 装备更换交互正常（点击·选装备·确认）
- [ ] 属性面板与装备加成同步
- [ ] 装备品质色标正确

## 阶段5：技能树

- [ ] 3职业线完整渲染
- [ ] 节点状态3态正确（已解锁/可解锁/锁定）
- [ ] 技能点余额显示
- [ ] 点击解锁后牌库更新

## 阶段6：成就

- [ ] 5个成就卡片正确渲染
- [ ] 进度条与完成状态同步
- [ ] 已完成成就金色高亮
