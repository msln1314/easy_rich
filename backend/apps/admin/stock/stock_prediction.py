# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2025/02/05
# @File           : stock_prediction.py
# @IDE            : PyCharm
# @desc           : 股票价格预测接口文件


from fastapi import APIRouter, Depends
from utils.response import SuccessResponse, ErrorResponse
from apps.admin.auth.utils.current import AllUserAuth, Auth
from .params import PredictionParams
from .schemas import PredictionOut, PredictionError
from services.prediction_service import PredictionService  # pyright: ignore[reportDeprecated]
router = APIRouter()

###########################################################
#    股票价格预测
###########################################################


# 全局预测服务实例（单例模式，避免重复加载模型）
_prediction_service: PredictionService | None = None

def get_prediction_service() -> PredictionService:
    """依赖注入：提供预测服务实例（单例模式）"""
    global _prediction_service
    if _prediction_service is None:
        _prediction_service = PredictionService()
    return _prediction_service


@router.post("/price_predict", summary="股票价格预测")
async def predict_stock_price(
    request: PredictionParams,
    service: PredictionService = Depends(get_prediction_service),
    auth: Auth = Depends(AllUserAuth())
):
    """
    使用 Kronos 时间序列模型预测股票价格
    """
    # 验证股票代码格式
    if not request.stock_code or len(request.stock_code.strip()) == 0:
        return ErrorResponse("股票代码不能为空")

    try:
        # 获取历史数据
        historical_data = await service._get_historical_data(request.stock_code, request.historical_days)
        # 执行预测
        result = await service.predict_stock_price(request, historical_data)

        return SuccessResponse(result.model_dump())

    except PredictionError as e:
        return ErrorResponse(str(e))
    except ValueError as e:
        return ErrorResponse(f"参数错误: {str(e)}")
    except Exception as e:
        print(e)
        return ErrorResponse("预测服务内部错误")


