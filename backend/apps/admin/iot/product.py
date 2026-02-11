# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import FullAdminAuth, Auth
from . import schemas, crud, models
from core.dependencies import IdList
from .params import ProductParams
from sqlalchemy.orm import joinedload
router = APIRouter()


###########################################################
#    产品管理
###########################################################
@router.get("", summary="获取设备分组列表")
async def get_products(
        params: ProductParams = Depends(),
        auth: Auth = Depends(FullAdminAuth())
):
    model = models.IotClient
    product_dict = params.dict()
    options = [joinedload(model.cate)]
    datas, count = await crud.ProductDal(auth.db).get_datas(**product_dict,  v_options=options,
                                                          v_return_count=True)
    return SuccessResponse(datas, count=count)



@router.get("/options", summary="获取产品选择项")
async def get_product_options(params: ProductParams = Depends(),auth: Auth = Depends(FullAdminAuth(permissions=["iot.product.create", "iot.product.update",]))):

    datas = await crud.ProductDal(auth.db).get_select_datas()
    return SuccessResponse(datas)

@router.post("", summary="创建产品信息")
async def create_product(data: schemas.Product, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ProductDal(auth.db).create_data(data=data))


@router.delete("", summary="批量删除设备分组", description="硬删除, 如果存在设备关联则无法删除")
async def delete_product(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.ProductDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新设备分组信息")
async def put_product(
        data_id: int,
        data: schemas.Product,
        auth: Auth = Depends(FullAdminAuth())
):
    return SuccessResponse(await crud.ProductDal(auth.db).put_data(data_id, data))
