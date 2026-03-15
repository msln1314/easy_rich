import traceback
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from apps.admin.stock.models import (
    StockBasicInfo,
    StockRealtime,
    StockBoardIndustry,
    StockBoardConcept,
)
from apps.module_task.stock_service_client import StockServiceClient
from utils.stock import StockUtils


async def sync_stock_base_info(db: AsyncSession) -> dict:
    """
    从 Stock Service 同步股票基础信息
    获取A股所有股票的基础信息并更新到数据库
    :return: 操作结果
    """
    try:
        print("开始从 Stock Service 同步股票基础信息...")

        # 调用 stock_service_client 获取股票基础信息
        async with StockServiceClient() as client:
            stock_list = await client.get_all_stock_list()

        if not stock_list:
            return {"is_success": False, "message": "未获取到股票基础信息"}

        # 获取数据库中已有的 full_code 列表
        sql = select(StockBasicInfo.full_code)
        result = await db.execute(sql)
        existing_full_codes = set(result.scalars().all())
        print(f"数据库中已有的 full_code 数量: {len(existing_full_codes)}")
        if existing_full_codes:
            print(f"示例 full_code: {list(existing_full_codes)[:5]}")

        # 处理数据
        updated_count = 0
        added_count = 0
        processed_codes = set()  # 用于检查本次同步中的重复

        for stock in stock_list:
            try:
                stock_code = stock.get("code", "")

                if not stock_code:
                    continue

                # 使用 StockUtils 计算完整股票代码
                full_code = StockUtils.get_full_code(stock_code)

                # 检查本次同步中是否已处理过该股票
                if full_code in processed_codes:
                    print(f"跳过重复股票: {full_code}")
                    continue
                processed_codes.add(full_code)

                if not full_code:
                    continue

                # 构建数据
                stock_data = {
                    "full_code": full_code,
                    "stock_code": stock_code,
                    "stock_name": stock.get("name", ""),
                    "current_price": stock.get("price"),
                    "change_percent": stock.get("change_percent"),
                    "change_amount": stock.get("change_amount"),
                    "open_price": stock.get("open"),
                    "high_price": stock.get("high"),
                    "low_price": stock.get("low"),
                    "close_price": stock.get("price") - stock.get("change_amount") if stock.get("price") and stock.get("change_amount") else None,
                    "volume": stock.get("volume"),
                    "amount": stock.get("amount"),
                    "turnover_rate": stock.get("turnover_rate"),
                    "volume_ratio": stock.get("volume_ratio"),
                    "amplitude": stock.get("amplitude"),
                    "pe_ratio": stock.get("pe_ratio"),
                    "pb_ratio": stock.get("pb_ratio"),
                    "total_market_cap": stock.get("market_cap"),
                    "circulating_market_cap": stock.get("circulating_market_cap"),
                }

                if full_code in existing_full_codes:
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
                traceback.print_exc()
                continue

        await db.commit()
        message = f"成功同步：新增 {added_count} 条，更新 {updated_count} 条股票基础信息"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步股票基础信息失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_stock_realtime_to_basic(db: AsyncSession) -> dict:
    """
    从 Stock Service 同步实时行情数据并更新到 stock_basic_info 表（用于排行功能）
    :return: 操作结果
    """
    try:
        print("开始从 Stock Service 同步实时行情数据到 stock_basic_info 表...")

        # 调用 stock_service_client 获取股票实时行情
        async with StockServiceClient() as client:
            stock_list = await client.get_all_stock_list()

        if not stock_list:
            return {"is_success": False, "message": "未获取到实时行情数据"}

        # 获取数据库中已有的 full_code 列表
        sql = select(StockBasicInfo.full_code)
        result = await db.execute(sql)
        existing_full_codes = set(result.scalars().all())

        # 处理数据
        updated_count = 0

        for stock in stock_list:
            try:
                stock_code = stock.get("code", "")

                if not stock_code:
                    continue

                # 使用 StockUtils 计算完整股票代码
                full_code = StockUtils.get_full_code(stock_code)

                if not full_code or full_code not in existing_full_codes:
                    continue  # 只更新已存在的股票

                # 构建更新数据
                stock_data = {
                    "current_price": stock.get("price"),
                    "change_percent": stock.get("change_percent"),
                    "change_amount": stock.get("change_amount"),
                    "open_price": stock.get("open"),
                    "high_price": stock.get("high"),
                    "low_price": stock.get("low"),
                    "volume": stock.get("volume"),
                    "amount": stock.get("amount"),
                    "turnover_rate": stock.get("turnover_rate"),
                    "volume_ratio": stock.get("volume_ratio"),
                    "amplitude": stock.get("amplitude"),
                    "pe_ratio": stock.get("pe_ratio"),
                    "pb_ratio": stock.get("pb_ratio"),
                    "total_market_cap": stock.get("market_cap"),
                    "circulating_market_cap": stock.get("circulating_market_cap"),
                    "change_speed": stock.get("change_speed"),
                    "change_5min": stock.get("change_5min"),
                    "change_60day": stock.get("change_60day"),
                    "change_ytd": stock.get("change_ytd"),
                    "updated_at": datetime.now(),
                }

                # 更新现有记录
                update_stmt = (
                    update(StockBasicInfo)
                    .where(StockBasicInfo.full_code == full_code)
                    .values(**stock_data)
                )
                await db.execute(update_stmt)
                updated_count += 1

            except Exception as e:
                print(f"更新股票 {stock_code} 实时数据失败: {str(e)}")
                traceback.print_exc()
                continue

        await db.commit()
        message = f"成功更新 {updated_count} 条股票实时数据到 stock_basic_info 表"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步实时行情数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_realtime_data(db: AsyncSession) -> dict:
    """
    同步实时行情数据
    从 Stock Service 获取股票实时行情，更新股票实时数据表
    :return: 操作结果
    """
    try:
        print("开始从 Stock Service 同步实时行情数据...")

        # 从 Stock Service 获取股票列表（包含实时行情）
        async with StockServiceClient() as client:
            stock_list = await client.get_all_stock_list()

        if not stock_list:
            return {"is_success": False, "message": "未获取到实时行情数据"}

        # 获取当前日期和时间
        current_date = datetime.now().date()
        current_time = datetime.now()

        # 获取数据库中当天已有的实时数据
        sql = select(StockRealtime.stock_code).where(StockRealtime.trade_date == current_date)
        result = await db.execute(sql)
        existing_codes = set(result.scalars().all())

        # 处理数据
        added_count = 0
        updated_count = 0

        for stock in stock_list:
            try:
                stock_code = str(stock.get("code", ""))

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

                # 构建实时数据
                realtime_data = {
                    "full_code": full_code,
                    "stock_code": stock_code,
                    "stock_name": stock.get("name"),
                    "trade_date": current_date,
                    "trade_time": current_time,
                    "current_price": float(stock.get("price", 0) or 0),
                    "open_price": float(stock.get("open", 0) or 0),
                    "high_price": float(stock.get("high", 0) or 0),
                    "low_price": float(stock.get("low", 0) or 0),
                    "previous_close": float(stock.get("pre_close", 0) or 0),
                    "change_amount": float(stock.get("change_amount", 0) or 0),
                    "change_percent": float(stock.get("change_percent", 0) or 0),
                    "volume": float(stock.get("volume", 0) or 0),
                    "amount": float(stock.get("amount", 0) or 0),
                    "turnover_rate": stock.get("turnover_rate"),
                    "volume_ratio": stock.get("volume_ratio"),
                    "amplitude": stock.get("amplitude"),
                    "total_market_cap": stock.get("market_cap"),
                    "circulating_market_cap": stock.get("circulating_market_cap"),
                    "pe_ratio": stock.get("pe_ratio"),
                    "pb_ratio": stock.get("pb_ratio"),
                    "is_trading": 1,
                    "trading_status": "normal",
                    "data_source": "stock_service",
                }

                if stock_code in existing_codes:
                    # 更新现有记录
                    del realtime_data["stock_code"]
                    del realtime_data["trade_date"]
                    update_stmt = (
                        update(StockRealtime)
                        .where(StockRealtime.stock_code == stock_code)
                        .where(StockRealtime.trade_date == current_date)
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
                traceback.print_exc()
                continue

        await db.commit()
        message = f"成功同步：新增 {added_count} 条，更新 {updated_count} 条实时行情数据"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步实时行情数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_board_industry_from_akshare(db: AsyncSession) -> dict:
    """
    从 Stock Service 同步行业板块数据
    先获取当天所有的行业板块信息，判断是更新还是插入
    :return: 操作结果
    """
    try:
        print("开始从 Stock Service 获取行业板块数据...")

        # 从 Stock Service 获取行业板块数据
        async with StockServiceClient() as client:
            industry_boards = await client.get_industry_boards()

        if not industry_boards:
            return {"is_success": False, "message": "未获取到行业板块数据"}

        # 获取当前日期
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 获取数据库中当天已有的行业板块名称
        existing_board_names = await get_board_industry_by_date(db, current_date)
        existing_set = set(existing_board_names)

        # 分离需要新增和更新的数据
        boards_to_add = []
        boards_to_update = []

        for board in industry_boards:
            try:
                board_name = board.get("name", "")
                if not board_name:
                    continue

                # 构建数据
                board_data = {
                    "board_name": board_name,
                    "board_code": board.get("code"),
                    "sequence": board.get("sequence"),
                    "change_percent": board.get("change_percent"),
                    "average_price": None,
                    "total_volume": board.get("volume"),
                    "total_amount": board.get("amount"),
                    "net_inflow": board.get("net_inflow"),
                    "up_count": board.get("up_count"),
                    "down_count": board.get("down_count"),
                    "leading_stock": board.get("leading_stock"),
                    "leading_stock_price": board.get("leading_stock_price"),
                    "leading_stock_change": board.get("leading_stock_change"),
                    "leading_stock_code": board.get("leading_stock_code"),
                    "date_at": current_date,
                    "data_time": datetime.now(),
                    "data_from": "stock_service",
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
        traceback.print_exc()
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
    从 Stock Service 同步概念板块数据
    先获取当天所有的概念板块信息，判断是更新还是插入
    :return: 操作结果
    """
    try:
        print("开始从 Stock Service 获取概念板块数据...")

        # 从 Stock Service 获取概念板块数据
        async with StockServiceClient() as client:
            concept_boards = await client.get_concept_boards()

        if not concept_boards:
            return {"is_success": False, "message": "未获取到概念板块数据"}

        # 获取当前日期
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 获取数据库中当天已有的概念板块名称
        existing_board_names = await get_board_concept_by_date(db, current_date)
        existing_set = set(existing_board_names)

        # 分离需要新增和更新的数据
        boards_to_add = []
        boards_to_update = []

        for board in concept_boards:
            try:
                board_name = board.get("name", "")
                if not board_name:
                    continue

                # 构建数据
                board_data = {
                    "board_name": board_name,
                    "board_code": board.get("code"),
                    "sequence": board.get("sequence"),
                    "change_percent": board.get("change_percent"),
                    "average_price": None,
                    "total_volume": board.get("volume"),
                    "total_amount": board.get("amount"),
                    "net_inflow": board.get("net_inflow"),
                    "up_count": board.get("up_count"),
                    "down_count": board.get("down_count"),
                    "leading_stock": board.get("leading_stock"),
                    "leading_stock_price": board.get("leading_stock_price"),
                    "leading_stock_change": board.get("leading_stock_change"),
                    "leading_stock_code": board.get("leading_stock_code"),
                    "date_at": current_date,
                    "data_time": datetime.now(),
                    "data_from": "stock_service",
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
        print(f"同步概念板块数据失败: {str(e)}")
        traceback.print_exc()
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
        print(f"批量更新概念板块数据失败: {str(e)}")
        traceback.print_exc()
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


async def sync_realtime_from_stock_service(db: AsyncSession) -> dict:
    """
    从 Stock Service 同步实时行情数据
    :return: 操作结果
    """
    try:
        print("开始从 Stock Service 同步实时行情数据...")

        async with StockServiceClient() as client:
            stock_list = await client.get_all_stock_list()

        if not stock_list:
            return {"is_success": False, "message": "未获取到实时行情数据"}

        # 获取当前日期和时间
        current_date = datetime.now().date()
        current_time = datetime.now()

        # 获取数据库中当天已有的实时数据
        sql = select(StockRealtime).where(StockRealtime.trade_date == current_date)
        result = await db.execute(sql)
        existing_realtime_list = await result.scalars()
        existing_codes = {item.stock_code: item for item in existing_realtime_list}

        # 处理数据
        added_count = 0
        updated_count = 0

        for stock in stock_list:
            try:
                stock_code = stock.get("code", "")

                if not stock_code:
                    continue

                # 构建实时数据
                realtime_data = {
                    "full_code": stock.get("full_code"),
                    "stock_code": stock_code,
                    "stock_name": stock.get("name"),
                    "trade_date": current_date,
                    "trade_time": current_time,
                    "current_price": stock.get("price") or 0.0,
                    "open_price": stock.get("open") or 0.0,
                    "high_price": stock.get("high") or 0.0,
                    "low_price": stock.get("low") or 0.0,
                    "previous_close": stock.get("price") - stock.get("change_amount") if stock.get("price") and stock.get("change_amount") else 0.0,
                    "change_amount": stock.get("change_amount") or 0.0,
                    "change_percent": stock.get("change_percent") or 0.0,
                    "volume": stock.get("volume") or 0.0,
                    "amount": stock.get("amount") or 0.0,
                    "turnover_rate": stock.get("turnover_rate"),
                    "volume_ratio": stock.get("volume_ratio"),
                    "amplitude": stock.get("amplitude"),
                    "total_market_cap": stock.get("market_cap"),
                    "circulating_market_cap": stock.get("circulating_market_cap"),
                    "pe_ratio": stock.get("pe_ratio"),
                    "pb_ratio": stock.get("pb_ratio"),
                    "is_trading": 1,
                    "trading_status": "normal",
                    "data_source": "stock_service",
                }

                if stock_code in existing_codes:
                    # 更新现有记录
                    existing = existing_codes[stock_code]
                    update_stmt = (
                        update(StockRealtime)
                        .where(StockRealtime.id == existing.id)
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
                traceback.print_exc()
                continue

        await db.commit()
        message = f"成功同步：新增 {added_count} 条，更新 {updated_count} 条实时行情数据"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步实时行情数据失败: {str(e)}")
        traceback.print_exc()
        raise e
