"""AI模型配置数据模型"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
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


class LLMModelConfig(BaseModel):
    """LLM模型配置"""
    id: Optional[int] = Field(None, description="配置ID")
    name: str = Field(..., description="配置名称")
    provider: ModelProvider = Field(..., description="模型提供商")
    model_name: str = Field(..., description="模型名称，如 gpt-4, deepseek-chat")
    api_key: str = Field(..., description="API密钥")
    api_base: str = Field(..., description="API基础URL")
    max_tokens: int = Field(default=4000, description="最大生成token数")
    temperature: float = Field(default=0.7, ge=0, le=2, description="温度参数")
    timeout: int = Field(default=120, description="请求超时时间(秒)")
    is_default: bool = Field(default=False, description="是否为默认模型")
    is_enabled: bool = Field(default=True, description="是否启用")
    description: Optional[str] = Field(None, description="配置描述")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "GPT-4配置",
                "provider": "openai",
                "model_name": "gpt-4",
                "api_key": "sk-xxx",
                "api_base": "https://api.openai.com/v1",
                "max_tokens": 4000,
                "temperature": 0.7,
                "timeout": 120,
                "is_default": True,
                "is_enabled": True,
                "description": "OpenAI GPT-4模型配置"
            }
        }


class LLMModelConfigCreate(BaseModel):
    """创建LLM模型配置"""
    name: str = Field(..., description="配置名称")
    provider: ModelProvider = Field(..., description="模型提供商")
    model_name: str = Field(..., description="模型名称")
    api_key: str = Field(..., description="API密钥")
    api_base: str = Field(..., description="API基础URL")
    max_tokens: int = Field(default=4000, description="最大token数")
    temperature: float = Field(default=0.7, description="温度参数")
    timeout: int = Field(default=120, description="超时时间")
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
    temperature: Optional[float] = Field(None, description="温度参数")
    timeout: Optional[int] = Field(None, description="超时时间")
    is_default: Optional[bool] = Field(None, description="是否默认")
    is_enabled: Optional[bool] = Field(None, description="是否启用")
    description: Optional[str] = Field(None, description="配置描述")


class LLMModelConfigResponse(BaseModel):
    """LLM模型配置响应（隐藏敏感信息）"""
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
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    # API Key 脱敏显示
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