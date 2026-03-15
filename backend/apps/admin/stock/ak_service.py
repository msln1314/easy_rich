#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/2/11
# @File           : ak_service.py
# @IDE            : PyCharm
# @desc           : 股票数据采集服务 - 通过 Stock Service 获取数据

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
from sqlalchemy.ext.asyncio import AsyncSession
from apps.module_task.task_service import (
    sync_stock_base_info,
    sync_realtime_data,
    sync_board_industry_from_akshare,
    sync_board_concept_from_akshare,
)

router = APIRouter()


###########################################################
#    股票基础信息同步
###########################################################


@router.get("/sync/basic", summary="同步股票基础信息")
async def sync_stock_basic_info_api(auth: Auth = Depends(OpenAuth())):
    """
    同步股票基础信息（从 Stock Service 获取）
    """
    try:
        result = await sync_stock_base_info(auth.db)
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"同步股票基础信息失败: {str(e)}")
        return ErrorResponse(f"同步股票基础信息失败: {str(e)}")


###########################################################
#    实时行情数据同步
###########################################################


@router.get("/sync/realtime", summary="同步实时行情数据")
async def sync_stock_realtime_api(auth: Auth = Depends(OpenAuth())):
    """
    同步实时行情数据（从 Stock Service 获取）
    """
    try:
        result = await sync_realtime_data(auth.db)
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"同步实时行情数据失败: {str(e)}")
        return ErrorResponse(f"同步实时行情数据失败: {str(e)}")


###########################################################
#    行业板块数据同步
###########################################################


@router.get("/sync/industry", summary="同步行业板块数据")
async def sync_stock_industry_api(auth: Auth = Depends(OpenAuth())):
    """
    同步行业板块数据（从 Stock Service 获取）
    """
    try:
        result = await sync_board_industry_from_akshare(auth.db)
        return SuccessResponse(result)
    except Exception as e:
        logger.error(f"同步行业板块数据失败: {str(e)}")
        return ErrorResponse(f"同步行业板块数据失败: {str(e)}")


###########################################################
#    概念板块数据同步
###########################################################


@router.get("/sync/concept", summary="同步概念板块数据")
async def sync_stock_concept_api(auth: Auth = Depends(OpenAuth())):
    """
    同步概念板块数据（从 Stock Service 获取）
    """
    try:
        result = await sync_board_concept_from_akshare(auth.db)
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
    批量同步所有股票数据（从 Stock Service 获取）
    """
    try:
        # 1. 同步基础信息
        basic_result = await sync_stock_base_info(auth.db)

        # 2. 同步实时行情
        realtime_result = await sync_realtime_data(auth.db)

        # 3. 同步行业板块
        industry_result = await sync_board_industry_from_akshare(auth.db)

        # 4. 同步概念板块
        concept_result = await sync_board_concept_from_akshare(auth.db)

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
    定时任务同步（每日执行，从 Stock Service 获取）
    """
    try:
        # 1. 同步实时行情（每日更新）
        realtime_result = await sync_realtime_data(auth.db)

        # 2. 同步行业板块（每日更新）
        industry_result = await sync_board_industry_from_akshare(auth.db)

        # 3. 同步概念板块（每日更新）
        concept_result = await sync_board_concept_from_akshare(auth.db)

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
