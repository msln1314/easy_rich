from apps.module_task.task_service import (
    sync_stock_base_info,
    sync_realtime_data,
    sync_board_industry_from_akshare,
    sync_realtime_from_stock_service,
    sync_stock_index,
    sync_stock_fund_flow,
    sync_stock_hot_rank,
    sync_north_money,
    sync_north_money_realtime,
    sync_board_concept_from_akshare,
    sync_stock_chip_distribution,
    sync_news,
    sync_stock_daily_ranking,
    sync_stock_hot_rank_detail,
)
from core.database import session_factory


def job():
    print("hello world")


async def sync_base_info_from_service(db):
    result = await sync_stock_base_info(db)


async def sync_realtime_from_akshare(db):
    result = await sync_realtime_data(db)


async def sync_realtime_from_service(db):
    result = await sync_realtime_from_stock_service(db)


async def sync_index_from_service(db):
    result = await sync_stock_index(db)


async def sync_fund_flow_from_service(db):
    result = await sync_stock_fund_flow(db)


async def sync_hot_rank_from_service(db):
    result = await sync_stock_hot_rank(db)


async def sync_north_money_from_service(db):
    result = await sync_north_money(db)


async def sync_north_money_realtime_from_service(db):
    result = await sync_north_money_realtime(db)


async def sync_chip_distribution_from_service(db):
    result = await sync_stock_chip_distribution(db)


async def sync_news_from_service(db):
    result = await sync_news(db)


async def sync_daily_ranking_from_service(db):
    result = await sync_stock_daily_ranking(db)


async def sync_hot_rank_detail_from_service(db):
    result = await sync_stock_hot_rank_detail(db)


async def main_day():
    async with session_factory() as session:
        async with session.begin():
            print("开始同步每日数据...")
            db = session

            try:
                result = await sync_base_info_from_service(db)
                print(f"股票基础信息同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"股票基础信息同步失败: {str(e)}")

            try:
                result = await sync_board_industry_from_akshare(db)
                print(f"行业板块同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"行业板块同步失败: {str(e)}")

            try:
                result = await sync_board_concept_from_akshare(db)
                print(f"概念板块同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"概念板块同步失败: {str(e)}")

            try:
                result = await sync_north_money_from_service(db)
                print(f"北向资金历史同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"北向资金历史同步失败: {str(e)}")

            try:
                result = await sync_chip_distribution_from_service(db)
                print(f"筹码分布同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"筹码分布同步失败: {str(e)}")


async def main_realtime():
    async with session_factory() as session:
        async with session.begin():
            print("开始同步实时数据...")
            db = session

            try:
                result = await sync_index_from_service(db)
                print(f"大盘指数同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"大盘指数同步失败: {str(e)}")

            try:
                result = await sync_north_money_realtime_from_service(db)
                print(f"实时北向资金同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"实时北向资金同步失败: {str(e)}")


async def main_hourly():
    async with session_factory() as session:
        async with session.begin():
            print("开始同步小时数据...")
            db = session

            try:
                result = await sync_hot_rank_from_service(db)
                print(f"股票热度排名同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"股票热度排名同步失败: {str(e)}")

            try:
                result = await sync_hot_rank_detail_from_service(db)
                print(f"热度详情同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"热度详情同步失败: {str(e)}")

            try:
                result = await sync_news_from_service(db)
                print(f"新闻资讯同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"新闻资讯同步失败: {str(e)}")


async def main_close():
    async with session_factory() as session:
        async with session.begin():
            print("开始同步收盘数据...")
            db = session

            try:
                result = await sync_fund_flow_from_service(db)
                print(f"个股资金流向同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"个股资金流向同步失败: {str(e)}")

            try:
                result = await sync_daily_ranking_from_service(db)
                print(f"每日排行同步: {result.get('message', '未知')}")
            except Exception as e:
                print(f"每日排行同步失败: {str(e)}")
