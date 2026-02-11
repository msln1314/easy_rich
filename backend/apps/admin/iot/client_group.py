# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from apps.admin.auth.utils.current import FullAdminAuth, Auth
from . import schemas, crud
from core.dependencies import IdList
from .params import ClientGroupParams

router = APIRouter()


###########################################################
#    设备分组管理
###########################################################
@router.get("", summary="获取设备分组列表")
async def get_groups(
        params: ClientGroupParams = Depends(),
        auth: Auth = Depends(FullAdminAuth())
):
    datas = await crud.ClientGroupDal(auth.db).get_tree_list(1)
    return SuccessResponse(datas)


@router.get("/tree/options", summary="获取设备分组树选择项，添加/修改设备分组时使用")
async def get_dept_options(auth: Auth = Depends(FullAdminAuth())):
    datas = await crud.ClientGroupDal(auth.db).get_tree_list(mode=2)
    return SuccessResponse(datas)


@router.get("/user/tree/options", summary="获取设备分组树选择项，添加/修改设备时使用")
async def get_dept_treeselect(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ClientGroupDal(auth.db).get_tree_list(mode=3))


@router.post("", summary="创建设备分组信息")
async def create_dept(data: schemas.ClientGroup, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.ClientGroupDal(auth.db).create_data(data=data))


@router.delete("", summary="批量删除设备分组", description="硬删除, 如果存在设备关联则无法删除")
async def delete_depts(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.ClientGroupDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新设备分组信息")
async def put_dept(
        data_id: int,
        data: schemas.ClientGroup,
        auth: Auth = Depends(FullAdminAuth())
):
    return SuccessResponse(await crud.ClientGroupDal(auth.db).put_data(data_id, data))
