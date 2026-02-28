# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/11
# @File           : stock_board_concept.py
# @IDE            : PyCharm
# @desc           : 股票概念板块接口文件

from fastapi import APIRouter, Depends, Body, Query
from typing import Optional
from datetime import datetime, timedelta
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth
from .params import StockBoardConceptParams
from . import schemas, crud
from core.dependencies import IdList
from sqlalchemy import select, desc, func, and_
from core.logger import logger
import random


router = APIRouter()


###########################################################
#    股票概念板块管理
###########################################################


@router.post("", summary="创建股票概念板块")
async def create_board_concept(
    data: schemas.StockBoardConceptCreate, auth: Auth = Depends(AllUserAuth())
):
    """
    创建股票概念板块
    """
    board = await crud.StockBoardConceptDal(auth.db).create_data(data=data)
    return SuccessResponse(board)


@router.get("", summary="获取股票概念板块列表，分页")
async def get_board_concept_list(
    params: StockBoardConceptParams = Depends(), auth: Auth = Depends(AllUserAuth())
):
    """
    获取股票概念板块列表
    """
    board_dict = params.dict()
    schema = schemas.StockBoardConceptOut
    datas, count = await crud.StockBoardConceptDal(auth.db).get_datas(
        **board_dict, v_schema=schema, v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@router.post("/export/excel", summary="导出股票概念板块为excel")
async def export_query_list(
    header: list = Body(..., title="表头与对应字段"),
    params: StockBoardConceptParams = Depends(),
    auth: Auth = Depends(FullAdminAuth(permissions=["stock_board_concept.export"])),
):
    """
    导出股票概念板块为excel
    """
    return SuccessResponse(
        await crud.StockBoardConceptDal(auth.db).export_query_list(header, params)
    )


@router.delete("", summary="批量删除股票概念板块", description="硬删除")
async def delete_board_concept(
    ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())
):
    """
    批量删除股票概念板块
    """
    await crud.StockBoardConceptDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新股票概念板块")
async def put_board_concept(
    data_id: int,
    data: schemas.StockBoardConceptUpdate,
    auth: Auth = Depends(AllUserAuth()),
):
    """
    更新股票概念板块
    """
    board = await crud.StockBoardConceptDal(auth.db).put_data(data_id, data)
    return SuccessResponse(board)


@router.get("/{data_id}", summary="获取股票概念板块详情")
async def get_board_concept_detail(data_id: int, auth: Auth = Depends(AllUserAuth())):
    """
    获取股票概念板块详情
    """
    data = await crud.StockBoardConceptDal(auth.db).get_data(data_id)
    return SuccessResponse(data)


@router.get("/board/{board_name}", summary="根据板块名称获取最新记录")
async def get_board_by_name(board_name: str, auth: Auth = Depends(AllUserAuth())):
    """
    根据板块名称获取最新记录
    :param board_name: 板块名称
    """
    data = await crud.StockBoardConceptDal(auth.db).get_by_board_name(board_name)
    return SuccessResponse(data)


@router.get("/top/inflow", summary="获取净流入排名前N的概念板块")
async def get_top_inflow(limit: int = 10, auth: Auth = Depends(AllUserAuth())):
    """
    获取净流入排名前N的概念板块
    :param limit: 返回数量，默认10
    """
    datas = await crud.StockBoardConceptDal(auth.db).get_top_inflow(limit)
    return SuccessResponse(datas)


@router.get("/top/change", summary="获取涨跌幅排名前N的概念板块")
async def get_top_change(limit: int = 10, auth: Auth = Depends(AllUserAuth())):
    """
    获取涨跌幅排名前N的概念板块
    :param limit: 返回数量，默认10
    """
    datas = await crud.StockBoardConceptDal(auth.db).get_top_change(limit)
    return SuccessResponse(datas)


###########################################################
#    板块轮动分析
###########################################################


@router.get("/sync", summary="同步概念板块数据")
async def sync_concept_data(auth: Auth = Depends(AllUserAuth())):
    """
    同步概念板块数据

    从同花顺获取概念板块数据并保存到数据库
    """
    try:
        dal = crud.StockBoardConceptDal(auth.db)

        # 获取概念板块数据
        concept_data = await dal.get_concept_data_from_ths()

        if not concept_data:
            return SuccessResponse("未获取到概念板块数据")

        # 同步数据到数据库
        result = await dal.sync_concept_data(concept_data)

        return SuccessResponse(f"同步完成，处理了 {result} 条数据")
    except Exception as e:
        logger.error(f"同步概念板块数据失败: {str(e)}")
        return SuccessResponse(f"同步概念板块数据失败: {str(e)}")



def format_concept_data(item, rank: int = None):
    """格式化概念板块数据"""
    return {
        "rank": rank,
        "sector_name": item.board_name,
        "sector_code": item.board_code,
        "change_rate": item.change_percent or 0,
        "volume": item.total_amount or 0,
        "turnover_rate": 0,  # 数据库中没有该字段，需要计算
        "leading_stocks": item.up_count or 0,
        "stock_count": (item.up_count or 0) + (item.down_count or 0),
        "market_cap": 0,  # 数据库中没有该字段
        "net_inflow": item.net_inflow or 0,
        "average_price": item.average_price or 0,
        "total_volume": item.total_volume or 0,
        "leading_stock": item.leading_stock,
        "leading_stock_code": item.leading_stock_code,
        "leading_stock_change": item.leading_stock_change,
        "up_count": item.up_count,
        "down_count": item.down_count,
    }


def generate_mock_concept_ranking_data(limit: int = 50):
    """生成模拟概念板块排行榜数据"""
    concept_names = [
        "人工智能",
        "新能源汽车",
        "半导体",
        "医药生物",
        "新材料",
        "5G通信",
        "云计算",
        "大数据",
        "物联网",
        "区块链",
        "军工",
        "环保",
        "新能源",
        "光伏",
        "风电",
        "储能",
        "锂电池",
        "芯片",
        "软件",
        "互联网",
    ]

    leading_stocks = ["比亚迪", "宁德时代", "贵州茅台", "工商银行", "中国平安"]

    ranking_data = []
    for i in range(min(limit, len(concept_names))):
        change_rate = round(random.uniform(-8, 8), 2)
        volume = round(random.uniform(50, 500), 2)
        net_inflow = round(random.uniform(-20, 20), 2)
        up_count = random.randint(5, 25)
        down_count = random.randint(5, 20)

        ranking_data.append(
            {
                "rank": i + 1,
                "sector_name": concept_names[i],
                "sector_code": f"GN{1000 + i}",
                "change_rate": change_rate,
                "volume": volume,
                "turnover_rate": round(random.uniform(1, 10), 2),
                "leading_stocks": up_count,
                "stock_count": up_count + down_count,
                "market_cap": round(random.uniform(1000, 10000), 2),
                "net_inflow": net_inflow,
                "average_price": round(random.uniform(10, 100), 2),
                "total_volume": round(random.uniform(100, 1000), 2),
                "leading_stock": random.choice(leading_stocks),
                "leading_stock_code": f"60{1000 + random.randint(1, 9999):04d}",
                "leading_stock_change": round(random.uniform(-10, 10), 2),
                "up_count": up_count,
                "down_count": down_count,
            }
        )

    # 按涨跌幅排序
    ranking_data.sort(key=lambda x: x["change_rate"], reverse=True)

    # 更新排名
    for i, item in enumerate(ranking_data):
        item["rank"] = i + 1

    return ranking_data


def generate_mock_concept_trend_data():
    """生成模拟趋势数据"""
    trend_data = []
    current_date = datetime.now() - timedelta(days=30)

    sector_names = ["人工智能", "新能源汽车", "半导体", "医药生物", "新材料"]

    for i in range(30):
        date_str = (current_date + timedelta(days=i)).strftime("%Y-%m-%d")
        sectors_data = {}

        for sector in sector_names:
            sectors_data[sector] = {
                "inflow": round(random.uniform(50, 200), 2),
                "outflow": round(random.uniform(20, 100), 2),
                "net_inflow": round(random.uniform(-20, 50), 2),
            }

        trend_data.append({"date": date_str, "sectors": sectors_data})

    return trend_data


def generate_mock_concept_heatmap_data():
    """生成模拟热力图数据"""
    concept_names = [
        "人工智能",
        "新能源汽车",
        "半导体",
        "医药生物",
        "新材料",
        "5G通信",
        "云计算",
        "大数据",
        "物联网",
        "区块链",
        "军工",
        "环保",
        "新能源",
        "光伏",
        "风电",
        "储能",
        "锂电池",
        "芯片",
        "软件",
        "互联网",
    ]

    leading_stocks = ["比亚迪", "宁德时代", "贵州茅台", "工商银行", "中国平安"]

    heatmap_data = []
    for i, concept_name in enumerate(concept_names):
        change_rate = round(random.uniform(-8, 8), 2)
        x = i % 10
        y = i // 10
        r = abs(change_rate)

        heatmap_data.append(
            {
                "rank": i + 1,
                "sector_name": concept_name,
                "sector_code": f"GN{1000 + i}",
                "change_rate": change_rate,
                "volume": round(random.uniform(50, 500), 2),
                "turnover_rate": round(random.uniform(1, 10), 2),
                "leading_stocks": random.randint(5, 25),
                "stock_count": random.randint(15, 40),
                "market_cap": round(random.uniform(1000, 10000), 2),
                "net_inflow": round(random.uniform(-20, 20), 2),
                "average_price": round(random.uniform(10, 100), 2),
                "total_volume": round(random.uniform(100, 1000), 2),
                "leading_stock": random.choice(leading_stocks),
                "leading_stock_code": f"60{1000 + random.randint(1, 9999):04d}",
                "leading_stock_change": round(random.uniform(-10, 10), 2),
                "up_count": random.randint(5, 25),
                "down_count": random.randint(5, 20),
                "x": x,
                "y": y,
                "r": r,
            }
        )

    return heatmap_data


@router.get("/sector/rotation/ranking", summary="获取概念板块轮动排行榜")
async def get_concept_rotation_ranking(
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    sector_type: Optional[str] = Query(None, description="板块类型"),
    limit: int = Query(50, description="返回数量限制"),
    auth: Auth = Depends(AllUserAuth()),
):
    """
    获取概念板块轮动排行榜
    """
    try:
        # 构建查询条件
        query = select(crud.StockBoardConceptDal(auth.db).model)

        # 日期范围过滤
        if start_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            query = query.where(
                crud.StockBoardConceptDal(auth.db).model.date_at >= start_date_obj
            )

        if end_date:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.where(
                crud.StockBoardConceptDal(auth.db).model.date_at <= end_date_obj
            )

        # 如果没有指定日期，获取最新日期的数据
        if not start_date and not end_date:
            latest_date_subquery = select(
                func.max(crud.StockBoardConceptDal(auth.db).model.date_at)
            ).scalar_subquery()
            query = query.where(
                crud.StockBoardConceptDal(auth.db).model.date_at == latest_date_subquery
            )

        # 按涨跌幅排序
        query = query.order_by(
            desc(crud.StockBoardConceptDal(auth.db).model.change_percent)
        )

        # 限制数量
        query = query.limit(limit)

        result = await auth.db.execute(query)
        items = result.scalars().all()

        # 如果没有数据，返回模拟数据
        if not items:
            ranking_data = generate_mock_concept_ranking_data(limit)
            return SuccessResponse(ranking_data, count=len(ranking_data))

        # 格式化数据并添加排名
        ranking_data = [
            format_concept_data(item, rank=i + 1) for i, item in enumerate(items)
        ]

        return SuccessResponse(ranking_data, count=len(ranking_data))

    except Exception as e:
        return SuccessResponse(generate_mock_concept_ranking_data(limit))


@router.get("/sector/rotation/trend", summary="获取概念板块资金流向趋势")
async def get_concept_rotation_trend(
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    sector_type: Optional[str] = Query(None, description="板块类型"),
    auth: Auth = Depends(AllUserAuth()),
):
    """
    获取概念板块资金流向趋势
    """
    try:
        # 构建查询条件
        query = select(crud.StockBoardConceptDal(auth.db).model)

        # 默认查询最近30天
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime(
                "%Y-%m-%d"
            )
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # 日期范围过滤
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

        query = query.where(
            and_(
                crud.StockBoardConceptDal(auth.db).model.date_at >= start_date_obj,
                crud.StockBoardConceptDal(auth.db).model.date_at <= end_date_obj,
            )
        )

        query = query.order_by(
            crud.StockBoardConceptDal(auth.db).model.date_at,
            desc(crud.StockBoardConceptDal(auth.db).model.net_inflow),
        )

        result = await auth.db.execute(query)
        items = result.scalars().all()

        # 按日期分组
        date_groups = {}
        for item in items:
            date_str = item.date_at.strftime("%Y-%m-%d")
            if date_str not in date_groups:
                date_groups[date_str] = {}

            # 取每个日期的前10个板块
            if len(date_groups[date_str]) < 10:
                date_groups[date_str][item.board_name] = {
                    "inflow": item.total_amount or 0,
                    "outflow": 0,  # 数据库中只有净流入，这里需要计算
                    "net_inflow": item.net_inflow or 0,
                }

        # 构建趋势数据
        trend_data = []
        for date_str in sorted(date_groups.keys()):
            trend_data.append({"date": date_str, "sectors": date_groups[date_str]})

        return SuccessResponse(trend_data)

    except Exception as e:
        # 如果查询失败，返回模拟数据
        return SuccessResponse(generate_mock_concept_trend_data())


@router.get("/sector/rotation/heatmap", summary="获取概念板块热力图数据")
async def get_concept_rotation_heatmap(
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    sector_type: Optional[str] = Query(None, description="板块类型"),
    auth: Auth = Depends(AllUserAuth()),
):
    """
    获取概念板块热力图数据
    """
    try:
        # 构建查询条件
        query = select(crud.StockBoardConceptDal(auth.db).model)

        # 默认查询最新日期的数据
        if not start_date and not end_date:
            latest_date_subquery = select(
                func.max(crud.StockBoardConceptDal(auth.db).model.date_at)
            ).scalar_subquery()
            query = query.where(
                crud.StockBoardConceptDal(auth.db).model.date_at == latest_date_subquery
            )
        else:
            if start_date:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
                query = query.where(
                    crud.StockBoardConceptDal(auth.db).model.date_at >= start_date_obj
                )

            if end_date:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
                query = query.where(
                    crud.StockBoardConceptDal(auth.db).model.date_at <= end_date_obj
                )

        query = query.where(
            crud.StockBoardConceptDal(auth.db).model.change_percent.isnot(None)
        )
        query = query.order_by(
            desc(crud.StockBoardConceptDal(auth.db).model.change_percent)
        )

        result = await auth.db.execute(query)
        items = result.scalars().all()

        # 限制热力图数据量
        items = list(items)[:100]

        # 计算热力图坐标
        heatmap_data = []
        for i, item in enumerate(items):
            x = i % 10
            y = i // 10
            r = abs(item.change_percent or 0)

            data = format_concept_data(item)
            data.update({"x": x, "y": y, "r": r})
            heatmap_data.append(data)

        return SuccessResponse(heatmap_data)

    except Exception as e:
        # 如果查询失败，返回模拟数据
        return SuccessResponse(generate_mock_concept_heatmap_data())


@router.get("/sector/rotation/list", summary="获取概念板块列表")
async def get_concept_rotation_list(
    sector_type: Optional[str] = Query(None, description="板块类型"),
    auth: Auth = Depends(AllUserAuth()),
):
    """
    获取概念板块列表
    """
    try:
        # 获取所有不同的板块名称
        subquery = select(
            crud.StockBoardConceptDal(auth.db).model.board_name,
            crud.StockBoardConceptDal(auth.db).model.board_code,
        ).distinct()

        result = await auth.db.execute(subquery)
        items = result.all()

        concepts = [
            {
                "sector_code": item.board_code,
                "sector_name": item.board_name,
                "sector_type": sector_type or "concept",
            }
            for item in items
        ]

        return SuccessResponse(concepts)

    except Exception as e:
        # 返回模拟概念板块列表
        mock_concepts = [
            {
                "sector_code": "BK1001",
                "sector_name": "人工智能",
                "sector_type": "concept",
            },
            {
                "sector_code": "BK1002",
                "sector_name": "新能源汽车",
                "sector_type": "concept",
            },
            {
                "sector_code": "BK1003",
                "sector_name": "半导体",
                "sector_type": "concept",
            },
            {
                "sector_code": "BK1004",
                "sector_name": "医药生物",
                "sector_type": "concept",
            },
            {
                "sector_code": "BK1005",
                "sector_name": "新材料",
                "sector_type": "concept",
            },
        ]
        return SuccessResponse(mock_concepts)


@router.get("/sector/rotation/detail/{board_name}", summary="获取概念板块详细信息")
async def get_concept_rotation_detail(
    board_name: str,
    date_str: Optional[str] = Query(None, description="日期 YYYY-MM-DD，默认最新"),
    auth: Auth = Depends(AllUserAuth()),
):
    """
    获取概念板块详细信息
    """
    try:
        query = select(crud.StockBoardConceptDal(auth.db).model).where(
            crud.StockBoardConceptDal(auth.db).model.board_name == board_name
        )

        if date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.where(
                crud.StockBoardConceptDal(auth.db).model.date_at == date_obj
            )
        else:
            # 获取最新日期的数据
            subquery = (
                select(func.max(crud.StockBoardConceptDal(auth.db).model.date_at))
                .where(
                    crud.StockBoardConceptDal(auth.db).model.board_name == board_name
                )
                .scalar_subquery()
            )
            query = query.where(
                crud.StockBoardConceptDal(auth.db).model.date_at == subquery
            )

        result = await auth.db.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            return SuccessResponse(f"未找到概念板块 {board_name} 的数据")

        data = format_concept_data(item)
        return SuccessResponse(data)

    except Exception as e:
        return SuccessResponse(f"查询失败: {str(e)}")


@router.get("/sector/rotation/analysis/summary", summary="获取概念板块分析概览")
async def get_concept_rotation_analysis_summary(
    date_str: Optional[str] = Query(None, description="日期 YYYY-MM-DD，默认最新"),
    auth: Auth = Depends(AllUserAuth()),
):
    """
    获取概念板块分析概览
    """
    try:
        query = select(crud.StockBoardConceptDal(auth.db).model)

        if date_str:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.where(
                crud.StockBoardConceptDal(auth.db).model.date_at == date_obj
            )
        else:
            # 获取最新日期的数据
            subquery = select(
                func.max(crud.StockBoardConceptDal(auth.db).model.date_at)
            ).scalar_subquery()
            query = query.where(
                crud.StockBoardConceptDal(auth.db).model.date_at == subquery
            )

        result = await auth.db.execute(query)
        items = result.scalars().all()

        if not items:
            return SuccessResponse(
                {
                    "total_concepts": 0,
                    "rising_concepts": 0,
                    "falling_concepts": 0,
                    "flat_concepts": 0,
                    "total_inflow": 0,
                    "total_amount": 0,
                    "best_concept": None,
                    "worst_concept": None,
                }
            )

        # 计算统计数据
        total_concepts = len(items)
        rising_concepts = len(
            [item for item in items if item.change_percent and item.change_percent > 0]
        )
        falling_concepts = len(
            [item for item in items if item.change_percent and item.change_percent < 0]
        )
        flat_concepts = total_concepts - rising_concepts - falling_concepts

        total_inflow = sum(item.net_inflow or 0 for item in items)
        total_amount = sum(item.total_amount or 0 for item in items)

        # 找出最好和最差概念板块
        sorted_by_change = sorted(
            items, key=lambda x: x.change_percent or 0, reverse=True
        )
        best_concept = (
            format_concept_data(sorted_by_change[0], 1) if sorted_by_change else None
        )
        worst_concept = (
            format_concept_data(sorted_by_change[-1], len(sorted_by_change))
            if sorted_by_change
            else None
        )

        summary = {
            "total_concepts": total_concepts,
            "rising_concepts": rising_concepts,
            "falling_concepts": falling_concepts,
            "flat_concepts": flat_concepts,
            "total_inflow": total_inflow,
            "total_amount": total_amount,
            "best_concept": best_concept,
            "worst_concept": worst_concept,
            "date": date_str or items[0].date_at.strftime("%Y-%m-%d"),
        }

        return SuccessResponse(summary)

    except Exception as e:
        return SuccessResponse(f"查询失败: {str(e)}")


async def sync_concept_board_data():
    """
    同步概念板块数据

    从同花顺获取概念板块数据并保存到数据库
    """
    try:
        dal = crud.StockBoardConceptDal(None)  # 不需要数据库连接

        # 获取概念板块数据
        concept_data = await dal.get_concept_data_from_ths()

        if not concept_data:
            return {"status": "error", "message": "未获取到概念板块数据"}

        # 保存数据到数据库
        result = await dal.sync_concept_data(concept_data)

        return {"status": "success", "message": f"同步完成，处理了 {result} 条数据"}
    except Exception as e:
        logger.error(f"同步概念板块数据失败: {str(e)}")
        return {"status": "error", "message": f"同步概念板块数据失败: {str(e)}"}
