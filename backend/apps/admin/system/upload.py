# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/24 16:44
# @File           : sms.py
# @IDE            : PyCharm
# @desc           : 主要接口文件

from fastapi import APIRouter, UploadFile, Form
from application.settings import settings
# from utils.file.aliyun_oss import AliyunOSS, BucketConf
from utils.file.file_manage import FileManage
from utils.response import SuccessResponse

router = APIRouter()







###########################################################
#    文件上传管理
###########################################################
# @router.post("/upload/image/to/oss", summary="上传图片到阿里云OSS")
# async def upload_image_to_oss(file: UploadFile, path: str = Form(...)):
#     result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_image(path, file)
#     return SuccessResponse(result)
#
#
# @router.post("/upload/video/to/oss", summary="上传视频到阿里云OSS")
# async def upload_video_to_oss(file: UploadFile, path: str = Form(...)):
#     result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_video(path, file)
#     return SuccessResponse(result)
#
#
# @router.post("/upload/file/to/oss", summary="上传文件到阿里云OSS")
# async def upload_file_to_oss(file: UploadFile, path: str = Form(...)):
#     result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_file(path, file)
#     return SuccessResponse(result)


@router.post("/image/to/local", summary="上传图片到本地")
async def upload_image_to_local(file: UploadFile, path: str = Form(...)):
    manage = FileManage(file, path)
    path = await manage.save_image_local()
    return SuccessResponse(path)

