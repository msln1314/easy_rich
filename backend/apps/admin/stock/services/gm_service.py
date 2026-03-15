#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/3/12
# @File           : gm_service.py
# @IDE            : PyCharm
# @desc           : 掘金量化数据服务

from typing import Optional
from core.logger import logger
from application.settings import settings


class GMService:
    """掘金量化数据服务"""

    def __init__(self, token: Optional[str] = None):
        """
        初始化 GM 服务

        Args:
            token: GM API token
        """
        self.enabled = False
        self.token = token
        self.gm = None
        self._init_gm()

    def _init_gm(self):
        """初始化掘金量化连接"""
        try:
            from gm import api as gm_api
            self.gm = gm_api

            # 使用 token 进行认证
            if self.token:
                try:
                    self.gm.set_token(self.token)
                    logger.info(f"GM Token 已设置: {self.token[:10]}...")
                except Exception as token_error:
                    logger.warning(f"GM Token 设置失败: {token_error}")

            self.enabled = True
            logger.info("掘金量化 SDK 初始化成功")
        except ImportError:
            logger.warning("掘金量化 SDK 未安装，GM 服务将不可用")
            self.enabled = False
        except Exception as e:
            logger.error(f"掘金量化 SDK 初始化失败: {str(e)}")
            self.enabled = False
        print(self.enabled, "gm 服务是否启用")

    def is_available(self) -> bool:
        """检查 GM 服务是否可用"""
        return self.enabled


# 创建全局 GM 服务实例
gm_service = GMService(token=settings.GM_TOKEN)