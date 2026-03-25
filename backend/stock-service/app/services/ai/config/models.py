# -*- coding: utf-8 -*-
"""
配置数据模型
参考 valuecell 三层配置系统设计
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from pathlib import Path


class ProviderModelMapping(BaseModel):
    """Provider模型映射 - 不同Provider使用不同模型ID"""
    provider: str
    model_id: str


class ModelConfig(BaseModel):
    """模型配置"""
    provider: str = "openai"
    model_id: str = "gpt-4"
    provider_models: Dict[str, str] = Field(default_factory=dict)
    """不同Provider的模型映射，如: {"deepseek": "deepseek-chat", "aliyun": "qwen-max"}"""

    max_tokens: int = 4000
    temperature: float = 0.7
    timeout: int = 120

    def get_model_id_for_provider(self, provider: str) -> str:
        """获取特定Provider的模型ID"""
        return self.provider_models.get(provider, self.model_id)


class ProviderConfig(BaseModel):
    """Provider配置"""
    name: str
    api_key_env: str = ""  # 环境变量名
    api_base: str = ""
    default: bool = False

    def get_api_key(self) -> Optional[str]:
        """获取API Key"""
        import os
        return os.getenv(self.api_key_env) if self.api_key_env else None


class AgentConfig(BaseModel):
    """Agent配置"""
    name: str
    primary_model: ModelConfig = Field(default_factory=ModelConfig)
    fallback_providers: List[str] = Field(default_factory=list)
    """回退Provider列表"""

    system_prompt_template: str = ""
    max_steps: int = 6

    # 模型参数覆盖
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None

    def get_effective_max_tokens(self) -> int:
        """获取有效的max_tokens"""
        return self.max_tokens or self.primary_model.max_tokens

    def get_effective_temperature(self) -> float:
        """获取有效的temperature"""
        return self.temperature if self.temperature is not None else self.primary_model.temperature


class LLMProvidersConfig(BaseModel):
    """LLM Providers配置"""
    providers: Dict[str, ProviderConfig] = Field(default_factory=dict)

    def get_provider(self, name: str) -> Optional[ProviderConfig]:
        return self.providers.get(name)


class AgentsConfig(BaseModel):
    """Agents配置"""
    agents: Dict[str, AgentConfig] = Field(default_factory=dict)

    def get_agent(self, name: str) -> Optional[AgentConfig]:
        return self.agents.get(name)


class AppConfig(BaseModel):
    """应用配置"""
    llm_providers: LLMProvidersConfig = Field(default_factory=LLMProvidersConfig)
    agents: AgentsConfig = Field(default_factory=AgentsConfig)

    # 全局设置
    default_provider: str = "openai"
    default_model: str = "gpt-4"

    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """获取Agent配置，返回默认配置如果不存在"""
        agent_config = self.agents.get_agent(agent_name)
        if agent_config:
            return agent_config

        # 返回默认配置
        return AgentConfig(
            name=agent_name,
            primary_model=ModelConfig(
                provider=self.default_provider,
                model_id=self.default_model,
            ),
        )