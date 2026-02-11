# -*- coding: utf-8 -*-

import json
import importlib
import asyncio
from datetime import datetime
from sqlalchemy.orm.session import Session
from typing import Union, List, Any, Optional
from asyncio import iscoroutinefunction
from apscheduler.job import Job
from apscheduler.events import JobExecutionEvent, EVENT_ALL, JobEvent
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore 
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from apps.admin.system.models.task import TaskModel

from application.settings import settings

from core.database import  session_factory, async_engine,engine
from core.exception import CustomException
from core.logger import logger
from utils.cron_util import CronUtil


job_stores = {
    'default': MemoryJobStore(),
    'sqlalchemy': SQLAlchemyJobStore(url=settings.DB_URI, engine=engine),
    'redis': RedisJobStore(
        host=settings.REDIS_HOST,
        port=int(settings.REDIS_PORT),
        username=settings.REDIS_USER,
        password=settings.REDIS_PASSWORD,
        db=int(settings.REDIS_DB_NAME),
    ),
}
# 配置执行器
executors = {
    'default': AsyncIOExecutor(), 
    'processpool': ProcessPoolExecutor(max_workers=1)  # 减少进程数量以减少资源消耗
}
# 配置默认参数
job_defaults = {
    'coalesce': False,  # 是否合并执行
    'max_instances': 1,  # 最大实例数
}
# 配置调度器
scheduler = AsyncIOScheduler()
scheduler.configure(
    jobstores=job_stores, 
    executors=executors, 
    job_defaults=job_defaults,
    timezone='Asia/Shanghai'
)

class SchedulerUtil:
    """
    定时任务相关方法
    """

    @classmethod
    def scheduler_event_listener(cls, event: JobEvent | JobExecutionEvent) -> None:
        """
        监听任务执行事件。
    
        参数:
        - event (JobEvent | JobExecutionEvent): 任务事件对象。
    
        返回:
        - None
        """
        # 延迟导入避免循环导入
        from apps.admin.system.models import TaskLogModel
        
        # 获取事件类型和任务ID
        event_type = event.__class__.__name__
        # 初始化任务状态
        status = True
        exception_info = ''
        if isinstance(event, JobExecutionEvent) and event.exception:
            exception_info = str(event.exception)
            status = False
        if hasattr(event, 'job_id'):
            job_id = event.job_id
            query_job = cls.get_job(job_id=job_id)
            if query_job:
                query_job_info = query_job.__getstate__()
                # 获取任务名称
                job_name = query_job_info.get('name')
                # 获取任务组名
                job_group = query_job._jobstore_alias
                # # 获取任务执行器
                job_executor = query_job_info.get('executor')
                # 获取调用目标字符串
                invoke_target = query_job_info.get('func')
                # 获取调用函数位置参数
                job_args = ','.join(map(str, query_job_info.get('args', [])))
                # 获取调用函数关键字参数
                job_kwargs = json.dumps(query_job_info.get('kwargs'))
                # 获取任务触发器
                job_trigger = str(query_job_info.get('trigger'))
                # 构造日志消息
                job_message = f"事件类型: {event_type}, 任务ID: {job_id}, 任务名称: {job_name}, 状态: {status}, 任务组: {job_group}, 错误详情: {exception_info}, 执行于{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                # 创建ORM对象
                job_log = TaskLogModel(
                    job_name=job_name,
                    job_group=job_group,
                    job_executor=job_executor,
                    invoke_target=invoke_target,
                    job_args=job_args,
                    job_kwargs=job_kwargs,
                    job_trigger=job_trigger,
                    job_message=job_message,
                    status=status,
                    exception_info=exception_info,
                    created_at=datetime.now(),
                    job_id=job_id,
                )

                # 使用后台任务保存日志，不阻塞事件处理
                asyncio.create_task(cls._save_job_log_async_wrapper(job_log))

    @classmethod
    async def close_system_scheduler(cls):
        """
        应用关闭时关闭定时任务

        :return:
        """
        scheduler.shutdown()
        logger.info('关闭定时任务成功')

    @classmethod
    async def _save_job_log_async_wrapper(cls, job_log):
        """
        异步保存任务日志的包装器函数，在独立线程中运行

        参数:
        - job_log (TaskLogModel): 任务日志对象

        返回:
        - None
        """
        print(job_log, "job_log")
        async with session_factory() as session:
            try:
                session.add(job_log)
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"保存任务日志失败: {str(e)}")



    @classmethod
    async def init_system_scheduler(cls):
        """
        应用启动时初始化定时任务。
    
        返回:
        - None
        """
        # 延迟导入避免循环导入
        from apps.admin.system.crud import TaskDal
        logger.info('🔎 开始启动定时任务...')
        scheduler.start()
        logger.info('🔎 开始启动定时任务...1')
        async with session_factory() as session:
            async with session.begin():
                db = session
                tasks, total = await TaskDal(db).get_datas(v_return_count=True)
                print(tasks, "kkkkkkkkkk")
                for item in tasks:
                    cls.remove_job(job_id=item.id)  # 删除旧任务
                    cls.add_job(item)
        scheduler.add_listener(cls.scheduler_event_listener, EVENT_ALL)
        logger.info('✅️ 系统初始定时任务加载成功')

    @classmethod
    async def close_system_scheduler(cls):
        """
        关闭系统定时任务。
    
        返回:
        - None
        """
        try:
            # 移除所有任务
            scheduler.remove_all_jobs()
            # 等待所有任务完成后再关闭
            scheduler.shutdown(wait=True)
            logger.info('✅️ 关闭定时任务成功')
        except Exception as e:
            logger.error(f'关闭定时任务失败: {str(e)}')

    @classmethod
    def get_job(cls, job_id: Union[str, int]) -> Optional[Job]:
        """
        根据任务ID获取任务对象。
    
        参数:
        - job_id (str | int): 任务ID。
    
        返回:
        - Optional[Job]: 任务对象，未找到则为 None。
        """
        return scheduler.get_job(job_id=str(job_id))

    @classmethod
    def get_all_jobs(cls) -> List[Job]:
        """
        获取全部调度任务列表。
    
        返回:
        - List[Job]: 任务列表。
        """
        return scheduler.get_jobs()

    @classmethod
    def add_job(cls, job_info: TaskModel) -> Job:
        """
        根据任务配置创建并添加调度任务。
    
        参数:
        - job_info (TaskModel): 任务对象信息（包含触发器、函数、参数等）。
    
        返回:
        - Job: 新增的任务对象。
        """
        # 动态导入模块
        # 1. 解析调用目标
        # apps.module_task.scheduler.job
        print(job_info.job_class,"job_info.job_class")
        module_path, func_name = str(job_info.job_class).rsplit('.', 1)
        # print(module_path, func_name,"module_path, func_name")
        module_path = "apps.module_task." + module_path
        try:
            module = importlib.import_module(module_path)
            job_func = getattr(module, func_name)
            
            if job_info.jobstore is None:
                job_info.jobstore = 'default'
            # 2. 确定执行器
            job_executor = job_info.executor
            if job_executor is None:
                job_executor = 'default'
            if job_info.trigger_args is None:
                    raise ValueError("interval 触发器缺少参数")
            
            if iscoroutinefunction(job_func):
                job_executor = 'default'
            if job_info.trigger == 'date':
                trigger = DateTrigger(run_date=job_info.trigger_args)
            elif job_info.trigger == 'interval':
                # 将传入的 interval 表达式拆分为不同的字段
                fields = job_info.trigger_args.strip().split()
                if len(fields) != 5:
                    raise ValueError("无效的 interval 表达式")
                second, minute, hour, day, week = tuple([int(field) if field != '*' else 0 for field in fields])
                # 秒、分、时、天、周（* * * * 1）
                trigger = IntervalTrigger(
                    weeks=week,
                    days=day,
                    hours=hour,
                    minutes=minute,
                    seconds=second,
                    start_date=job_info.start_date,
                    end_date=job_info.end_date,
                    timezone='Asia/Shanghai',
                    jitter=None
                )
            elif job_info.trigger == 'cron':
                # 秒、分、时、天、月、星期几、年 ()
                fields = job_info.trigger_args.strip().split()
                if len(fields) not in (6, 7):
                    raise ValueError("无效的 Cron 表达式")
                if not CronUtil.validate_cron_expression(job_info.trigger_args):
                    raise ValueError(f'定时任务{job_info.name}, Cron表达式不正确')

                parsed_fields = [None if field in ('*', '?') else field for field in fields]
                if len(fields) == 6:
                    parsed_fields.append(None)

                second, minute, hour, day, month, day_of_week, year = tuple(parsed_fields)
                trigger = CronTrigger(
                    second=second,
                    minute=minute,
                    hour=hour,
                    day=day,
                    month=month,
                    day_of_week=day_of_week,
                    year=year,
                    start_date=job_info.start_date,
                    end_date=job_info.end_date,
                    timezone='Asia/Shanghai'
                )
            else:
                raise ValueError("无效的 trigger 触发器")

            # 3. 添加任务
            job = scheduler.add_job(
                func=job_func,  # 直接使用函数对象
                trigger=trigger,
                args=str(job_info.args).split(',') if job_info.args else None,
                kwargs=json.loads(job_info.kwargs) if job_info.kwargs else None,
                id=str(job_info.id),
                name=job_info.name,
                coalesce=job_info.coalesce,
                max_instances=job_info.max_instances,
                jobstore=job_info.jobstore,
                executor=job_executor,
            )
            return job
        except ModuleNotFoundError:
            raise ValueError(f"未找到该模块：{module_path}")
        except AttributeError:
            raise ValueError(f"未找到该模块下的方法：{func_name}")
        except Exception as e:
            raise CustomException(msg=f"添加任务失败: {str(e)}")

    @classmethod
    def run_job(cls, task:TaskModel) -> None:
        """
        立即执行指定的任务（创建临时一次性任务）。

        参数:
        - job_id (str | int): 任务ID。

        返回:
        - Nones
        """
        temp_task = TaskModel(
            name=f"{task.name}_run_once",
            jobstore=task.jobstore,
            executor=task.executor,
            trigger='date',
            trigger_args=datetime.now() + timedelta(seconds=1),
            job_class=task.job_class,
            args=task.args,
            kwargs=task.kwargs,
            coalesce=task.coalesce,
            max_instances=task.max_instances,
        )

        # 复用 add_job 方法添加任务
        cls.add_job(temp_task)
        logger.info(f"任务已创建一次性执行: {task.name}")


    @classmethod
    def remove_job(cls, job_id: Union[str, int]) -> None:
        """
        根据任务ID删除调度任务。

        参数:
        - job_id (str | int): 任务ID。

        返回:
        - None
        """
        query_job = cls.get_job(job_id=str(job_id))
        print(query_job,"query_job1")
        if query_job:
            scheduler.remove_job(job_id=str(job_id))
        print(query_job, "query_job")

    @classmethod
    def clear_jobs(cls):
        """
        删除所有调度任务。
    
        返回:
        - None
        """
        scheduler.remove_all_jobs()

    @classmethod
    def modify_job(cls, job_id: Union[str, int]) -> Job:
        """
        更新指定任务的配置（运行中的任务下次执行生效）。
    
        参数:
        - job_id (str | int): 任务ID。
    
        返回:
        - Job: 更新后的任务对象。
    
        异常:
        - CustomException: 当任务不存在时抛出。
        """
        query_job = cls.get_job(job_id=str(job_id)) 
        if not query_job:
            raise CustomException(msg=f"未找到该任务：{job_id}")
        return scheduler.modify_job(job_id=str(job_id))

    @classmethod
    def pause_job(cls, job_id: Union[str, int]):
        """
        暂停指定任务（仅运行中可暂停，已终止不可）。
    
        参数:
        - job_id (str | int): 任务ID。
    
        返回:
        - None
    
        异常:
        - ValueError: 当任务不存在时抛出。
        """
        logger.info(f"开始获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")
        query_job = cls.get_job(job_id=str(job_id))
        if not query_job:
            raise ValueError(f"未找到该任务：{job_id}")
        scheduler.pause_job(job_id=str(job_id))
        logger.info(f"查看获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")

    @classmethod
    def resume_job(cls, job_id: Union[str, int]):
        """
        恢复指定任务（仅暂停中可恢复，已终止不可）。
    
        参数:
        - job_id (str | int): 任务ID。
    
        返回:
        - None
    
        异常:
        - ValueError: 当任务不存在时抛出。
        """
        
        logger.info(f"开始获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")
        query_job = cls.get_job(job_id=str(job_id))
        if not query_job:
            raise ValueError(f"未找到该任务：{job_id}")
        scheduler.resume_job(job_id=str(job_id))
        logger.info(f"查看获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")

    @classmethod
    def reschedule_job(cls, job_id: Union[str, int]) -> Optional[Job]:
        """
        重启指定任务的触发器。
    
        参数:
        - job_id (str | int): 任务ID。
    
        返回:
        - None
    
        异常:
        - CustomException: 当任务不存在时抛出。
        """
        logger.info(f"开始获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")
        query_job = cls.get_job(job_id=str(job_id))
        if not query_job:
            raise CustomException(msg=f"未找到该任务：{job_id}")
        scheduler.reschedule_job(job_id=str(job_id))
        logger.info(f"查看获取全部任务：{cls.get_all_jobs()}， 状态： {cls.get_job_status()}")

    @classmethod
    def export_jobs(cls):
        scheduler.export_jobs("/tmp/jobs.json")

    @classmethod
    def import_jobs(cls):
        scheduler.import_jobs("/tmp/jobs.json")

    @classmethod
    def print_jobs(cls,jobstore: Any | None = None, out: Any | None = None):
        """
        打印调度任务列表。
    
        参数:
        - jobstore (Any | None): 任务存储别名。
        - out (Any | None): 输出目标。
    
        返回:
        - None
        """
        scheduler.print_jobs(jobstore=jobstore, out=out)

    @classmethod
    def get_job_status(cls) -> str:
        """
        获取调度器当前状态。
    
        返回:
        - str: 状态字符串（'stopped' | 'running' | 'paused' | 'unknown'）。
        """
        #: constant indicating a scheduler's stopped state
        STATE_STOPPED = 0
        #: constant indicating a scheduler's running state (started and processing jobs)
        STATE_RUNNING = 1
        #: constant indicating a scheduler's paused state (started but not processing jobs)
        STATE_PAUSED = 2
        if scheduler.state == STATE_STOPPED:
            return 'stopped'
        elif scheduler.state == STATE_RUNNING:
            return 'running'
        elif scheduler.state == STATE_PAUSED:
            return 'paused'
        else:
            return 'unknown'