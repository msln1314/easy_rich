# -*- coding: utf-8 -*-
"""
配置管理器
参考 valuecell 三层配置系统设计
配置优先级: 环境变量 > .env 文件 > YAML 配置
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, TypeVar, Type
import yaml

from .models import AppConfig, AgentConfig, ModelConfig, ProviderConfig


T = TypeVar('T')


class ConfigManager:
    """
    三层配置管理器

    优先级: 环境变量 > .env 文件 > YAML 配置 > 默认值
    """

    _instance: Optional['ConfigManager'] = None

    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self._yaml_config: Dict[str, Any] = {}
        self._env_config: Dict[str, str] = {}
        self._app_config: Optional[AppConfig] = None

        self._load_all()

    def _load_all(self):
        """加载所有配置"""
        # 1. 加载YAML配置
        self._yaml_config = self._load_yaml_config()

        # 2. 加载.env配置
        self._env_config = self._load_env_file()

        # 3. 构建应用配置
        self._app_config = self._build_app_config()

    def _load_yaml_config(self) -> Dict[str, Any]:
        """加载YAML配置文件"""
        config: Dict[str, Any] = {}

        # 主配置文件
        main_config_path = self.config_dir / "config.yaml"
        if main_config_path.exists():
            with open(main_config_path, "r", encoding="utf-8") as f:
                config.update(yaml.safe_load(f) or {})

        # Agents配置
        agents_config_path = self.config_dir / "agents.yaml"
        if agents_config_path.exists():
            with open(agents_config_path, "r", encoding="utf-8") as f:
                agents_config = yaml.safe_load(f) or {}
                if "agents" not in config:
                    config["agents"] = {}
                config["agents"].update(agents_config.get("agents", {}))

        return config

    def _load_env_file(self) -> Dict[str, str]:
        """加载.env文件"""
        env_config: Dict[str, str] = {}

        env_path = Path(".env")
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        env_config[key.strip()] = value.strip().strip('"').strip("'")

        return env_config

    def _build_app_config(self) -> AppConfig:
        """构建应用配置对象"""
        # 转换YAML配置为AppConfig
        config_data = self._yaml_config.copy()

        # 应用环境变量覆盖
        config_data = self._apply_env_overrides(config_data)

        try:
            return AppConfig(**config_data)
        except Exception:
            # 如果解析失败，返回默认配置
            return AppConfig()

    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """应用环境变量覆盖"""
        # 环境变量映射
        env_mappings = {
            "DEFAULT_PROVIDER": ("default_provider", str),
            "DEFAULT_MODEL": ("default_model", str),
            "OPENAI_API_KEY": ("llm_providers.providers.openai.api_key", str),
            "DEEPSEEK_API_KEY": ("llm_providers.providers.deepseek.api_key", str),
            "ALIYUN_API_KEY": ("llm_providers.providers.aliyun.api_key", str),
            "ZHIPU_API_KEY": ("llm_providers.providers.zhipu.api_key", str),
        }

        for env_key, (path, value_type) in env_mappings.items():
            value = self.get_env(env_key)
            if value:
                self._set_nested(config, path.split("."), value)

        return config

    def _set_nested(self, config: Dict, path: List[str], value: Any):
        """设置嵌套配置值"""
        for key in path[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[path[-1]] = value

    def get_env(self, key: str, default: str = None) -> Optional[str]:
        """
        获取环境变量
        优先级: os.environ > .env文件
        """
        # 首先检查系统环境变量
        value = os.getenv(key)
        if value:
            return value

        # 然后检查.env文件
        return self._env_config.get(key, default)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        优先级: 环境变量 > .env > YAML
        """
        # 检查环境变量
        env_value = self.get_env(key.upper())
        if env_value is not None:
            return env_value

        # 检查YAML配置
        keys = key.split(".")
        value = self._yaml_config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """获取Agent配置"""
        return self._app_config.get_agent_config(agent_name)

    def get_model_config(self, agent_name: str) -> ModelConfig:
        """获取Agent的模型配置"""
        agent_config = self.get_agent_config(agent_name)
        return agent_config.primary_model

    def get_provider_config(self, provider_name: str) -> Optional[ProviderConfig]:
        """获取Provider配置"""
        return self._app_config.llm_providers.get_provider(provider_name)

    def get_all_providers(self) -> Dict[str, ProviderConfig]:
        """获取所有Provider配置"""
        return self._app_config.llm_providers.providers

    @property
    def app_config(self) -> AppConfig:
        """获取应用配置"""
        return self._app_config

    @classmethod
    def get_instance(cls) -> 'ConfigManager':
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reload(self):
        """重新加载配置"""
        self._load_all()


def get_config_manager() -> ConfigManager:
    """获取配置管理器实例"""
    return ConfigManager.get_instance()