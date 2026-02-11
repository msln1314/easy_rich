from typing import Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps


router = APIRouter()


@router.get("/list", response_model=schemas.Response)
def get_notices(*, db: Session = Depends(deps.get_db), limit: Optional[int] = None, page: Optional[int] = None, notice_title: Optional[str] = None, order: Optional[str] = None,
                prop: Optional[str] = None, status: Optional[str] = None, notice_type: Optional[str] = None, notice_to: Optional[str] = None, created_by: Optional[str] = None,
                is_manage: bool = False, User=Depends(deps.get_current_active_user)) -> Any:
    """用户通知-查询"""
    query = db.query(models.User_Notice)
    # read_notice_all = [i.value for i in get_data_type(db,models.Dict_Type,'read_notice_all')]
    if not is_manage:
        query = query.filter(models.User_Notice.notice_to == User.username)
    if notice_title: query = query.filter(models.User_Notice.notice_title.like("%" + notice_title + "%"))
    if status: query = query.filter(models.User_Notice.status == status)
    if notice_type: query = query.filter(models.User_Notice.notice_type == notice_type)
    if notice_to: query = query.filter(models.User_Notice.notice_to == notice_to)
    if created_by: query = query.filter(models.User_Notice.created_by == created_by)
    total = query.count()
    if prop and order:
        if order == 'descending':
            query = query.order_by(getattr(models.User_Notice, prop).desc())
        elif order == 'ascending':
            query = query.order_by(getattr(models.User_Notice, prop).asc())
        else:
            query = query.order_by(getattr(models.User_Notice, prop))
    else:
        query = query.order_by(models.User_Notice.created_at.asc())
    if page and limit:
        query = query.limit(limit).offset((page - 1) * limit)
    user_notices = query.all()

    return {"code": 20000, "data": {"items": user_notices, 'total': total}, }


@router.post("/", response_model=schemas.Response)
def add_notice(*, db: Session = Depends(deps.get_db), User_notice: schemas.User_notice) -> Any:
    """部门管理-新增"""
    db.add(models.User_Notice(**User_notice.dict()))
    return {"code": 20000, "data": "", "message": "新增通知成功"}


@router.get("/{id}", response_model=schemas.Response)
def get_user_notice(*, db: Session = Depends(deps.get_db), id: int, ) -> Any:
    """部门管理-更新前查询"""
    user_notice = db.query(models.User_Notice).filter(models.User_Notice.id == id).one()
    return {"code": 20000, "data": user_notice, }


@router.put("/", response_model=schemas.Response)
def update_user_notice(*, db: Session = Depends(deps.get_db), User_notice: schemas.User_notice_change_status, User=Depends(deps.get_current_active_user)) -> Any:
    """部门管理-修改"""
    user_notice = User_notice.dict()
    user_notice['updated_by'] = User.username
    user_notice['updated_at'] = datetime.now()
    data = db.query(models.User_Notice).filter(models.User_Notice.id == User_notice.id).update(User_notice)
    return {"code": 20000, "message": "修改成功", 'data': data}


@router.delete("/{id}", response_model=schemas.Response)
def delete_user_notice_id(id: int, db: Session = Depends(deps.get_db), ) -> Any:
    """部门管理-删除"""
    db.query(models.User_Notice).filter(models.User_Notice.id == id).delete()
    return {"code": 20000, "message": f"删除成功"}


