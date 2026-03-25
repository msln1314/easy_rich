# -*- coding: utf-8 -*-
"""
模型工厂
参考 valuecell ModelFactory 设计，支持Provider回退链
"""
import os
import logging
from typing import Dict, List, Optional, Any, Type
from dataclasses import dataclass

from .llm_adapter import LLMToolAdapter, LLMConfig
from .config import get_config_manager, AgentConfig, ModelConfig, ProviderConfig

logger = logging.getLogger(__name__)


# Provider API基础URL映射
PROVIDER_API_BASE: Dict[str, str] = {
    "openai": "https://api.openai.com/v1",
    "deepseek": "https://api.deepseek.com/v1",
    "aliyun": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "zhipu": "https://open.bigmodel.cn/api/paas/v4",
    "baidu": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat",
    "tencent": "https://api.hunyuan.cloud.tencent.com/v1",
    "local": "http://localhost:11434/v1",
}

# Provider API Key环境变量映射
PROVIDER_API_KEY_ENV: Dict[str, str] = {
    "openai": "OPENAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "aliyun": "ALIYUN_API_KEY",
    "zhipu": "ZHIPU_API_KEY",
    "baidu": "BAIDU_API_KEY",
    "tencent": "TENCENT_API_KEY",
    "local": "LOCAL_API_KEY",
}


@dataclass
class ProviderInfo:
    """Provider信息"""
    name: str
    api_key: str
    api_base: str

    @classmethod
    def from_config(cls, provider_name: str) -> Optional["ProviderInfo"]:
        """从配置创建Provider信息"""
        config_manager = get_config_manager()

        # 获取API Key
        api_key_env = PROVIDER_API_KEY_ENV.get(provider_name, f"{provider_name.upper()}_API_KEY")
        api_key = config_manager.get_env(api_key_env) or os.getenv(api_key_env, "")

        # 获取API Base
        provider_config = config_manager.get_provider_config(provider_name)
        if provider_config:
            api_base = provider_config.api_base or PROVIDER_API_BASE.get(provider_name, "")
        else:
            api_base = PROVIDER_API_BASE.get(provider_name, "")

        if not api_key:
            logger.warning(f"Provider {provider_name} 缺少API Key")
            return None

        return cls(name=provider_name, api_key=api_key, api_base=api_base)


class ModelFactory:
    """
    模型工厂

    支持为特定Agent创建模型，并实现Provider回退链。
    参考 valuecell 设计模式。
    """

    _instance: Optional["ModelFactory"] = None

    def __init__(self):
        self._config_manager = get_config_manager()

    def get_provider_info(self, provider_name: str) -> Optional[ProviderInfo]:
        """获取Provider信息"""
        return ProviderInfo.from_config(provider_name)

    def create_llm_config(
        self,
        provider: str,
        model_id: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        timeout: int = 120,
    ) -> LLMConfig:
        """创建LLM配置"""
        provider_info = self.get_provider_info(provider)
        if not provider_info:
            raise ValueError(f"无法获取Provider {provider} 的配置信息")

        return LLMConfig(
            provider=provider,
            model=model_id,
            api_key=provider_info.api_key,
            api_base=provider_info.api_base,
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=timeout,
        )

    def create_adapter(
        self,
        provider: str,
        model_id: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
    ) -> LLMToolAdapter:
        """创建LLM适配器"""
        config = self.create_llm_config(
            provider=provider,
            model_id=model_id,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return LLMToolAdapter(config)

    def create_model_for_agent(
        self,
        agent_name: str,
        use_fallback: bool = True,
        **kwargs,
    ) -> LLMToolAdapter:
        """
        为特定Agent创建模型，支持自动回退

        Args:
            agent_name: Agent名称
            use_fallback: 是否使用回退Provider
            **kwargs: 覆盖参数

        Returns:
            LLMToolAdapter: LLM适配器

        Raises:
            RuntimeError: 所有Provider都失败时抛出
        """
        agent_config = self._config_manager.get_agent_config(agent_name)
        model_config = agent_config.primary_model

        # 获取覆盖参数
        max_tokens = kwargs.get("max_tokens", agent_config.get_effective_max_tokens())
        temperature = kwargs.get("temperature", agent_config.get_effective_temperature())

        # 获取Provider列表
        providers = [model_config.provider]
        if use_fallback and agent_config.fallback_providers:
            providers.extend(agent_config.fallback_providers)

        errors: List[str] = []

        for provider in providers:
            try:
                # 获取该Provider对应的模型ID
                model_id = model_config.get_model_id_for_provider(provider)

                adapter = self.create_adapter(
                    provider=provider,
                    model_id=model_id,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

                logger.info(f"为Agent {agent_name} 创建模型: {provider}/{model_id}")
                return adapter

            except Exception as e:
                error_msg = f"Provider {provider} 创建失败: {str(e)}"
                logger.warning(error_msg)
                errors.append(error_msg)
                continue

        raise RuntimeError(
            f"为Agent {agent_name} 创建模型失败，所有Provider都不可用: {'; '.join(errors)}"
        )

    def get_available_providers(self) -> List[str]:
        """获取可用的Provider列表"""
        available = []
        for provider_name in PROVIDER_API_BASE.keys():
            provider_info = self.get_provider_info(provider_name)
            if provider_info and provider_info.api_key:
                available.append(provider_name)
        return available

    @classmethod
    def get_instance(cls) -> "ModelFactory":
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def get_model_factory() -> ModelFactory:
    """获取模型工厂实例"""
    return ModelFactory.get_instance()


def create_model_for_agent(agent_name: str, use_fallback: bool = True, **kwargs) -> LLMToolAdapter:
    """
    便捷函数：为Agent创建模型

    Args:
        agent_name: Agent名称
        use_fallback: 是否使用回退Provider
        **kwargs: 覆盖参数

    Returns:
        LLMToolAdapter: LLM适配器
    """
    factory = get_model_factory()
    return factory.create_model_for_agent(agent_name, use_fallback=use_fallback, **kwargs)