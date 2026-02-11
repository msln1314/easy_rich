#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/2/11
# @File           : ak_service.py
# @IDE            : PyCharm
# @desc           : 股票数据采集服务

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Body, Request, Query
from utils.response import ErrorResponse, SuccessResponse
from apps.admin.auth.utils.current import AllUserAuth, FullAdminAuth, Auth, OpenAuth
from .models import StockBasicInfo, StockRealtime, StockBoardIndustry, StockBoardConcept
from .crud import (
    StockBaseInfoDal,
    StockRealtimeDal,
    StockBoardIndustryDal,
    StockBoardConceptDal,
)
from core.logger import logger
from core.dependencies import IdList
from core.exception import CustomException
from utils.helpers import date_range
from utils.akshare_service import AkShareService
import akshare as ak
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


###########################################################
#    股票基础信息同步
###########################################################


@router.get("/sync/basic", summary="同步股票基础信息")
async def sync_stock_basic_info(auth: Auth = Depends(OpenAuth())):
    """
    同步股票基础信息
    """
    try:
        dal = StockBaseInfoDal(auth.db)
        result = await dal.sync_from_akshare()
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"同步股票基础信息失败: {str(e)}")
        return ErrorResponse(f"同步股票基础信息失败: {str(e)}")


###########################################################
#    实时行情数据同步
###########################################################


@router.get("/sync/realtime", summary="同步实时行情数据")
async def sync_stock_realtime(auth: Auth = Depends(OpenAuth())):
    """
    同步实时行情数据
    """
    try:
        dal = StockRealtimeDal(auth.db)
        result = await dal.sync_realtime_data()
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"同步实时行情数据失败: {str(e)}")
        return ErrorResponse(f"同步实时行情数据失败: {str(e)}")


###########################################################
#    行业板块数据同步
###########################################################


@router.get("/sync/industry", summary="同步行业板块数据")
async def sync_stock_industry(auth: Auth = Depends(OpenAuth())):
    """
    同步行业板块数据
    """
    try:
        from .stock_board_industry import sync_industry_board_data

        result = await sync_industry_board_data()
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"同步行业板块数据失败: {str(e)}")
        return ErrorResponse(f"同步行业板块数据失败: {str(e)}")


###########################################################
#    概念板块数据同步
###########################################################


@router.get("/sync/concept", summary="同步概念板块数据")
async def sync_stock_concept(auth: Auth = Depends(OpenAuth())):
    """
    同步概念板块数据
    """
    try:
        from .stock_board_concept import sync_concept_board_data

        result = await sync_concept_board_data()
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"同步概念板块数据失败: {str(e)}")
        return ErrorResponse(f"同步概念板块数据失败: {str(e)}")


###########################################################
#    批量同步任务
###########################################################


@router.get("/sync/all", summary="批量同步所有股票数据")
async def sync_all_stock_data(auth: Auth = Depends(OpenAuth())):
    """
    批量同步所有股票数据
    """
    try:
        # 1. 同步基础信息
        basic_dal = StockBaseInfoDal(auth.db)
        basic_result = await basic_dal.sync_from_akshare()

        # 2. 同步实时行情
        realtime_dal = StockRealtimeDal(auth.db)
        realtime_result = await realtime_dal.sync_realtime_data()

        # 3. 同步行业板块
        from .stock_board_industry import sync_industry_board_data

        industry_result = await sync_industry_board_data()

        # 4. 同步概念板块
        from .stock_board_concept import sync_concept_board_data

        concept_result = await sync_concept_board_data()

        return SuccessResponse(
            {
                "basic_info": basic_result,
                "realtime_data": realtime_result,
                "industry_board": industry_result,
                "concept_board": concept_result,
            }
        )
    except Exception as e:
        logger.error(f"批量同步股票数据失败: {str(e)}")
        return ErrorResponse(f"批量同步股票数据失败: {str(e)}")


###########################################################
#    定时任务同步
###########################################################


@router.get("/schedule/sync", summary="定时任务同步")
async def schedule_sync(auth: Auth = Depends(OpenAuth())):
    """
    定时任务同步（每日执行）
    """
    try:
        # 1. 同步实时行情（每日更新）
        realtime_dal = StockRealtimeDal(auth.db)
        realtime_result = await realtime_dal.sync_realtime_data()

        # 2. 同步行业板块（每日更新）
        from .stock_board_industry import sync_industry_board_data

        industry_result = await sync_industry_board_data()

        # 3. 同步概念板块（每日更新）
        from .stock_board_concept import sync_concept_board_data

        concept_result = await sync_concept_board_data()

        return SuccessResponse(
            {
                "realtime_data": realtime_result,
                "industry_board": industry_result,
                "concept_board": concept_result,
            }
        )
    except Exception as e:
        logger.error(f"定时任务同步失败: {str(e)}")
        return ErrorResponse(f"定时任务同步失败: {str(e)}")


###########################################################
#    数据清理
###########################################################


@router.get("/cleanup", summary="清理过期数据")
async def cleanup_data(auth: Auth = Depends(FullAdminAuth())):
    """
    清理过期数据（保留最近30天）
    """
    try:
        # 清理实时行情数据（保留30天）
        realtime_dal = StockRealtimeDal(auth.db)
        cutoff_date = datetime.now() - timedelta(days=30)
        deleted_count = await realtime_dal.delete_old_data(cutoff_date)

        return SuccessResponse(f"已清理 {deleted_count} 条过期实时行情数据")
    except Exception as e:
        logger.error(f"清理数据失败: {str(e)}")
        return ErrorResponse(f"清理数据失败: {str(e)}")


###########################################################
#    辅助函数
###########################################################


async def get_board_concept_by_date(
    db: AsyncSession, current_date: datetime
) -> List[str]:
    """
    获取指定日期的概念板块名称列表
    """
    sql = select(StockBoardConcept.board_name).where(
        StockBoardConcept.date_at == current_date
    )
    queryset = await db.scalars(sql)
    return [i for i in queryset.all() if i]


async def batch_board_concept_add(
    db: AsyncSession, board_models: List[StockBoardConcept]
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
    db: AsyncSession, board_data: List[Dict[str, Any]]
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
