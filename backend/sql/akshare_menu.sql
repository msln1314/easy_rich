-- Easy Rich AKShare 增强功能菜单 SQL
-- 运行此SQL添加菜单数据

-- 1. 多因子选股菜单
INSERT INTO sys_menu (id, menu_name, icon, path, component, status, hidden, order_num, menu_type, parent_id, perms, create_time, update_time, delete_time) VALUES
(200, '多因子选股', 'fluent:calculate-24', 'factor', 'Vadmin/Stock/FactorSelection/FactorSelection', 1, 0, 1, 'C', (SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1), 'stock:factor:list', NOW(), NOW(), 0);

-- 2. 资金流向菜单
INSERT INTO sys_menu (id, menu_name, icon, path, component, status, hidden, order_num, menu_type, parent_id, perms, create_time, update_time, delete_time) VALUES
(201, '资金流向', 'ep:money', 'fundflow', 'Vadmin/Stock/FundFlow/FundFlow', 1, 0, 2, 'C', (SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1), 'stock:fundflow:list', NOW(), NOW(), 0);

-- 3. 涨停板分析菜单
INSERT INTO sys_menu (id, menu_name, icon, path, component, status, hidden, order_num, menu_type, parent_id, perms, create_time, update_time, delete_time) VALUES
(202, '涨停板分析', 'ep:trend-charts', 'limitup', 'Vadmin/Stock/LimitUp/LimitUp', 1, 0, 3, 'C', (SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1), 'stock:limitup:list', NOW(), NOW(), 0);

-- 4. 综合评分菜单
INSERT INTO sys_menu (id, menu_name, icon, path, component, status, hidden, order_num, menu_type, parent_id, perms, create_time, update_time, delete_time) VALUES
(203, '综合评分', 'ep:star', 'composite', 'Vadmin/Stock/CompositeScore/CompositeScore', 1, 0, 4, 'C', (SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1), 'stock:composite:list', NOW(), NOW(), 0);
