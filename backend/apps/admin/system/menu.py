# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import schemas, crud
from core.dependencies import IdList
from apps.admin.auth.utils.current import FullAdminAuth, Auth

router = APIRouter()



###########################################################
#    菜单管理
###########################################################
@router.get("", summary="获取菜单列表")
async def get_menus(auth: Auth = Depends(FullAdminAuth(permissions=["sys.menu.list"]))):

    datas = await crud.MenuDal(auth.db).get_tree_list(mode=1)
    return SuccessResponse(datas)


@router.get("/tree/options", summary="获取菜单树选择项，添加/修改菜单时使用")
async def get_menus_options(auth: Auth = Depends(FullAdminAuth(permissions=["sys.menu.create", "sys.menu.update"]))):
    datas = await crud.MenuDal(auth.db).get_tree_list(mode=2)
    return SuccessResponse(datas)


@router.get("/role/tree/options", summary="获取菜单列表树信息，角色权限使用")
async def get_menus_treeselect(
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.role.create", "sys.role.update"]))
):
    return SuccessResponse(await crud.MenuDal(auth.db).get_tree_list(mode=3))


@router.post("", summary="创建菜单信息")
async def create_menu(menu: schemas.Menu, auth: Auth = Depends(FullAdminAuth(permissions=["sys.menu.create"]))):
    if menu.parent_id:
        menu.alwaysShow = False
    if not menu.order:
        order = await crud.MenuDal(auth.db).get_max_order()
        menu.order = order
    return SuccessResponse(await crud.MenuDal(auth.db).create_data(data=menu))


@router.delete("", summary="批量删除菜单", description="硬删除, 如果存在角色关联则无法删除")
async def delete_menus(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth(permissions=["sys.menu.delete"]))):
    await crud.MenuDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@router.put("/{data_id}", summary="更新菜单信息")
async def put_menus(
        data_id: int,
        data: schemas.Menu, auth: Auth = Depends(FullAdminAuth(permissions=["sys.menu.update"]))
):
    return SuccessResponse(await crud.MenuDal(auth.db).put_data(data_id, data))


@router.get("/routes", summary="获取当前用户菜单树")
async def get_menu_list(auth: Auth = Depends(FullAdminAuth())):
    # print(auth.user.__dict__)
    return SuccessResponse(await crud.MenuDal(auth.db).get_routers(auth.user))


@router.get("/{data_id}", summary="获取菜单信息")
async def put_menus(
        data_id: int,
        auth: Auth = Depends(FullAdminAuth(permissions=["sys.menu.view", "sys.menu.update"]))
):
    schema = schemas.MenuSimpleOut
    return SuccessResponse(await crud.MenuDal(auth.db).get_data(data_id, v_schema=schema))


