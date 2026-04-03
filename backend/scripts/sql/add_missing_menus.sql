-- 添加前端路由中缺失的菜单
-- 股票分析父菜单ID为100
-- 执行前请确认数据库中没有这些菜单

-- 每日排行
INSERT INTO sys_menu (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES ('每日排行', 'mdi:format-list-numbered', NULL, 'views/Vadmin/Stock/DailyRanking/DailyRanking', 'daily-ranking', 1, 0, 107, 'page', 100, NULL, 0, 1, 0, 0, 0, 1, NOW(), NOW());

-- 智能选股
INSERT INTO sys_menu (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES ('智能选股', 'mdi:filter', NULL, 'views/Vadmin/Stock/Screener/Screener', 'screener', 1, 0, 108, 'page', 100, NULL, 0, 1, 0, 0, 0, 1, NOW(), NOW());

-- 选股信号
INSERT INTO sys_menu (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES ('选股信号', 'mdi:sine-wave', NULL, 'views/Vadmin/Stock/SelectionSignal/SelectionSignal', 'selection-signal', 1, 0, 109, 'page', 100, NULL, 0, 1, 0, 0, 0, 1, NOW(), NOW());

-- 形态识别
INSERT INTO sys_menu (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES ('形态识别', 'mdi:chart-areaspline', NULL, 'views/Vadmin/Stock/Pattern/Pattern', 'pattern', 1, 0, 110, 'page', 100, NULL, 0, 1, 0, 0, 0, 1, NOW(), NOW());

-- 股票全景
INSERT INTO sys_menu (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES ('股票全景', 'mdi:view-dashboard-outline', NULL, 'views/Vadmin/Stock/Aggregate/Aggregate', 'aggregate', 1, 0, 111, 'page', 100, NULL, 0, 1, 0, 0, 0, 1, NOW(), NOW());

-- AI对话助手
INSERT INTO sys_menu (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES ('AI对话助手', 'mdi:robot-outline', NULL, 'views/Vadmin/Stock/AI/Chat/Chat', 'ai-chat', 1, 0, 112, 'page', 100, NULL, 0, 1, 0, 0, 0, 1, NOW(), NOW());

-- AI分析师工作台
INSERT INTO sys_menu (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES ('AI分析师工作台', 'mdi:brain', NULL, 'views/Vadmin/Stock/AI/Workbench/Workbench', 'ai-workbench', 1, 0, 113, 'page', 100, NULL, 0, 1, 0, 0, 0, 1, NOW(), NOW());

-- 大模型配置
INSERT INTO sys_menu (menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES ('大模型配置', 'mdi:cog-outline', NULL, 'views/Vadmin/Stock/AI/LLMConfig/LLMConfig', 'llm-config', 1, 0, 114, 'page', 100, NULL, 0, 1, 0, 0, 0, 1, NOW(), NOW());