#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2026/04/01
# @File           : llm_config.py
# @IDE            : PyCharm
# @desc           : LLM模型配置 pydantic 模型，用于API序列化操作

from pydantic import BaseModel, ConfigDict, Field
from core.data_types import DatetimeStr
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ModelProvider(str, Enum):
    """模型提供商"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    ALIYUN = "aliyun"
    ZHIPU = "zhipu"
    BAIDU = "baidu"
    TENCENT = "tencent"
    CUSTOM = "custom"


class LLMModelConfigCreate(BaseModel):
    """创建LLM模型配置"""
    name: str = Field(..., description="配置名称")
    provider: ModelProvider = Field(..., description="模型提供商")
    model_name: str = Field(..., description="模型名称")
    api_key: str = Field(..., description="API密钥")
    api_base: str = Field(..., description="API基础URL")
    max_tokens: int = Field(default=4000, description="最大token数")
    temperature: float = Field(default=0.7, ge=0, le=2, description="温度参数")
    timeout: int = Field(default=120, description="超时时间(秒)")
    is_default: bool = Field(default=False, description="是否默认")
    is_enabled: bool = Field(default=True, description="是否启用")
    description: Optional[str] = Field(None, description="配置描述")


class LLMModelConfigUpdate(BaseModel):
    """更新LLM模型配置"""
    name: Optional[str] = Field(None, description="配置名称")
    provider: Optional[ModelProvider] = Field(None, description="模型提供商")
    model_name: Optional[str] = Field(None, description="模型名称")
    api_key: Optional[str] = Field(None, description="API密钥")
    api_base: Optional[str] = Field(None, description="API基础URL")
    max_tokens: Optional[int] = Field(None, description="最大token数")
    temperature: Optional[float] = Field(None, ge=0, le=2, description="温度参数")
    timeout: Optional[int] = Field(None, description="超时时间(秒)")
    is_default: Optional[bool] = Field(None, description="是否默认")
    is_enabled: Optional[bool] = Field(None, description="是否启用")
    description: Optional[str] = Field(None, description="配置描述")


class LLMModelConfigOut(BaseModel):
    """LLM模型配置输出"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    provider: ModelProvider
    model_name: str
    api_base: str
    max_tokens: int
    temperature: float
    timeout: int
    is_default: bool
    is_enabled: bool
    description: Optional[str] = None
    created_at: Optional[DatetimeStr] = None
    updated_at: Optional[DatetimeStr] = None
    api_key_masked: str = Field(..., description="脱敏后的API Key")


class ProviderInfo(BaseModel):
    """提供商信息"""
    value: str
    label: str
    default_api_base: str
    models: List[str]


# 预设提供商信息
PROVIDER_INFO: List[ProviderInfo] = [
    ProviderInfo(
        value="openai",
        label="OpenAI",
        default_api_base="https://api.openai.com/v1",
        models=["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
    ),
    ProviderInfo(
        value="deepseek",
        label="DeepSeek",
        default_api_base="https://api.deepseek.com/v1",
        models=["deepseek-chat", "deepseek-coder"]
    ),
    ProviderInfo(
        value="aliyun",
        label="阿里云通义千问",
        default_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        models=["qwen-max", "qwen-plus", "qwen-turbo"]
    ),
    ProviderInfo(
        value="zhipu",
        label="智谱AI",
        default_api_base="https://open.bigmodel.cn/api/paas/v4",
        models=["glm-4", "glm-3-turbo"]
    ),
    ProviderInfo(
        value="baidu",
        label="百度文心一言",
        default_api_base="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat",
        models=["ernie-4.0", "ernie-3.5"]
    ),
    ProviderInfo(
        value="tencent",
        label="腾讯混元",
        default_api_base="https://hunyuan.tencentcloudapi.com",
        models=["hunyuan-lite", "hunyuan-standard"]
    ),
    ProviderInfo(
        value="custom",
        label="自定义",
        default_api_base="",
        models=[]
    ),
]