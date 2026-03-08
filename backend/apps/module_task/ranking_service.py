#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
个股排行数据采集服务
每日收盘后采集各类排行数据并存储到历史表
"""

import traceback
from datetime import datetime, date
from typing import List, Dict, Optional
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from apps.admin.stock.models.stock_basic_info import StockBasicInfo
from apps.admin.stock.models.stock_hot_rank import StockHotRank
from apps.admin.stock.models.stock_daily_ranking import StockDailyRanking
from apps.admin.stock.params.stock_daily_ranking import DailyRankingType


# 排行类型与数据库字段的映射
RANKING_FIELD_MAP = {
    DailyRankingType.VOLUME: {
        "field": StockBasicInfo.volume,
        "unit": "手",
        "name": "成交量",
    },
    DailyRankingType.TURNOVER: {
        "field": StockBasicInfo.turnover_rate,
        "unit": "%",
        "name": "换手率",
    },
    DailyRankingType.AMOUNT: {
        "field": StockBasicInfo.amount,
        "unit": "元",
        "name": "成交额",
    },
    DailyRankingType.CHANGE_PERCENT: {
        "field": StockBasicInfo.change_percent,
        "unit": "%",
        "name": "涨跌幅",
    },
}


async def collect_daily_ranking(
    db: AsyncSession, ranking_type: DailyRankingType, target_date: Optional[date] = None
) -> Dict:
    """
    采集单类排行数据并存储到历史表

    Args:
        db: 数据库会话
        ranking_type: 排行类型
        target_date: 目标日期，默认今天

    Returns:
        操作结果
    """
    if target_date is None:
        target_date = date.today()

    try:
        print(f"开始采集 {target_date} {ranking_type.value} 排行数据...")

        # 获取排行配置
        ranking_config = RANKING_FIELD_MAP.get(ranking_type)
        if not ranking_config and ranking_type != DailyRankingType.HOT:
            return {
                "is_success": False,
                "message": f"不支持的排行类型: {ranking_type.value}",
            }

        # 获取需要采集的股票（上市的且交易中的）
        query = select(StockBasicInfo).filter(
            StockBasicInfo.status == "L", StockBasicInfo.trade_status == "交易中"
        )

        if ranking_type == DailyRankingType.HOT:
            # 热度排行从 StockHotRank 表获取
            hot_query = (
                select(StockHotRank)
                .filter(StockHotRank.data_date == target_date)
                .order_by(StockHotRank.rank)
            )
            result = await db.execute(hot_query)
            hot_stocks = result.scalars().all()
            return await _save_hot_ranking(db, hot_stocks, target_date)
        else:
            # 其他排行从 StockBasicInfo 获取
            ranking_field = ranking_config["field"]
            query = query.order_by(desc(ranking_field)).limit(5000)
            result = await db.execute(query)
            stocks = result.scalars().all()
            return await _save_ranking(
                db, stocks, ranking_type, ranking_config, target_date
            )

    except Exception as e:
        await db.rollback()
        print(f"采集 {ranking_type.value} 排行数据失败: {str(e)}")
        traceback.print_exc()
        return {"is_success": False, "message": str(e)}


async def _save_ranking(
    db: AsyncSession,
    stocks: List[StockBasicInfo],
    ranking_type: DailyRankingType,
    ranking_config: Dict,
    target_date: date,
) -> Dict:
    """保存排行数据到历史表"""
    ranking_field = ranking_config["field"]
    unit = ranking_config["unit"]

    added_count = 0
    updated_count = 0

    for idx, stock in enumerate(stocks):
        try:
            # 获取当前值
            current_value = getattr(stock, ranking_field.name)
            if current_value is None:
                continue

            # 查询是否已存在该记录
            exist_query = select(StockDailyRanking).filter(
                StockDailyRanking.stock_code == stock.stock_code,
                StockDailyRanking.data_date == target_date,
                StockDailyRanking.ranking_type == ranking_type.value,
            )
            exist_result = await db.execute(exist_query)
            existing = exist_result.scalar_one_or_none()

            # 构建数据
            ranking_data = {
                "stock_code": stock.stock_code,
                "stock_name": stock.stock_name,
                "full_code": stock.full_code,
                "ranking_type": ranking_type.value,
                "rank": idx + 1,
                "ranking_value": float(current_value) if current_value else None,
                "ranking_value_unit": unit,
                "market": stock.market,
                "industry": stock.industry,
                "current_price": stock.current_price,
                "change_percent": stock.change_percent,
                "change_amount": stock.change_amount,
                "volume": stock.volume,
                "amount": stock.amount,
                "turnover_rate": stock.turnover_rate,
                "total_market_cap": stock.total_market_cap,
                "circulating_market_cap": stock.circulating_market_cap,
                "data_date": target_date,
                "data_source": "akshare",
            }

            if existing:
                # 更新现有记录（保留排名变化）
                ranking_data["rank_change"] = existing.rank - ranking_data["rank"]
                for key, value in ranking_data.items():
                    if value is not None:
                        setattr(existing, key, value)
                updated_count += 1
            else:
                # 新增记录
                new_ranking = StockDailyRanking(**ranking_data)
                db.add(new_ranking)
                added_count += 1

        except Exception as e:
            print(f"处理股票 {stock.stock_code} 排行数据失败: {str(e)}")
            continue

    await db.commit()
    message = f"成功采集 {ranking_config['name']} 排行：新增 {added_count} 条，更新 {updated_count} 条"
    print(message)
    return {"is_success": True, "message": message}


async def _save_hot_ranking(
    db: AsyncSession, hot_stocks: List[StockHotRank], target_date: date
) -> Dict:
    """保存热度排行数据"""
    added_count = 0
    updated_count = 0

    for idx, hot in enumerate(hot_stocks):
        try:
            # 查询是否已存在
            exist_query = select(StockDailyRanking).filter(
                StockDailyRanking.stock_code == hot.stock_code,
                StockDailyRanking.data_date == target_date,
                StockDailyRanking.ranking_type == DailyRankingType.HOT.value,
            )
            exist_result = await db.execute(exist_query)
            existing = exist_result.scalar_one_or_none()

            # 构建数据
            ranking_data = {
                "stock_code": hot.stock_code,
                "stock_name": hot.stock_name,
                "full_code": hot.full_code,
                "ranking_type": DailyRankingType.HOT.value,
                "rank": hot.rank,
                "rank_change": hot.rank_change,
                "ranking_value": hot.change_percent,
                "ranking_value_unit": "%",
                "market": hot.market,
                "current_price": hot.current_price,
                "change_percent": hot.change_percent,
                "change_amount": hot.change_amount,
                "hot_value": hot.rank_change,
                "data_date": target_date,
                "data_source": hot.data_from,
            }

            if existing:
                for key, value in ranking_data.items():
                    if value is not None:
                        setattr(existing, key, value)
                updated_count += 1
            else:
                new_ranking = StockDailyRanking(**ranking_data)
                db.add(new_ranking)
                added_count += 1

        except Exception as e:
            print(f"处理热度股票 {hot.stock_code} 失败: {str(e)}")
            continue

    await db.commit()
    message = f"成功采集热度排行：新增 {added_count} 条，更新 {updated_count} 条"
    print(message)
    return {"is_success": True, "message": message}


async def collect_all_rankings(
    db: AsyncSession,
    target_date: Optional[date] = None,
    ranking_types: Optional[List[DailyRankingType]] = None,
) -> Dict:
    """
    采集所有类型的排行数据

    Args:
        db: 数据库会话
        target_date: 目标日期
        ranking_types: 要采集的排行类型列表，默认采集所有类型

    Returns:
        汇总结果
    """
    if target_date is None:
        target_date = date.today()

    if ranking_types is None:
        ranking_types = list(DailyRankingType)

    results = {
        "date": str(target_date),
        "total_success": 0,
        "total_failed": 0,
        "details": [],
    }

    for ranking_type in ranking_types:
        result = await collect_daily_ranking(db, ranking_type, target_date)
        if result["is_success"]:
            results["total_success"] += 1
        else:
            results["total_failed"] += 1
        results["details"].append(
            {
                "type": ranking_type.value,
                "success": result["is_success"],
                "message": result.get("message", ""),
            }
        )

    return {
        "is_success": results["total_failed"] == 0,
        "message": f"采集完成：成功 {results['total_success']} 类，失败 {results['total_failed']} 类",
        "data": results,
    }


async def get_previous_ranking(
    db: AsyncSession, stock_code: str, ranking_type: DailyRankingType, target_date: date
) -> Optional[StockDailyRanking]:
    """获取指定股票某日的排行数据（用于计算排名变化）"""
    query = select(StockDailyRanking).filter(
        StockDailyRanking.stock_code == stock_code,
        StockDailyRanking.ranking_type == ranking_type.value,
        StockDailyRanking.data_date == target_date,
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def sync_rankings_from_realtime(
    db: AsyncSession, target_date: Optional[date] = None
) -> Dict:
    """
    从实时行情数据同步排行数据到历史表
    每日收盘后调用，确保数据完整性
    """
    if target_date is None:
        target_date = date.today()

    print(f"开始同步 {target_date} 排行数据...")

    # 先同步实时行情数据
    from apps.module_task.task_service import sync_stock_realtime_to_basic

    sync_result = await sync_stock_realtime_to_basic(db)

    if not sync_result["is_success"]:
        return {"is_success": False, "message": "同步实时行情失败，无法采集排行数据"}

    # 再采集排行数据
    ranking_types = [
        DailyRankingType.VOLUME,
        DailyRankingType.TURNOVER,
        DailyRankingType.AMOUNT,
        DailyRankingType.CHANGE_PERCENT,
    ]
    result = await collect_all_rankings(db, target_date, ranking_types)

    return {
        "is_success": result["is_success"],
        "message": f"排行数据同步完成：{result['message']}",
        "data": {"realtime_sync": sync_result, "ranking_collect": result},
    }
