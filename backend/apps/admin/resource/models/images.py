#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/8/25 13:41
# @File           : images.py
# @IDE            : PyCharm
# @desc           : 图片素材表

from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.admin.system.models import SysUser
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer


class SysImages(BaseModel):
    __tablename__ = "sys_resource_images"
    __table_args__ = ({'comment': '图片素材表'})

    filename: Mapped[str] = mapped_column(String(255), nullable=False, comment="原图片名称")
    image_url: Mapped[str] = mapped_column(String(500), nullable=False, comment="图片链接")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sys_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[SysUser] = relationship(foreign_keys=create_user_id)
