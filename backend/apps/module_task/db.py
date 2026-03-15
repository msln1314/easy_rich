from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from apps.admin.stock.models import StockBasicInfo, StockBoardIndustry

async def get_all_full_codes(db: AsyncSession) -> list[str]:
    """
    获取所有股票的full_code列表
    :return: full_code列表
    """
    sql = select(StockBasicInfo.full_code).order_by(StockBasicInfo.full_code)
    queryset = await db.scalars(sql)
    return list(queryset.all())
async def update_delist_status(db, full_codes: list[str]) -> None:
    """
    将股票状态更新为退市
    :param full_codes: full_code列表
    """
    await db.execute(
        update(StockBasicInfo)
        .where(StockBasicInfo.full_code.in_(full_codes))
        .values(
            status='D',
            delist_date=datetime.now(),
            updated_at=datetime.now()
        )
    )
    await db.flush()
    await db.commit()
async def batch_update_stock_list(db, update_datas: list[dict]) -> None:
    """
    将股票信息批量更新
    :param update_datas: 更新数据列表

    """

     # 执行更新

    for row in update_datas:
        # print(row)
        await db.execute(
        update(StockBasicInfo)
        .where(StockBasicInfo.full_code == row['full_code'])
        .values(**row)
        )
    await db.flush()
    await db.commit()


async def batch_stock_add(db, stock_list: list[StockBasicInfo]) -> None:
    """
    批量添加股票基本信息
    :param stock_list: 股票基本信息列表
    """
    db.add_all(stock_list)
    await db.flush()
    await db.commit()


async def batch_board_industry_add(db, board_list: list[StockBoardIndustry]) -> None:
    """
    批量添加行业板块信息
    :param board_list: 行业板块信息列表
    """
    db.add_all(board_list)
    await db.flush()
    await db.commit()


async def batch_board_industry_update(db, update_datas: list[dict]) -> None:
    """
    批量更新行业板块信息
    :param update_datas: 更新数据列表
    """
    for row in update_datas:
        await db.execute(
            update(StockBoardIndustry)
            .where(StockBoardIndustry.board_name == row['board_name'])
            .where(StockBoardIndustry.date_at == row['date_at'])
            .values(**row)
        )
    await db.flush()
    await db.commit()


async def get_board_industry_by_date(db, date: datetime) -> list[str]:
    """
    获取指定日期的行业板块名称列表
    :param date: 查询日期
    :return: 板块名称列表
    """
    sql = select(StockBoardIndustry.board_name).where(StockBoardIndustry.date_at == date)
    queryset = await db.scalars(sql)
    return list(queryset.all())