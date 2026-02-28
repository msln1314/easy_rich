import akshare as ak
import pandas as pd
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from apps.admin.stock.models import (
    StockBasicInfo,
    StockRealtime,
    StockBoardIndustry,
    StockBoardConcept,
)


async def sync_from_akshare(db: AsyncSession) -> dict:
    """
    从akshare同步股票基础信息
    获取A股所有股票的基础信息并更新到数据库
    :return: 操作结果
    """
    try:
        print("开始同步股票基础信息...")

        # 获取A股股票基础信息
        stock_info_df = ak.stock_zh_a_spot_em()

        if stock_info_df.empty:
            return {"is_success": False, "message": "未获取到股票基础信息"}

        # 字段映射
        column_mapping = {
            "代码": "stock_code",
            "名称": "stock_name",
            "最新价": "current_price",
            "涨跌幅": "change_percent",
            "涨跌额": "change_amount",
            "成交量": "volume",
            "成交额": "amount",
            "振幅": "amplitude",
            "最高": "high_price",
            "最低": "low_price",
            "今开": "open_price",
            "昨收": "previous_close",
            "量比": "volume_ratio",
            "换手率": "turnover_rate",
            "市盈率-动态": "pe_ratio",
            "市净率": "pb_ratio",
            "总市值": "total_market_cap",
            "流通市值": "circulating_market_cap",
        }

        # 重命名列
        stock_info_df = stock_info_df.rename(columns=column_mapping)

        # 处理数据
        updated_count = 0
        added_count = 0

        for _, row in stock_info_df.iterrows():
            try:
                stock_code = str(row["stock_code"])
                stock_name = row["stock_name"] if pd.notna(row["stock_name"]) else ""

                if not stock_code or not stock_name:
                    continue

                # 处理6位股票代码，添加后缀
                if len(stock_code) == 6:
                    if stock_code.startswith("6"):
                        full_code = f"{stock_code}.SH"
                    else:
                        full_code = f"{stock_code}.SZ"
                else:
                    full_code = stock_code

                # 检查是否存在
                sql = select(StockBasicInfo).where(StockBasicInfo.full_code == full_code)
                result = await db.execute(sql)
                existing_stock = result.scalar_one_or_none()

                # 构建数据
                stock_data = {
                    "full_code": full_code,
                    "stock_code": stock_code,
                    "stock_name": stock_name,
                    "current_price": float(row["current_price"]) if pd.notna(row["current_price"]) else None,
                    "change_percent": float(row["change_percent"]) if pd.notna(row["change_percent"]) else None,
                    "change_amount": float(row["change_amount"]) if pd.notna(row["change_amount"]) else None,
                    "open_price": float(row["open_price"]) if pd.notna(row["open_price"]) else None,
                    "high_price": float(row["high_price"]) if pd.notna(row["high_price"]) else None,
                    "low_price": float(row["low_price"]) if pd.notna(row["low_price"]) else None,
                    "previous_close": float(row["previous_close"]) if pd.notna(row["previous_close"]) else None,
                    "volume": float(row["volume"]) if pd.notna(row["volume"]) else None,
                    "amount": float(row["amount"]) if pd.notna(row["amount"]) else None,
                    "turnover_rate": float(row["turnover_rate"]) if pd.notna(row["turnover_rate"]) else None,
                    "volume_ratio": float(row["volume_ratio"]) if pd.notna(row["volume_ratio"]) else None,
                    "amplitude": float(row["amplitude"]) if pd.notna(row["amplitude"]) else None,
                    "total_market_cap": float(row["total_market_cap"]) if pd.notna(row["total_market_cap"]) else None,
                    "circulating_market_cap": float(row["circulating_market_cap"]) if pd.notna(row["circulating_market_cap"]) else None,
                    "pe_ratio": float(row["pe_ratio"]) if pd.notna(row["pe_ratio"]) else None,
                    "pb_ratio": float(row["pb_ratio"]) if pd.notna(row["pb_ratio"]) else None,
                }

                if existing_stock:
                    # 更新现有记录
                    update_stmt = (
                        update(StockBasicInfo)
                        .where(StockBasicInfo.full_code == full_code)
                        .values(**stock_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    # 新增记录
                    new_stock = StockBasicInfo(**stock_data)
                    db.add(new_stock)
                    added_count += 1

            except Exception as e:
                print(f"处理股票 {stock_code} 失败: {str(e)}")
                continue

        await db.commit()
        message = f"成功同步：新增 {added_count} 条，更新 {updated_count} 条股票基础信息"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步股票基础信息失败: {str(e)}")
        raise e


async def sync_realtime_data(db: AsyncSession) -> dict:
    """
    同步实时行情数据
    从akshare获取股票实时行情，更新股票实时数据表
    :return: 操作结果
    """
    try:
        print("开始同步实时行情数据...")

        # 获取A股实时行情
        realtime_df = ak.stock_zh_a_spot_em()

        if realtime_df.empty:
            return {"is_success": False, "message": "未获取到实时行情数据"}

        # 字段映射
        column_mapping = {
            "代码": "stock_code",
            "名称": "stock_name",
            "最新价": "current_price",
            "涨跌幅": "change_percent",
            "涨跌额": "change_amount",
            "成交量": "volume",
            "成交额": "amount",
            "振幅": "amplitude",
            "最高": "high_price",
            "最低": "low_price",
            "今开": "open_price",
            "昨收": "previous_close",
            "量比": "volume_ratio",
            "换手率": "turnover_rate",
            "市盈率-动态": "pe_ratio",
            "市净率": "pb_ratio",
            "总市值": "total_market_cap",
            "流通市值": "circulating_market_cap",
        }

        # 重命名列
        realtime_df = realtime_df.rename(columns=column_mapping)

        # 获取当前日期和时间
        current_date = datetime.now().date()
        current_time = datetime.now()

        # 处理数据
        added_count = 0
        updated_count = 0

        for _, row in realtime_df.iterrows():
            try:
                stock_code = str(row["stock_code"])

                if not stock_code:
                    continue

                # 处理6位股票代码，添加后缀
                if len(stock_code) == 6:
                    if stock_code.startswith("6"):
                        full_code = f"{stock_code}.SH"
                    else:
                        full_code = f"{stock_code}.SZ"
                else:
                    full_code = stock_code

                # 检查今日是否已存在该股票的实时数据
                sql = select(StockRealtime).where(
                    StockRealtime.stock_code == stock_code,
                    StockRealtime.trade_date == current_date
                )
                result = await db.execute(sql)
                existing_realtime = result.scalar_one_or_none()

                # 构建实时数据
                realtime_data = {
                    "full_code": full_code,
                    "stock_code": stock_code,
                    "stock_name": row["stock_name"] if pd.notna(row["stock_name"]) else None,
                    "trade_date": current_date,
                    "trade_time": current_time,
                    "current_price": float(row["current_price"]) if pd.notna(row["current_price"]) else 0.0,
                    "open_price": float(row["open_price"]) if pd.notna(row["open_price"]) else 0.0,
                    "high_price": float(row["high_price"]) if pd.notna(row["high_price"]) else 0.0,
                    "low_price": float(row["low_price"]) if pd.notna(row["low_price"]) else 0.0,
                    "previous_close": float(row["previous_close"]) if pd.notna(row["previous_close"]) else 0.0,
                    "change_amount": float(row["change_amount"]) if pd.notna(row["change_amount"]) else 0.0,
                    "change_percent": float(row["change_percent"]) if pd.notna(row["change_percent"]) else 0.0,
                    "volume": float(row["volume"]) if pd.notna(row["volume"]) else 0.0,
                    "amount": float(row["amount"]) if pd.notna(row["amount"]) else 0.0,
                    "turnover_rate": float(row["turnover_rate"]) if pd.notna(row["turnover_rate"]) else None,
                    "volume_ratio": float(row["volume_ratio"]) if pd.notna(row["volume_ratio"]) else None,
                    "amplitude": float(row["amplitude"]) if pd.notna(row["amplitude"]) else None,
                    "total_market_cap": float(row["total_market_cap"]) if pd.notna(row["total_market_cap"]) else None,
                    "circulating_market_cap": float(row["circulating_market_cap"]) if pd.notna(row["circulating_market_cap"]) else None,
                    "pe_ratio": float(row["pe_ratio"]) if pd.notna(row["pe_ratio"]) else None,
                    "pb_ratio": float(row["pb_ratio"]) if pd.notna(row["pb_ratio"]) else None,
                    "is_trading": 1,
                    "trading_status": "normal",
                    "data_source": "akshare",
                }

                if existing_realtime:
                    # 更新现有记录
                    update_stmt = (
                        update(StockRealtime)
                        .where(StockRealtime.id == existing_realtime.id)
                        .values(**realtime_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    # 新增记录
                    new_realtime = StockRealtime(**realtime_data)
                    db.add(new_realtime)
                    added_count += 1

            except Exception as e:
                print(f"处理股票 {stock_code} 实时数据失败: {str(e)}")
                continue

        await db.commit()
        message = f"成功同步：新增 {added_count} 条，更新 {updated_count} 条实时行情数据"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步实时行情数据失败: {str(e)}")
        raise e


async def sync_board_industry_from_akshare(db: AsyncSession) -> dict:
    """
    从akshare同步行业板块数据
    先获取当天所有的行业板块信息，判断是更新还是插入
    :return: 操作结果
    """
    try:
        print("开始获取行业板块数据...")

        # 获取行业板块数据
        board_industry_df = ak.stock_board_industry_name_ths()

        # 如果获取的是板块列表，需要获取详细信息
        if "板块名称" in board_industry_df.columns or "板块代码" in board_industry_df.columns:
            # 获取行业板块详细数据
            board_industry_df = ak.stock_board_industry_ths()

        # 字段映射
        column_mapping = {
            "序号": "sequence",
            "板块": "board_name",
            "涨跌幅": "change_percent",
            "总成交量": "total_volume",
            "总成交额": "total_amount",
            "净流入": "net_inflow",
            "上涨家数": "up_count",
            "下跌家数": "down_count",
            "均价": "average_price",
            "领涨股": "leading_stock",
            "领涨股-最新价": "leading_stock_price",
            "领涨股-涨跌幅": "leading_stock_change",
        }

        # 重命名列
        board_industry_df = board_industry_df.rename(columns=column_mapping)

        # 获取当前日期
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 获取数据库中当天已有的行业板块名称
        existing_board_names = await get_board_industry_by_date(db, current_date)
        existing_set = set(existing_board_names)

        # 分离需要新增和更新的数据
        boards_to_add = []
        boards_to_update = []

        for _, row in board_industry_df.iterrows():
            try:
                board_name = row["board_name"] if pd.notna(row["board_name"]) else ""
                if not board_name:
                    continue

                # 构建数据
                board_data = {
                    "board_name": board_name,
                    "board_code": None,  # 同花顺接口不提供板块代码
                    "sequence": int(row["sequence"]) if pd.notna(row["sequence"]) else None,
                    "change_percent": float(row["change_percent"]) if pd.notna(row["change_percent"]) else None,
                    "average_price": float(row["average_price"]) if pd.notna(row["average_price"]) else None,
                    "total_volume": float(row["total_volume"]) if pd.notna(row["total_volume"]) else None,
                    "total_amount": float(row["total_amount"]) if pd.notna(row["total_amount"]) else None,
                    "net_inflow": float(row["net_inflow"]) if pd.notna(row["net_inflow"]) else None,
                    "up_count": int(row["up_count"]) if pd.notna(row["up_count"]) else None,
                    "down_count": int(row["down_count"]) if pd.notna(row["down_count"]) else None,
                    "leading_stock": row["leading_stock"] if pd.notna(row["leading_stock"]) else None,
                    "leading_stock_price": float(row["leading_stock_price"]) if pd.notna(row["leading_stock_price"]) else None,
                    "leading_stock_change": float(row["leading_stock_change"]) if pd.notna(row["leading_stock_change"]) else None,
                    "leading_stock_code": None,  # 同花顺接口不提供领涨股代码
                    "date_at": current_date,
                    "data_time": datetime.now(),
                    "data_from": "akshare_ths",
                }

                # 判断是新增还是更新
                if board_name in existing_set:
                    board_data["updated_at"] = datetime.now()
                    boards_to_update.append(board_data)
                else:
                    boards_to_add.append(board_data)

            except Exception as e:
                print(f"处理行业板块数据失败: {str(e)}")
                continue

        # 执行批量新增
        add_count = 0
        if boards_to_add:
            board_models = [StockBoardIndustry(**data) for data in boards_to_add]
            db.add_all(board_models)
            add_count = len(board_models)

        # 执行批量更新
        update_count = 0
        if boards_to_update:
            for data in boards_to_update:
                board_name = data["board_name"]
                del data["board_name"]

                # 更新操作
                update_stmt = (
                    update(StockBoardIndustry)
                    .where(StockBoardIndustry.board_name == board_name)
                    .where(StockBoardIndustry.date_at == data["date_at"])
                    .values(**data)
                )
                await db.execute(update_stmt)
                update_count += 1

        await db.commit()
        message = f"成功同步：新增 {add_count} 条，更新 {update_count} 条行业板块数据"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步行业板块数据失败: {str(e)}")
        raise e


async def get_board_concept_by_date(
    db: AsyncSession, current_date: datetime
) -> list:
    """
    获取指定日期的概念板块名称列表
    """
    sql = select(StockBoardConcept.board_name).where(
        StockBoardConcept.date_at == current_date
    )
    queryset = await db.scalars(sql)
    return [i for i in queryset.all() if i]


async def get_board_industry_by_date(
    db: AsyncSession, current_date: datetime
) -> list:
    """
    获取指定日期的行业板块名称列表
    """
    sql = select(StockBoardIndustry.board_name).where(
        StockBoardIndustry.date_at == current_date
    )
    queryset = await db.scalars(sql)
    return [i for i in queryset.all() if i]


async def sync_board_concept_from_akshare(db: AsyncSession) -> dict:
    """
    从akshare同步概念板块数据
    先获取当天所有的概念板块信息，判断是更新还是插入
    :return: 操作结果
    """
    try:
        print("开始获取概念板块数据...")

        # 获取概念板块数据
        board_concept_df = ak.stock_board_concept_ths()

        # 字段映射
        column_mapping = {
            "序号": "sequence",
            "板块": "board_name",
            "涨跌幅": "change_percent",
            "总成交量": "total_volume",
            "总成交额": "total_amount",
            "净流入": "net_inflow",
            "上涨家数": "up_count",
            "下跌家数": "down_count",
            "均价": "average_price",
            "领涨股": "leading_stock",
            "领涨股-最新价": "leading_stock_price",
            "领涨股-涨跌幅": "leading_stock_change",
        }

        # 重命名列
        board_concept_df = board_concept_df.rename(columns=column_mapping)

        # 获取当前日期
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 获取数据库中当天已有的概念板块名称
        existing_board_names = await get_board_concept_by_date(db, current_date)
        existing_set = set(existing_board_names)

        # 分离需要新增和更新的数据
        boards_to_add = []
        boards_to_update = []

        for _, row in board_concept_df.iterrows():
            try:
                board_name = row["board_name"] if pd.notna(row["board_name"]) else ""
                if not board_name:
                    continue

                # 构建数据
                board_data = {
                    "board_name": board_name,
                    "board_code": None,  # 同花顺接口不提供板块代码
                    "sequence": int(row["sequence"])
                    if pd.notna(row["sequence"])
                    else None,
                    "change_percent": float(row["change_percent"])
                    if pd.notna(row["change_percent"])
                    else None,
                    "average_price": float(row["average_price"])
                    if pd.notna(row["average_price"])
                    else None,
                    "total_volume": float(row["total_volume"])
                    if pd.notna(row["total_volume"])
                    else None,
                    "total_amount": float(row["total_amount"])
                    if pd.notna(row["total_amount"])
                    else None,
                    "net_inflow": float(row["net_inflow"])
                    if pd.notna(row["net_inflow"])
                    else None,
                    "up_count": int(row["up_count"])
                    if pd.notna(row["up_count"])
                    else None,
                    "down_count": int(row["down_count"])
                    if pd.notna(row["down_count"])
                    else None,
                    "leading_stock": row["leading_stock"]
                    if pd.notna(row["leading_stock"])
                    else None,
                    "leading_stock_price": float(row["leading_stock_price"])
                    if pd.notna(row["leading_stock_price"])
                    else None,
                    "leading_stock_change": float(row["leading_stock_change"])
                    if pd.notna(row["leading_stock_change"])
                    else None,
                    "leading_stock_code": None,  # 同花顺接口不提供领涨股代码
                    "date_at": current_date,
                    "data_time": datetime.now(),
                    "data_from": "akshare_ths",
                }

                # 判断是新增还是更新
                if board_name in existing_set:
                    board_data["updated_at"] = datetime.now()
                    boards_to_update.append(board_data)
                else:
                    boards_to_add.append(board_data)

            except Exception as e:
                print(f"处理概念板块数据失败: {str(e)}")
                continue

        # 执行批量新增
        add_count = 0
        if boards_to_add:
            board_models = [StockBoardConcept(**data) for data in boards_to_add]
            await batch_board_concept_add(db, board_models)
            add_count = len(board_models)

        # 执行批量更新
        update_count = 0
        if boards_to_update:
            await batch_board_concept_update(db, boards_to_update)
            update_count = len(boards_to_update)

        message = f"成功同步：新增 {add_count} 条，更新 {update_count} 条概念板块数据"
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        raise e


async def batch_board_concept_add(
    db: AsyncSession, board_models: list
) -> None:
    """
    批量添加概念板块数据
    """
    try:
        db.add_all(board_models)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def batch_board_concept_update(
    db: AsyncSession, board_data: list
) -> None:
    """
    批量更新概念板块数据
    """
    try:
        for data in board_data:
            board_name = data["board_name"]
            del data["board_name"]

            # 更新操作
            update_stmt = (
                update(StockBoardConcept)
                .where(StockBoardConcept.board_name == board_name)
                .where(StockBoardConcept.date_at == data["date_at"])
                .values(**data)
            )
            await db.execute(update_stmt)

        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
