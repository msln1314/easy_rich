from apps.module_task.task_service import sync_stock_base_info, sync_realtime_data, sync_board_industry_from_akshare, sync_realtime_from_stock_service
from core.database import session_factory


def job():
    print("hello world")


async def sync_base_info_from_service(db):
    result = await sync_stock_base_info(db)




async def sync_realtime_from_akshare(db):
    result = await sync_realtime_data(db)


async def sync_realtime_from_service(db):
    result = await sync_realtime_from_stock_service(db)


async def main_day():
    async with session_factory() as session:
        async with session.begin():
            print("开始同步数据...")
            db = session

            # 同步股票基础信息（优先使用 Stock Service，失败则使用 akshare）
            try:
                result = await sync_base_info_from_service(db)
                print(f"股票基础信息同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"Stock Service 同步失败，尝试使用 akshare: {str(e)}")
            

            # # 同步实时行情数据（优先使用 Stock Service，失败则使用 akshare）
            # try:
            #     result = await sync_realtime_from_service(db)
            #     print(f"实时行情同步: {result.get('message', '未知')}")
            # except Exception as e:
            #     print(f"Stock Service 实时行情同步失败，尝试使用 akshare: {str(e)}")
            #     await sync_realtime_from_akshare(db)

            # # 同步行业板块数据
            # await sync_board_industry_from_akshare(db)
