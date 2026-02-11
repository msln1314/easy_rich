from apps.module_task.ak_service import sync_from_akshare,sync_realtime_data,sync_board_industry_from_akshare
from core.database import  session_factory
def job():
    print("hello world")

async def sync_base_info_from_akshare(db):
  
    result = await sync_from_akshare(db)

async def main_day():

    async with session_factory() as session:

        async with session.begin():
            print
            db = session
            await sync_base_info_from_akshare(db)
            # # 同步实时行情数据 从akshare获取股票实时行情，更新股票基本信息中的实时字段
            await sync_realtime_data(db)
            # 同步行业板块数据 从akshare获取行业板块数据，更新行业板块信息中的数据
            await sync_board_industry_from_akshare(db)



