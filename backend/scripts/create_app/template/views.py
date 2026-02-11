#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : {created_at}
# @File           : sms.py
# @IDE            : PyCharm
# @desc           :


from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import schemas, crud, models

app = APIRouter()


