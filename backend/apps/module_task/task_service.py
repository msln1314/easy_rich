import traceback
from datetime import datetime, date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from apps.admin.stock.models import (
    StockBasicInfo,
    StockRealtime,
    StockBoardIndustry,
    StockBoardConcept,
    StockIndex,
    StockFundFlow,
    StockHotRank,
    StockNorthMoney,
    StockNorthMoneyRealtime,
    StockChipDistribution,
    StockDailyRanking,
    StockHotRankDetail,
    News,
    StockLonghubang,
    StockLonghubangDetail,
    StockMarginSummary,
    StockMarginDetail,
)
import json
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
                    "close_price": stock.get("price") - stock.get("change_amount")
                    if stock.get("price") and stock.get("change_amount")
                    else None,
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
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条股票基础信息"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步实时行情数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_longhubang(db: AsyncSession) -> dict:
    """
    同步龙虎榜数据
    从 Stock Service 获取龙虎榜数据并存储
    """
    try:
        print("开始从 Stock Service 同步龙虎榜数据...")

        async with StockServiceClient() as client:
            lhb_list = await client.get_longhubang_list()

        if not lhb_list:
            return {"is_success": False, "message": "未获取到龙虎榜数据"}

        current_time = datetime.now()
        current_date = date.today()

        added_count = 0
        updated_count = 0
        detail_added_count = 0

        for lhb in lhb_list:
            try:
                stock_code = lhb.get("stock_code", "") or lhb.get("code", "")
                if not stock_code:
                    continue

                full_code = StockUtils.get_full_code(stock_code)

                trade_date_str = lhb.get("trade_date", "") or lhb.get("date", "")
                if trade_date_str:
                    if isinstance(trade_date_str, str):
                        if len(trade_date_str) == 10:
                            trade_date = datetime.strptime(
                                trade_date_str, "%Y-%m-%d"
                            ).date()
                        else:
                            trade_date = datetime.strptime(
                                trade_date_str, "%Y%m%d"
                            ).date()
                    else:
                        trade_date = trade_date_str
                else:
                    trade_date = current_date

                buy_details = lhb.get("buy_details", []) or lhb.get("buy_list", [])
                sell_details = lhb.get("sell_details", []) or lhb.get("sell_list", [])

                lhb_data = {
                    "trade_date": trade_date,
                    "stock_code": stock_code,
                    "stock_name": lhb.get("stock_name") or lhb.get("name"),
                    "full_code": full_code,
                    "market": "SH" if stock_code.startswith("6") else "SZ",
                    "close_price": lhb.get("close_price") or lhb.get("close"),
                    "change_percent": lhb.get("change_percent") or lhb.get("pct_chg"),
                    "turnover_rate": lhb.get("turnover_rate"),
                    "total_amount": lhb.get("total_amount") or lhb.get("amount"),
                    "net_buy_amount": lhb.get("net_buy_amount")
                    or lhb.get("net_amount"),
                    "net_buy_ratio": lhb.get("net_buy_ratio"),
                    "reason": lhb.get("reason") or lhb.get("exalt_reason"),
                    "buy_details": json.dumps(buy_details, ensure_ascii=False)
                    if buy_details
                    else None,
                    "sell_details": json.dumps(sell_details, ensure_ascii=False)
                    if sell_details
                    else None,
                    "buy_amount_total": lhb.get("buy_amount_total")
                    or lhb.get("buy_value"),
                    "sell_amount_total": lhb.get("sell_amount_total")
                    or lhb.get("sell_value"),
                    "data_from": "stock_service",
                    "data_time": current_time,
                }

                existing_sql = select(StockLonghubang).where(
                    StockLonghubang.stock_code == stock_code,
                    StockLonghubang.trade_date == trade_date,
                )
                result = await db.execute(existing_sql)
                existing = result.scalar_one_or_none()

                if existing:
                    del lhb_data["stock_code"]
                    del lhb_data["trade_date"]
                    update_stmt = (
                        update(StockLonghubang)
                        .where(StockLonghubang.id == existing.id)
                        .values(**lhb_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                    lhb_id = existing.id
                else:
                    new_lhb = StockLonghubang(**lhb_data)
                    db.add(new_lhb)
                    await db.flush()
                    lhb_id = new_lhb.id
                    added_count += 1

                all_details = []
                for detail in buy_details:
                    all_details.append(
                        {
                            "longhubang_id": lhb_id,
                            "trade_date": trade_date,
                            "stock_code": stock_code,
                            "stock_name": lhb.get("stock_name") or lhb.get("name"),
                            "trade_type": "buy",
                            "broker_name": detail.get("broker_name")
                            or detail.get("name"),
                            "broker_type": detail.get("broker_type")
                            or detail.get("type"),
                            "buy_amount": detail.get("buy_amount") or detail.get("buy"),
                            "sell_amount": detail.get("sell_amount")
                            or detail.get("sell"),
                            "net_amount": detail.get("net_amount") or detail.get("net"),
                            "data_from": "stock_service",
                            "data_time": current_time,
                        }
                    )

                for detail in sell_details:
                    all_details.append(
                        {
                            "longhubang_id": lhb_id,
                            "trade_date": trade_date,
                            "stock_code": stock_code,
                            "stock_name": lhb.get("stock_name") or lhb.get("name"),
                            "trade_type": "sell",
                            "broker_name": detail.get("broker_name")
                            or detail.get("name"),
                            "broker_type": detail.get("broker_type")
                            or detail.get("type"),
                            "buy_amount": detail.get("buy_amount") or detail.get("buy"),
                            "sell_amount": detail.get("sell_amount")
                            or detail.get("sell"),
                            "net_amount": detail.get("net_amount") or detail.get("net"),
                            "data_from": "stock_service",
                            "data_time": current_time,
                        }
                    )

                for detail_data in all_details:
                    existing_detail_sql = select(StockLonghubangDetail).where(
                        StockLonghubangDetail.longhubang_id == lhb_id,
                        StockLonghubangDetail.broker_name
                        == detail_data.get("broker_name"),
                        StockLonghubangDetail.trade_type
                        == detail_data.get("trade_type"),
                    )
                    detail_result = await db.execute(existing_detail_sql)
                    existing_detail = detail_result.scalar_one_or_none()

                    if existing_detail:
                        del detail_data["longhubang_id"]
                        del detail_data["broker_name"]
                        del detail_data["trade_type"]
                        update_detail_stmt = (
                            update(StockLonghubangDetail)
                            .where(StockLonghubangDetail.id == existing_detail.id)
                            .values(**detail_data)
                        )
                        await db.execute(update_detail_stmt)
                    else:
                        new_detail = StockLonghubangDetail(**detail_data)
                        db.add(new_detail)
                        detail_added_count += 1

            except Exception as e:
                print(f"处理龙虎榜数据 {stock_code} 失败: {str(e)}")
                traceback.print_exc()
                continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条龙虎榜数据，"
            f"新增 {detail_added_count} 条明细数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步龙虎榜数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_stock_chip_distribution(db: AsyncSession, limit: int = 100) -> dict:
    """
    同步股票筹码分布数据
    从 Stock Service 获取热门股票的筹码分布数据
    """
    try:
        print("开始从 Stock Service 同步股票筹码分布数据...")

        async with StockServiceClient() as client:
            stock_list = await client.get_all_stock_list()

        if not stock_list:
            return {"is_success": False, "message": "未获取到股票列表"}

        current_date = date.today()
        current_time = datetime.now()

        added_count = 0
        updated_count = 0
        error_count = 0

        for stock in stock_list[:limit]:
            try:
                stock_code = stock.get("code", "")
                if not stock_code:
                    continue

                full_code = StockUtils.get_full_code(stock_code)

                async with StockServiceClient() as client:
                    chip_data = await client.get_chip_distribution(stock_code)

                if not chip_data:
                    continue

                for chip in chip_data:
                    try:
                        profit_ratio = chip.get("profit_ratio")
                        if profit_ratio is None:
                            continue

                        chip_record = {
                            "stock_code": stock_code,
                            "full_code": full_code,
                            "stock_name": stock.get("name"),
                            "trade_date": current_date,
                            "profit_ratio": profit_ratio,
                            "avg_cost": chip.get("avg_cost", 0),
                            "cost_90_low": chip.get("cost_90pct_low", 0),
                            "cost_90_high": chip.get("cost_90pct_high", 0),
                            "concentration_90": chip.get("concentration_90", 0),
                            "cost_70_low": chip.get("cost_70pct_low", 0),
                            "cost_70_high": chip.get("cost_70pct_high", 0),
                            "concentration_70": chip.get("concentration_70", 0),
                            "data_time": current_time,
                            "data_from": "stock_service",
                        }

                        existing_sql = select(StockChipDistribution).where(
                            StockChipDistribution.stock_code == stock_code,
                            StockChipDistribution.trade_date == current_date,
                        )
                        result = await db.execute(existing_sql)
                        existing = result.scalar_one_or_none()

                        if existing:
                            del chip_record["stock_code"]
                            del chip_record["trade_date"]
                            update_stmt = (
                                update(StockChipDistribution)
                                .where(StockChipDistribution.id == existing.id)
                                .values(**chip_record)
                            )
                            await db.execute(update_stmt)
                            updated_count += 1
                        else:
                            new_chip = StockChipDistribution(**chip_record)
                            db.add(new_chip)
                            added_count += 1

                    except Exception as e:
                        print(f"处理筹码数据失败: {str(e)}")
                        continue

            except Exception as e:
                error_count += 1
                if error_count <= 5:
                    print(f"处理股票 {stock_code} 筹码分布失败: {str(e)}")
                continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条筹码分布数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步筹码分布数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_news(db: AsyncSession) -> dict:
    """
    同步新闻资讯数据
    从 Stock Service 获取全球财经快讯和财联社电报数据
    """
    try:
        print("开始从 Stock Service 同步新闻资讯数据...")

        current_time = datetime.now()
        added_count = 0
        updated_count = 0

        async with StockServiceClient() as client:
            global_news = await client.get_global_finance_news()
            cls_news = await client.get_cls_telegraph("全部")

        all_news = []

        for item in global_news:
            all_news.append(
                {
                    "source": "global_finance",
                    "data": item,
                }
            )

        for item in cls_news:
            all_news.append(
                {
                    "source": "cls_telegraph",
                    "data": item,
                }
            )

        for news_item in all_news:
            try:
                source = news_item.get("source", "")
                data = news_item.get("data", {})

                title = data.get("title") or data.get("content", "")[:250]
                if not title:
                    continue

                content = data.get("content") or data.get("digest", "") or title

                existing_sql = select(News).where(News.name == title)
                result = await db.execute(existing_sql)
                existing = result.scalar_one_or_none()

                news_data = {
                    "name": title,
                    "content": content,
                    "data_from": source,
                    "agent": "stock_service",
                    "is_send": 0,
                    "priority": 2 if data.get("level") == "重要" else 3,
                    "date_at": current_time,
                    "url": data.get("url"),
                    "tag": data.get("tag") or data.get("keywords"),
                    "category": data.get("column") or "财经",
                }

                if existing:
                    del news_data["name"]
                    update_stmt = (
                        update(News).where(News.id == existing.id).values(**news_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    new_news = News(**news_data)
                    db.add(new_news)
                    added_count += 1

            except Exception as e:
                print(f"处理新闻数据失败: {str(e)}")
                continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条新闻资讯数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步新闻资讯数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_stock_daily_ranking(db: AsyncSession) -> dict:
    """
    同步每日排行历史数据
    从 Stock Service 获取股票列表，计算各类排行并存储
    """
    try:
        print("开始同步每日排行历史数据...")

        async with StockServiceClient() as client:
            stock_list = await client.get_all_stock_list()

        if not stock_list:
            return {"is_success": False, "message": "未获取到股票列表"}

        current_date = date.today()
        current_time = datetime.now()

        ranking_types = ["change_percent", "turnover_rate", "volume", "amount"]

        sorted_stocks = {
            "change_percent": sorted(
                [s for s in stock_list if s.get("change_percent") is not None],
                key=lambda x: x.get("change_percent", 0),
                reverse=True,
            ),
            "turnover_rate": sorted(
                [s for s in stock_list if s.get("turnover_rate") is not None],
                key=lambda x: x.get("turnover_rate", 0),
                reverse=True,
            ),
            "volume": sorted(
                [s for s in stock_list if s.get("volume") is not None],
                key=lambda x: x.get("volume", 0),
                reverse=True,
            ),
            "amount": sorted(
                [s for s in stock_list if s.get("amount") is not None],
                key=lambda x: x.get("amount", 0),
                reverse=True,
            ),
        }

        added_count = 0
        updated_count = 0

        for ranking_type in ranking_types:
            for rank, stock in enumerate(sorted_stocks[ranking_type][:100], 1):
                try:
                    stock_code = stock.get("code", "")
                    if not stock_code:
                        continue

                    full_code = StockUtils.get_full_code(stock_code)

                    ranking_value = {
                        "change_percent": stock.get("change_percent"),
                        "turnover_rate": stock.get("turnover_rate"),
                        "volume": stock.get("volume"),
                        "amount": stock.get("amount"),
                    }.get(ranking_type)

                    ranking_data = {
                        "stock_code": stock_code,
                        "stock_name": stock.get("name"),
                        "full_code": full_code,
                        "ranking_type": ranking_type,
                        "rank": rank,
                        "ranking_value": ranking_value,
                        "current_price": stock.get("price"),
                        "change_percent": stock.get("change_percent"),
                        "change_amount": stock.get("change_amount"),
                        "volume": stock.get("volume"),
                        "amount": stock.get("amount"),
                        "turnover_rate": stock.get("turnover_rate"),
                        "total_market_cap": stock.get("market_cap"),
                        "circulating_market_cap": stock.get("circulating_market_cap"),
                        "data_date": current_date,
                        "data_source": "stock_service",
                        "market": "SH" if stock_code.startswith("6") else "SZ",
                    }

                    existing_sql = select(StockDailyRanking).where(
                        StockDailyRanking.stock_code == stock_code,
                        StockDailyRanking.data_date == current_date,
                        StockDailyRanking.ranking_type == ranking_type,
                    )
                    result = await db.execute(existing_sql)
                    existing = result.scalar_one_or_none()

                    if existing:
                        del ranking_data["stock_code"]
                        del ranking_data["data_date"]
                        del ranking_data["ranking_type"]
                        update_stmt = (
                            update(StockDailyRanking)
                            .where(StockDailyRanking.id == existing.id)
                            .values(**ranking_data)
                        )
                        await db.execute(update_stmt)
                        updated_count += 1
                    else:
                        new_ranking = StockDailyRanking(**ranking_data)
                        db.add(new_ranking)
                        added_count += 1

                except Exception as e:
                    print(f"处理排行数据失败: {str(e)}")
                    continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条每日排行数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步每日排行数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_stock_hot_rank_detail(db: AsyncSession) -> dict:
    """
    同步股票热度详情历史数据
    从 Stock Service 获取热度排名数据并存储详细历史
    """
    try:
        print("开始从 Stock Service 同步股票热度详情历史数据...")

        async with StockServiceClient() as client:
            hot_ranks = await client.get_stock_hot_rank()

        if not hot_ranks:
            return {"is_success": False, "message": "未获取到股票热度排名数据"}

        current_date = date.today()
        current_time = datetime.now()

        added_count = 0
        updated_count = 0

        for rank_data in hot_ranks:
            try:
                stock_code = rank_data.get("stock_code", "")
                if not stock_code:
                    continue

                full_code = StockUtils.get_full_code(stock_code)

                detail_data = {
                    "stock_code": stock_code,
                    "stock_name": rank_data.get("stock_name"),
                    "full_code": full_code,
                    "rank": rank_data.get("rank", 0),
                    "rank_change": rank_data.get("rank_change"),
                    "hot_value": rank_data.get("hot_value"),
                    "current_price": rank_data.get("price"),
                    "change_percent": rank_data.get("change_percent"),
                    "change_amount": rank_data.get("change"),
                    "volume": rank_data.get("volume"),
                    "amount": rank_data.get("amount"),
                    "turnover_rate": rank_data.get("turnover_rate"),
                    "data_date": current_date,
                    "data_time": current_time,
                    "data_from": "stock_service",
                }

                existing_sql = select(StockHotRankDetail).where(
                    StockHotRankDetail.stock_code == stock_code,
                    StockHotRankDetail.data_date == current_date,
                )
                result = await db.execute(existing_sql)
                existing = result.scalar_one_or_none()

                if existing:
                    del detail_data["stock_code"]
                    del detail_data["data_date"]
                    update_stmt = (
                        update(StockHotRankDetail)
                        .where(StockHotRankDetail.id == existing.id)
                        .values(**detail_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    new_detail = StockHotRankDetail(**detail_data)
                    db.add(new_detail)
                    added_count += 1

            except Exception as e:
                print(f"处理股票 {stock_code} 热度详情失败: {str(e)}")
                continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条热度详情数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步热度详情数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_stock_index(db: AsyncSession) -> dict:
    """
    同步大盘指数数据
    从 Stock Service 获取上证指数、深证成指、创业板指、科创50等主要指数数据
    """
    try:
        print("开始从 Stock Service 同步大盘指数数据...")

        async with StockServiceClient() as client:
            index_quotes = await client.get_index_quotes()

        if not index_quotes:
            return {"is_success": False, "message": "未获取到大盘指数数据"}

        current_date = date.today()
        current_time = datetime.now()

        updated_count = 0
        added_count = 0

        for quote in index_quotes:
            try:
                index_code = quote.get("code", "")
                if not index_code:
                    continue

                index_data = {
                    "index_code": index_code,
                    "index_name": quote.get("name"),
                    "open_price": quote.get("open"),
                    "high_price": quote.get("high"),
                    "low_price": quote.get("low"),
                    "close_price": quote.get("price"),
                    "pre_close": quote.get("pre_close"),
                    "change_percent": quote.get("change_percent"),
                    "change_amount": quote.get("change"),
                    "volume": quote.get("volume"),
                    "amount": quote.get("amount"),
                    "amplitude": quote.get("amplitude"),
                    "data_date": current_date,
                    "data_time": current_time,
                    "data_source": "stock_service",
                }

                existing_sql = select(StockIndex).where(
                    StockIndex.index_code == index_code,
                    StockIndex.data_date == current_date,
                )
                result = await db.execute(existing_sql)
                existing = result.scalar_one_or_none()

                if existing:
                    del index_data["index_code"]
                    del index_data["data_date"]
                    update_stmt = (
                        update(StockIndex)
                        .where(StockIndex.id == existing.id)
                        .values(**index_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    new_index = StockIndex(**index_data)
                    db.add(new_index)
                    added_count += 1

            except Exception as e:
                print(f"处理指数 {index_code} 数据失败: {str(e)}")
                traceback.print_exc()
                continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条大盘指数数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步大盘指数数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_stock_fund_flow(db: AsyncSession) -> dict:
    """
    同步个股资金流向数据
    从 Stock Service 获取个股资金流向数据
    注：此接口需要逐只股票调用，为提高效率，只获取股票列表中的前500只
    """
    try:
        print("开始从 Stock Service 同步个股资金流向数据...")

        async with StockServiceClient() as client:
            stock_list = await client.get_all_stock_list()

        if not stock_list:
            return {"is_success": False, "message": "未获取到股票列表"}

        current_date = date.today()
        current_time = datetime.now()

        existing_sql = select(StockFundFlow.stock_code).where(
            StockFundFlow.trade_date == current_date
        )
        result = await db.execute(existing_sql)
        existing_codes = set(result.scalars().all())

        added_count = 0
        updated_count = 0
        error_count = 0

        for stock in stock_list[:500]:
            try:
                stock_code = stock.get("code", "")
                if not stock_code:
                    continue

                async with StockServiceClient() as client:
                    fund_flow = await client.get_stock_fund_flow(stock_code)

                if not fund_flow or not fund_flow.get("main_net_inflow"):
                    continue

                full_code = StockUtils.get_full_code(stock_code)

                fund_data = {
                    "stock_code": stock_code,
                    "stock_name": stock.get("name"),
                    "full_code": full_code,
                    "trade_date": current_date,
                    "main_net_inflow": fund_flow.get("main_net_inflow", 0),
                    "main_net_inflow_percent": fund_flow.get(
                        "main_net_inflow_ratio", 0
                    ),
                    "super_large_net_inflow": fund_flow.get("super_net_inflow", 0),
                    "large_net_inflow": fund_flow.get("big_net_inflow", 0),
                    "medium_net_inflow": fund_flow.get("medium_net_inflow", 0),
                    "small_net_inflow": fund_flow.get("small_net_inflow", 0),
                    "data_time": current_time,
                    "data_from": "stock_service",
                }

                if stock_code in existing_codes:
                    del fund_data["stock_code"]
                    del fund_data["trade_date"]
                    update_stmt = (
                        update(StockFundFlow)
                        .where(StockFundFlow.stock_code == stock_code)
                        .where(StockFundFlow.trade_date == current_date)
                        .values(**fund_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    new_fund_flow = StockFundFlow(**fund_data)
                    db.add(new_fund_flow)
                    added_count += 1

            except Exception as e:
                error_count += 1
                if error_count <= 5:
                    print(f"处理股票 {stock_code} 资金流向失败: {str(e)}")
                continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条个股资金流向数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步个股资金流向数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_stock_hot_rank(db: AsyncSession) -> dict:
    """
    同步股票热度排名数据
    从 Stock Service 获取股票人气榜排名数据
    """
    try:
        print("开始从 Stock Service 同步股票热度排名数据...")

        async with StockServiceClient() as client:
            hot_ranks = await client.get_stock_hot_rank()

        if not hot_ranks:
            return {"is_success": False, "message": "未获取到股票热度排名数据"}

        current_date = date.today()
        current_time = datetime.now()

        existing_sql = select(StockHotRank.stock_code).where(
            StockHotRank.data_date == current_date
        )
        result = await db.execute(existing_sql)
        existing_codes = set(result.scalars().all())

        added_count = 0
        updated_count = 0

        for rank_data in hot_ranks:
            try:
                stock_code = rank_data.get("stock_code", "")
                if not stock_code:
                    continue

                full_code = StockUtils.get_full_code(stock_code)

                hot_rank_data = {
                    "stock_code": stock_code,
                    "stock_name": rank_data.get("stock_name"),
                    "full_code": full_code,
                    "rank": rank_data.get("rank", 0),
                    "rank_change": rank_data.get("rank_change"),
                    "current_price": rank_data.get("price"),
                    "change_amount": rank_data.get("change"),
                    "change_percent": rank_data.get("change_percent"),
                    "market": "SH" if stock_code.startswith("6") else "SZ",
                    "data_date": current_date,
                    "data_time": current_time,
                    "data_from": "stock_service",
                }

                if stock_code in existing_codes:
                    del hot_rank_data["stock_code"]
                    del hot_rank_data["data_date"]
                    update_stmt = (
                        update(StockHotRank)
                        .where(StockHotRank.stock_code == stock_code)
                        .where(StockHotRank.data_date == current_date)
                        .values(**hot_rank_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    new_hot_rank = StockHotRank(**hot_rank_data)
                    db.add(new_hot_rank)
                    added_count += 1

            except Exception as e:
                print(f"处理股票 {stock_code} 热度排名失败: {str(e)}")
                traceback.print_exc()
                continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条股票热度排名数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步股票热度排名数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_north_money(db: AsyncSession) -> dict:
    """
    同步北向资金历史流向数据
    从 Stock Service 获取北向资金历史数据
    """
    try:
        print("开始从 Stock Service 同步北向资金历史流向数据...")

        async with StockServiceClient() as client:
            north_money_list = await client.get_north_money_flow(days=30)

        if not north_money_list:
            return {"is_success": False, "message": "未获取到北向资金数据"}

        current_time = datetime.now()

        added_count = 0
        updated_count = 0

        for item in north_money_list:
            try:
                date_str = item.get("date", "")
                if not date_str:
                    continue

                if isinstance(date_str, str):
                    if len(date_str) == 10:
                        trade_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    else:
                        trade_date = datetime.strptime(date_str, "%Y%m%d").date()
                else:
                    trade_date = date_str

                north_data = {
                    "trade_date": trade_date,
                    "sh_buy_amount": None,
                    "sh_sell_amount": None,
                    "sh_net_amount": item.get("sh_hk_flow", 0) * 100000000,
                    "sz_buy_amount": None,
                    "sz_sell_amount": None,
                    "sz_net_amount": item.get("sz_hk_flow", 0) * 100000000,
                    "total_buy_amount": None,
                    "total_sell_amount": None,
                    "total_net_amount": item.get("total_flow", 0) * 100000000,
                    "data_time": current_time,
                    "data_from": "stock_service",
                }

                existing_sql = select(StockNorthMoney).where(
                    StockNorthMoney.trade_date == trade_date
                )
                result = await db.execute(existing_sql)
                existing = result.scalar_one_or_none()

                if existing:
                    del north_data["trade_date"]
                    update_stmt = (
                        update(StockNorthMoney)
                        .where(StockNorthMoney.id == existing.id)
                        .values(**north_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    new_north_money = StockNorthMoney(**north_data)
                    db.add(new_north_money)
                    added_count += 1

            except Exception as e:
                print(f"处理北向资金数据 {date_str} 失败: {str(e)}")
                traceback.print_exc()
                continue

        await db.commit()
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条北向资金历史数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步北向资金历史数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_north_money_realtime(db: AsyncSession) -> dict:
    """
    同步实时北向资金数据
    从 Stock Service 获取当日实时北向资金数据
    """
    try:
        print("开始从 Stock Service 同步实时北向资金数据...")

        async with StockServiceClient() as client:
            realtime_data = await client.get_realtime_north_money()

        if not realtime_data:
            return {"is_success": False, "message": "未获取到实时北向资金数据"}

        current_date = date.today()
        current_time = datetime.now()

        delete_stmt = delete(StockNorthMoneyRealtime).where(
            StockNorthMoneyRealtime.data_date == current_date
        )
        await db.execute(delete_stmt)

        realtime_record = StockNorthMoneyRealtime(
            data_date=current_date,
            sh_buy_amount=None,
            sh_sell_amount=None,
            sh_net_amount=realtime_data.get("sh_hk_flow", 0) * 100000000,
            sz_buy_amount=None,
            sz_sell_amount=None,
            sz_net_amount=realtime_data.get("sz_hk_flow", 0) * 100000000,
            total_buy_amount=None,
            total_sell_amount=None,
            total_net_amount=realtime_data.get("total_flow", 0) * 100000000,
            data_time=current_time,
            data_from="stock_service",
        )
        db.add(realtime_record)

        await db.commit()
        message = "成功同步实时北向资金数据"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步实时北向资金数据失败: {str(e)}")
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
        sql = select(StockRealtime.stock_code).where(
            StockRealtime.trade_date == current_date
        )
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
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条实时行情数据"
        )
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


async def get_board_concept_by_date(db: AsyncSession, current_date: datetime) -> list:
    """
    获取指定日期的概念板块名称列表
    """
    sql = select(StockBoardConcept.board_name).where(
        StockBoardConcept.date_at == current_date
    )
    queryset = await db.scalars(sql)
    return [i for i in queryset.all() if i]


async def get_board_industry_by_date(db: AsyncSession, current_date: datetime) -> list:
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


async def batch_board_concept_add(db: AsyncSession, board_models: list) -> None:
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


async def batch_board_concept_update(db: AsyncSession, board_data: list) -> None:
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
                    "previous_close": stock.get("price") - stock.get("change_amount")
                    if stock.get("price") and stock.get("change_amount")
                    else 0.0,
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
        message = (
            f"成功同步：新增 {added_count} 条，更新 {updated_count} 条实时行情数据"
        )
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步实时行情数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_margin_summary(db: AsyncSession) -> dict:
    """
    同步融资融券汇总数据
    从 Stock Service 获取融资融券汇总数据并存储
    """
    try:
        print("开始从 Stock Service 同步融资融券汇总数据...")

        async with StockServiceClient() as client:
            margin_data = await client.get_margin_summary()

        if not margin_data:
            return {"is_success": False, "message": "未获取到融资融券汇总数据"}

        current_time = datetime.now()
        trade_date_str = margin_data.get("trade_date", "")
        
        if trade_date_str:
            if len(trade_date_str) == 8:
                trade_date = datetime.strptime(trade_date_str, "%Y%m%d").date()
            else:
                trade_date = datetime.strptime(trade_date_str[:10], "%Y-%m-%d").date()
        else:
            trade_date = date.today()

        existing_sql = select(StockMarginSummary).where(
            StockMarginSummary.trade_date == trade_date
        )
        result = await db.execute(existing_sql)
        existing = result.scalar_one_or_none()

        margin_summary_data = {
            "trade_date": trade_date,
            "rzye": margin_data.get("rzye"),
            "rzmre": margin_data.get("rzmre"),
            "rzche": margin_data.get("rzche"),
            "rqye": margin_data.get("rqye"),
            "rqmcl": margin_data.get("rqmcl"),
            "rqchl": margin_data.get("rqchl"),
            "total": margin_data.get("total"),
            "data_time": current_time,
            "data_from": "stock_service",
        }

        if existing:
            del margin_summary_data["trade_date"]
            update_stmt = (
                update(StockMarginSummary)
                .where(StockMarginSummary.id == existing.id)
                .values(**margin_summary_data)
            )
            await db.execute(update_stmt)
            message = f"成功更新融资融券汇总数据，日期: {trade_date}"
        else:
            new_margin = StockMarginSummary(**margin_summary_data)
            db.add(new_margin)
            message = f"成功新增融资融券汇总数据，日期: {trade_date}"

        await db.commit()
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步融资融券汇总数据失败: {str(e)}")
        traceback.print_exc()
        raise e


async def sync_margin_detail(db: AsyncSession) -> dict:
    """
    同步融资融券明细数据
    从 Stock Service 获取融资融券明细数据并存储
    """
    try:
        print("开始从 Stock Service 同步融资融券明细数据...")

        async with StockServiceClient() as client:
            detail_list = await client.get_margin_detail()

        if not detail_list:
            return {"is_success": False, "message": "未获取到融资融券明细数据"}

        current_time = datetime.now()
        current_date = date.today()

        existing_sql = select(StockMarginDetail.stock_code).where(
            StockMarginDetail.trade_date == current_date
        )
        result = await db.execute(existing_sql)
        existing_codes = set(result.scalars().all())

        added_count = 0
        updated_count = 0

        for detail in detail_list:
            try:
                stock_code = detail.stock_code if hasattr(detail, 'stock_code') else detail.get("stock_code", "")
                if not stock_code:
                    continue

                full_code = StockUtils.get_full_code(stock_code)

                detail_data = {
                    "trade_date": current_date,
                    "stock_code": stock_code,
                    "stock_name": detail.stock_name if hasattr(detail, 'stock_name') else detail.get("stock_name"),
                    "full_code": full_code,
                    "rzye": detail.financing_balance if hasattr(detail, 'financing_balance') else detail.get("financing_balance"),
                    "rzmre": detail.financing_buy_amount if hasattr(detail, 'financing_buy_amount') else detail.get("financing_buy_amount"),
                    "rzche": detail.financing_repay_amount if hasattr(detail, 'financing_repay_amount') else detail.get("financing_repay_amount"),
                    "rqye": detail.securities_balance if hasattr(detail, 'securities_balance') else detail.get("securities_balance"),
                    "rqmcl": detail.securities_sell_volume if hasattr(detail, 'securities_sell_volume') else detail.get("securities_sell_volume"),
                    "rqchl": detail.securities_repay_volume if hasattr(detail, 'securities_repay_volume') else detail.get("securities_repay_volume"),
                    "data_time": current_time,
                    "data_from": "stock_service",
                }

                if stock_code in existing_codes:
                    del detail_data["stock_code"]
                    del detail_data["trade_date"]
                    update_stmt = (
                        update(StockMarginDetail)
                        .where(StockMarginDetail.stock_code == stock_code)
                        .where(StockMarginDetail.trade_date == current_date)
                        .values(**detail_data)
                    )
                    await db.execute(update_stmt)
                    updated_count += 1
                else:
                    new_detail = StockMarginDetail(**detail_data)
                    db.add(new_detail)
                    added_count += 1

            except Exception as e:
                print(f"处理融资融券明细 {stock_code} 失败: {str(e)}")
                continue

        await db.commit()
        message = f"成功同步：新增 {added_count} 条，更新 {updated_count} 条融资融券明细数据"
        print(message)
        return {"is_success": True, "message": message}

    except Exception as e:
        await db.rollback()
        print(f"同步融资融券明细数据失败: {str(e)}")
        traceback.print_exc()
        raise e
