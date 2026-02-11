from fastapi import APIRouter

from apps.admin.iot import client_group,client,device,product

# #
#
router = APIRouter()
router.include_router(client_group.router, prefix="/client_groups", tags=["iot"])
router.include_router(client.router, prefix="/clients", tags=["iot"])
router.include_router(device.router, prefix="/devices", tags=["iot"])
router.include_router(product.router, prefix="/products", tags=["iot"])

# router.include_router(notice.router, prefix="/system/notice", tags=["system"])
# router.include_router(alarm.router, prefix="/system/alarm", tags=["system"])