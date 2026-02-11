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
from .params import DeptParams

router = APIRouter()


###########################################################
#    部门管理
###########################################################
@router.get("", summary="获取部门列表")
async def get_depts(
        params: DeptParams = Depends(),
        auth: Auth = Depends(FullAdminAuth())
):
    datas = await crud.DeptDal(auth.db).get_tree_list(1)
    return SuccessResponse(datas)


@router.get("/tree/options", summary="获取部门树选择项，添加/修改部门时使用")
async def get_dept_options(auth: Auth = Depends(FullAdminAuth())):
    datas = await crud.DeptDal(auth.db).get_tree_list(mode=2)
    return SuccessResponse(datas)


@router.get("/user/tree/options", summary="获取部门树选择项，添加/修改用户时使用")
async def get_dept_treeselect(auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.DeptDal(auth.db).get_tree_list(mode=3))


@router.post("", summary="创建部门信息")
async def create_dept(data: schemas.Dept, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.DeptDal(auth.db).create_data(data=data))


@router.delete("", summary="批量删除部门", description="硬删除, 如果存在用户关联则无法删除")
async def delete_depts(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.DeptDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新部门信息")
async def put_dept(
        data_id: int,
        data: schemas.Dept,
        auth: Auth = Depends(FullAdminAuth())
):
    return SuccessResponse(await crud.DeptDal(auth.db).put_data(data_id, data))
