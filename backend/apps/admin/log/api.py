from fastapi import APIRouter

from apps.admin.log import sms, action, operation, login, task

router = APIRouter()
router.include_router(sms.router, prefix="/sms", tags=["log"])
router.include_router(login.router, prefix="/logins", tags=["log"])
router.include_router(action.router, prefix="/actions", tags=["log"])
router.include_router(operation.router, prefix="/operations", tags=["log"])
router.include_router(task.router, prefix="/tasks", tags=["log"])
