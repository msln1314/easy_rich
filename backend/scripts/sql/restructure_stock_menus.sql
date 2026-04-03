-- 股票分析菜单重构SQL
-- 将菜单按功能维度分组

-- 1. 创建分组菜单
INSERT INTO sys_menu (menu_name, icon, path, component, status, hidden, `order`, menu_type, parent_id, is_delete, noCache, breadcrumb, affix, noTagsView, canTo, alwaysShow, created_at, updated_at)
VALUES
('行情概览', 'mdi:chart-box-outline', 'market-overview', '#', 1, 0, 1, 'dir', 100, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW()),
('选股工具', 'mdi:filter-outline', 'stock-screener', '#', 1, 0, 2, 'dir', 100, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW()),
('个股分析', 'mdi:chart-line-variant', 'stock-analysis', '#', 1, 0, 3, 'dir', 100, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW()),
('资金监控', 'mdi:currency-usd', 'fund-monitor', '#', 1, 0, 4, 'dir', 100, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW()),
('资讯数据', 'mdi:newspaper-variant-outline', 'news-data', '#', 1, 0, 5, 'dir', 100, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW()),
('复盘管理', 'mdi:notebook-outline', 'review-manage', '#', 1, 0, 6, 'dir', 100, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW()),
('AI分析', 'mdi:robot-outline', 'ai-analysis', '#', 1, 0, 7, 'dir', 100, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW()),
('我的股票', 'mdi:star-outline', 'my-stocks', '#', 1, 0, 8, 'dir', 100, 0, 0, 1, 0, 0, 0, 1, NOW(), NOW());

-- 2. 更新子菜单的parent_id (需要根据实际创建的分组ID调整)
-- 行情概览 (假设新创建的ID为 @overview_id)
-- SET @overview_id = (SELECT id FROM sys_menu WHERE menu_name = '行情概览' AND parent_id = 100);
-- UPDATE sys_menu SET parent_id = @overview_id WHERE path IN ('marketDashboard', 'cloud-map', 'sector-rotation', 'daily-ranking');

-- 选股工具
-- SET @screener_id = (SELECT id FROM sys_menu WHERE menu_name = '选股工具' AND parent_id = 100);
-- UPDATE sys_menu SET parent_id = @screener_id WHERE path IN ('screener', 'selection-signal', 'pattern', 'condition');

-- 个股分析
-- SET @analysis_id = (SELECT id FROM sys_menu WHERE menu_name = '个股分析' AND parent_id = 100 AND menu_type = 'dir');
-- UPDATE sys_menu SET parent_id = @analysis_id WHERE path IN ('analysis', 'aggregate', 'prediction', 'analysis_report');

-- 资金监控
-- SET @fund_id = (SELECT id FROM sys_menu WHERE menu_name = '资金监控' AND parent_id = 100);
-- UPDATE sys_menu SET parent_id = @fund_id WHERE path IN ('mainforce', 'watchlist', 'policy', 'policy_report');

-- 资讯数据
-- SET @news_id = (SELECT id FROM sys_menu WHERE menu_name = '资讯数据' AND parent_id = 100);
-- UPDATE sys_menu SET parent_id = @news_id WHERE path IN ('news', 'hot_news', 'calendar');

-- 复盘管理
-- SET @review_id = (SELECT id FROM sys_menu WHERE menu_name = '复盘管理' AND parent_id = 100);
-- UPDATE sys_menu SET parent_id = @review_id WHERE path IN ('review', 'experience', 'rules');

-- AI分析
-- SET @ai_id = (SELECT id FROM sys_menu WHERE menu_name = 'AI分析' AND parent_id = 100);
-- UPDATE sys_menu SET parent_id = @ai_id WHERE path IN ('ai-chat', 'ai-workbench', 'llm-config');

-- 我的股票
-- SET @mystock_id = (SELECT id FROM sys_menu WHERE menu_name = '我的股票' AND parent_id = 100);
-- UPDATE sys_menu SET parent_id = @mystock_id WHERE path IN ('my_stock', 'base_info');