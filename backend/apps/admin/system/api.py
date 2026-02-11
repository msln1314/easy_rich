from fastapi import APIRouter

from apps.admin.system import menu, dict, dept, user, task, sms, settings, role, upload

# #
#
router = APIRouter()
router.include_router(user.router, prefix="/users", tags=["system"])
router.include_router(menu.router, prefix="/menus", tags=["system"])
router.include_router(dict.router, prefix="/dict", tags=["system"])
router.include_router(dept.router, prefix="/depts", tags=["system"])
router.include_router(role.router, prefix="/roles", tags=["system"])
router.include_router(upload.router, prefix="/upload", tags=["system"])
router.include_router(task.router, prefix="/tasks", tags=["system"])
router.include_router(sms.router, prefix="/sms", tags=["system"])
router.include_router(settings.router, prefix="/settings", tags=["system"])

# router.include_router(notice.router, prefix="/system/notice", tags=["system"])
# router.include_router(alarm.router, prefix="/system/alarm", tags=["system"])
