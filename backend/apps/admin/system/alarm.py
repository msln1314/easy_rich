from typing import Any, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.extensions.utils import list_to_tree
from app.utils.get_dict_data_type import get_data_type
import json

router = APIRouter()


# 告警处理
@router.get("/list", response_model=schemas.Response)
def get_alarm_notices(*, db: Session = Depends(deps.get_db), limit: Optional[int] = None, page: Optional[int] = None, order: Optional[str] = None, prop: Optional[str] = None,
                      status: Optional[str] = None, alarm_type: Optional[str] = None, engineer_to: Optional[str] = None, created_by: Optional[str] = None, is_manage: bool = False,
                      alarm_title: Optional[str] = None, User=Depends(deps.get_current_active_user)) -> Any:
    """用户通知-查询"""
    query = db.query(models.User_Alarm)
    # read_notice_all = [i.value for i in get_data_type(db,models.Dict_Type,'read_notice_all')]
    if not is_manage:
        query = query.filter(models.User_Alarm.alarm_to == User.username)
    if alarm_title: query = query.filter(models.User_Alarm.alarm_title.like("%" + alarm_title + "%"))
    if status: query = query.filter(models.User_Alarm.status == status)
    if alarm_type: query = query.filter(models.User_Alarm.alarm_type == alarm_type)
    if engineer_to: query = query.filter(models.User_Alarm.engineer_to == engineer_to)
    if created_by: query = query.filter(models.User_Alarm.created_by == created_by)
    total = query.count()
    if prop and order:
        if order == 'descending':
            query = query.order_by(getattr(models.User_Alarm, prop).desc())
        elif order == 'ascending':
            query = query.order_by(getattr(models.User_Alarm, prop).asc())
        else:
            query = query.order_by(getattr(models.User_Alarm, prop))
    else:
        query = query.order_by(models.User_Alarm.created_at.asc())
    if page and limit:
        query = query.limit(limit).offset((page - 1) * limit)
    user_alarm_notices = query.all()

    return {"code": 20000, "data": {"items": user_alarm_notices, 'total': total}, }


@router.post("/", response_model=schemas.Response)
def add_alarm_notice(*, db: Session = Depends(deps.get_db), User_alarm: schemas.User_alarm) -> Any:
    """部门管理-新增"""
    db.add(models.User_Alarm(**User_alarm.dict()))
    return {"code": 20000, "data": "", "message": "新增告警通知成功"}


@router.get("/{id}", response_model=schemas.Response)
def get_user_alarm(*, db: Session = Depends(deps.get_db), id: int, ) -> Any:
    """部门管理-更新前查询"""
    user_notice = db.query(models.User_Alarm).filter(models.User_Alarm.id == id).one()
    return {"code": 20000, "data": user_notice, }


@router.put("/", response_model=schemas.Response)
def update_user_alarm(*, db: Session = Depends(deps.get_db), User_alarm: schemas.User_alarm_update, User=Depends(deps.get_current_active_user)) -> Any:
    """部门管理-修改"""
    user_alarm = User_alarm.dict()
    user_alarm['updated_by'] = User.username
    user_alarm['updated_at'] = datetime.now()
    data = db.query(models.User_Alarm).filter(models.User_Alarm.id == User_alarm.id).update(user_alarm)
    return {"code": 20000, "message": "修改成功", 'data': data}


@router.put("/action", response_model=schemas.Response)
def update_user_alarm_action(*, db: Session = Depends(deps.get_db), User_alarm: schemas.User_alarm_action_case, User=Depends(deps.get_current_active_user)) -> Any:
    """部门管理-修改"""
    user_alarm_notice = User_alarm.dict()

    #  生成单号
    def get_case_no(type):
        # 年月日时分秒
        case_time = datetime.now().strftime('%Y%m%d%H%M%S')
        return type + '_' + case_time

    case_id = get_case_no(User_alarm.work_type)
    user_alarm_notice['case_id'] = case_id
    user_alarm_notice['updated_by'] = User.username
    user_alarm_notice['updated_at'] = datetime.now()
    user_alarm_notice['status'] = 2
    user_alarm_notice.pop('work_type')
    db.query(models.User_Alarm).filter(models.User_Alarm.id == User_alarm.id).update(user_alarm_notice)
    data = db.query(models.User_Alarm).filter(models.User_Alarm.id == User_alarm.id).one()

    # content ={
    #     "target_obj": [{
    #         "source_mac": "12:11:12:34:12:34"
    #     }, {
    #         "source_mac": "55:12:d2:23:12:f4"
    #     }]
    # }
    content =json.loads(data.alarm_content)
    data = data.dict()
    data['alarm_content'] = content
    # print(json.dumps(content))
    # print(jsonable_encoder(data.alarm_content))

    return jsonable_encoder({"code": 20000, "message": "修改成功", 'data': data})


@router.delete("/{id}", response_model=schemas.Response)
def delete_user_alarm_id(id: int, db: Session = Depends(deps.get_db), ) -> Any:
    """部门管理-删除"""
    db.query(models.User_Alarm).filter(models.User_Alarm.id == id).delete()
    db.flush()
    return {"code": 20000, "message": f"删除成功"}