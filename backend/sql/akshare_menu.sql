-- Easy Rich AKShare 增强功能菜单 SQL
-- 运行此SQL添加菜单数据

-- 获取股票分析菜单的父级ID
-- 假设父级菜单ID为 X，请在执行前确认

-- 1. 多因子选股菜单
INSERT INTO sys_menu (menu_name, icon, path, component, status, hidden, `order`, menu_type, parent_id, perms) VALUES
('多因子选股', 'fluent:calculate-24', 'factor', 'Vadmin/Stock/FactorSelection/FactorSelection', 1, 0, 1, 'C', (SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1), 'stock:factor:list');

-- 2. 资金流向菜单
INSERT INTO sys_menu (menu_name, icon, path, component, status, hidden, `order`, menu_type, parent_id, perms) VALUES
('资金流向', 'ep:money', 'fundflow', 'Vadmin/Stock/FundFlow/FundFlow', 1, 0, 2, 'C', (SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1), 'stock:fundflow:list');

-- 3. 涨停板分析菜单
INSERT INTO sys_menu (menu_name, icon, path, component, status, hidden, `order`, menu_type, parent_id, perms) VALUES
('涨停板分析', 'ep:trend-charts', 'limitup', 'Vadmin/Stock/LimitUp/LimitUp', 1, 0, 3, 'C', (SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1), 'stock:limitup:list');

-- 4. 综合评分菜单
INSERT INTO sys_menu (menu_name, icon, path, component, status, hidden, `order`, menu_type, parent_id, perms) VALUES
('综合评分', 'ep:star', 'composite', 'Vadmin/Stock/CompositeScore/CompositeScore', 1, 0, 4, 'C', (SELECT id FROM sys_menu WHERE menu_name = '股票分析' LIMIT 1), 'stock:composite:list');

-- 注意：如果子查询报错，请先查询父级菜单ID，然后手动填写
-- SELECT id, menu_name FROM sys_menu WHERE menu_name = '股票分析';
