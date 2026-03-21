-- 股票数据同步定时任务初始化脚本
-- 执行方式: 在 MySQL 客户端中执行此脚本

-- 先创建任务分组（如果不存在）
INSERT INTO sys_task_group (name, description, status, created_at, updated_at, is_delete)
VALUES ('股票数据同步', '股票数据定时同步任务组', 1, NOW(), NOW(), 0)
ON DUPLICATE KEY UPDATE name = '股票数据同步';

-- 获取分组ID
SET @task_group_id = (SELECT id FROM sys_task_group WHERE name = '股票数据同步' LIMIT 1);

-- 1. 每日凌晨同步任务
-- 包含: 股票基础信息、板块数据、北向资金历史、筹码分布
INSERT INTO sys_task (name, jobstore, executor, trigger, trigger_args, job_class, args, kwargs, coalesce, max_instances, status, task_group_id, created_at, updated_at, is_delete)
VALUES ('每日数据同步', 'default', 'default', 'cron', '0 0 2 * * ?', 'scheduler.main_day', NULL, NULL, 0, 1, 1, @task_group_id, NOW(), NOW(), 0)
ON DUPLICATE KEY UPDATE trigger_args = '0 0 2 * * ?', updated_at = NOW();

-- 2. 实时数据同步任务
-- 包含: 大盘指数、实时北向资金
INSERT INTO sys_task (name, jobstore, executor, trigger, trigger_args, job_class, args, kwargs, coalesce, max_instances, status, task_group_id, created_at, updated_at, is_delete)
VALUES ('实时数据同步', 'default', 'default', 'cron', '0 */5 9-15 * * ?', 'scheduler.main_realtime', NULL, NULL, 0, 1, 1, @task_group_id, NOW(), NOW(), 0)
ON DUPLICATE KEY UPDATE trigger_args = '0 */5 9-15 * * ?', updated_at = NOW();

-- 3. 小时数据同步任务
-- 包含: 股票热度排名、热度详情历史、新闻资讯
INSERT INTO sys_task (name, jobstore, executor, trigger, trigger_args, job_class, args, kwargs, coalesce, max_instances, status, task_group_id, created_at, updated_at, is_delete)
VALUES ('小时数据同步', 'default', 'default', 'cron', '0 0 9-15 * * ?', 'scheduler.main_hourly', NULL, NULL, 0, 1, 1, @task_group_id, NOW(), NOW(), 0)
ON DUPLICATE KEY UPDATE trigger_args = '0 0 9-15 * * ?', updated_at = NOW();

-- 4. 收盘后数据同步任务
-- 包含: 个股资金流向、每日排行历史
INSERT INTO sys_task (name, jobstore, executor, trigger, trigger_args, job_class, args, kwargs, coalesce, max_instances, status, task_group_id, created_at, updated_at, is_delete)
VALUES ('收盘数据同步', 'default', 'default', 'cron', '0 30 15 * * ?', 'scheduler.main_close', NULL, NULL, 0, 1, 1, @task_group_id, NOW(), NOW(), 0)
ON DUPLICATE KEY UPDATE trigger_args = '0 30 15 * * ?', updated_at = NOW();

SELECT '定时任务初始化完成！' AS result;
SELECT id, name, trigger, trigger_args, job_class, status FROM sys_task WHERE task_group_id = @task_group_id;