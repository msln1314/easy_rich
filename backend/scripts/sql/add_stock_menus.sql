-- 添加股票分析菜单结构到sys_menu表
-- 数据库: fastapi_app

-- 1. 添加股票分析父菜单 (id=100)
INSERT INTO sys_menu (id, menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, is_delete, created_at, updated_at)
VALUES (100, '股票分析', 'mdi:chart-line', '/stock/sector-rotation', '#', '/stock', 1, 0, 5, '0', NULL, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW());

-- 2. 添加因子库子菜单
INSERT INTO sys_menu (id, menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, is_delete, created_at, updated_at)
VALUES (101, '因子库', 'mdi:function-variant', NULL, 'views/Vadmin/Stock/Factor/index', 'factor', 1, 0, 1, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW());

-- 3. 添加其他股票子菜单 (常用功能)
INSERT INTO sys_menu (id, menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, is_delete, created_at, updated_at)
VALUES
(102, '板块轮动', 'mdi:chart-donut-variant', NULL, 'views/Vadmin/Stock/SectorRotation/SectorRotation', 'sector-rotation', 1, 0, 2, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(103, '大盘座舱', 'mdi:gauge', NULL, 'views/Vadmin/Stock/MarketDashboard/MarketDashboard', 'market-dashboard', 1, 0, 3, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(104, '每日排行', 'mdi:format-list-numbered', NULL, 'views/Vadmin/Stock/DailyRanking/DailyRanking', 'daily-ranking', 1, 0, 4, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(105, '智能选股', 'mdi:filter', NULL, 'views/Vadmin/Stock/Screener/Screener', 'screener', 1, 0, 5, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(106, '主力分析', 'mdi:account-group', NULL, 'views/Vadmin/Stock/Fund/MainForce', 'mainforce', 1, 0, 6, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(107, '复盘工作台', 'mdi:notebook', NULL, 'views/Vadmin/Stock/Review/Review', 'review', 1, 0, 7, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(108, '大盘云图', 'mdi:cloud', NULL, 'views/Vadmin/Stock/MarketCloudMap/MarketCloudMap', 'cloud-map', 1, 0, 8, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(109, '热门头条', 'mdi:newspaper', NULL, 'views/Vadmin/Stock/HotNews/HotNews', 'hot-news', 1, 0, 9, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(110, '财经日历', 'mdi:calendar', NULL, 'views/Vadmin/Stock/InvestCalendar/InvestCalendar', 'calendar', 1, 0, 10, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW());

-- QMT交易模块
INSERT INTO sys_menu (id, menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, is_delete, created_at, updated_at)
VALUES
(111, '交易面板', 'mdi:cash-multiple', NULL, 'views/Vadmin/Stock/QMT/Trade/Trade', 'qmt-trade', 1, 0, 11, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(112, '持仓管理', 'mdi:briefcase', NULL, 'views/Vadmin/Stock/QMT/Position/Position', 'qmt-position', 1, 0, 12, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW());

-- AI分析模块
INSERT INTO sys_menu (id, menu_name, icon, redirect, component, path, status, hidden, `order`, menu_type, parent_id, perms, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, is_delete, created_at, updated_at)
VALUES
(113, 'AI对话助手', 'mdi:robot', NULL, 'views/Vadmin/Stock/AI/Chat/Chat', 'ai-chat', 1, 0, 13, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(114, 'AI分析师工作台', 'mdi:brain', NULL, 'views/Vadmin/Stock/AI/Workbench/Workbench', 'ai-workbench', 1, 0, 14, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW()),
(115, '大模型配置', 'mdi:cog', NULL, 'views/Vadmin/Stock/AI/LLMConfig/LLMConfig', 'llm-config', 1, 0, 15, '1', 100, NULL, 0, 1, 0, 0, 0, 1, 0, NOW(), NOW());