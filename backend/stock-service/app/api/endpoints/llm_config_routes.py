# -*- coding: utf-8 -*-
"""LLM模型配置管理接口"""
import json
import os
from typing import List, Optional
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.models.llm_config_models import (
    LLMModelConfig,
    LLMModelConfigCreate,
    LLMModelConfigUpdate,
    LLMModelConfigResponse,
    PROVIDER_INFO,
    ProviderInfo,
)

router = APIRouter()

# 配置文件路径
CONFIG_DIR = Path("config")
CONFIG_FILE = CONFIG_DIR / "llm_models.json"


def _ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _load_configs() -> List[LLMModelConfig]:
    """加载配置"""
    _ensure_config_dir()
    if not CONFIG_FILE.exists():
        return []
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [LLMModelConfig(**item) for item in data]
    except Exception:
        return []


def _save_configs(configs: List[LLMModelConfig]):
    """保存配置"""
    _ensure_config_dir()
    data = [config.model_dump() for config in configs]
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def _mask_api_key(api_key: str) -> str:
    """脱敏API Key"""
    if len(api_key) <= 8:
        return "****"
    return api_key[:4] + "****" + api_key[-4:]


def _get_next_id(configs: List[LLMModelConfig]) -> int:
    """获取下一个ID"""
    if not configs:
        return 1
    return max(c.id or 0 for c in configs) + 1


@router.get("/providers", response_model=List[ProviderInfo])
async def get_providers():
    """获取支持的模型提供商列表"""
    return PROVIDER_INFO


@router.get("/list", response_model=List[LLMModelConfigResponse])
async def list_configs():
    """获取所有模型配置列表"""
    configs = _load_configs()
    result = []
    for config in configs:
        result.append(LLMModelConfigResponse(
            id=config.id,
            name=config.name,
            provider=config.provider,
            model_name=config.model_name,
            api_base=config.api_base,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            timeout=config.timeout,
            is_default=config.is_default,
            is_enabled=config.is_enabled,
            description=config.description,
            created_at=config.created_at,
            updated_at=config.updated_at,
            api_key_masked=_mask_api_key(config.api_key),
        ))
    return result


@router.get("/{config_id}", response_model=LLMModelConfigResponse)
async def get_config(config_id: int):
    """获取单个模型配置"""
    configs = _load_configs()
    for config in configs:
        if config.id == config_id:
            return LLMModelConfigResponse(
                id=config.id,
                name=config.name,
                provider=config.provider,
                model_name=config.model_name,
                api_base=config.api_base,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                timeout=config.timeout,
                is_default=config.is_default,
                is_enabled=config.is_enabled,
                description=config.description,
                created_at=config.created_at,
                updated_at=config.updated_at,
                api_key_masked=_mask_api_key(config.api_key),
            )
    raise HTTPException(status_code=404, detail="配置不存在")


@router.post("/create", response_model=LLMModelConfigResponse)
async def create_config(data: LLMModelConfigCreate):
    """创建模型配置"""
    configs = _load_configs()

    # 检查名称是否重复
    for c in configs:
        if c.name == data.name:
            raise HTTPException(status_code=400, detail="配置名称已存在")

    # 如果设置为默认，取消其他默认
    if data.is_default:
        for c in configs:
            c.is_default = False

    now = datetime.now()
    new_config = LLMModelConfig(
        id=_get_next_id(configs),
        **data.model_dump(),
        created_at=now,
        updated_at=now,
    )
    configs.append(new_config)
    _save_configs(configs)

    return LLMModelConfigResponse(
        id=new_config.id,
        name=new_config.name,
        provider=new_config.provider,
        model_name=new_config.model_name,
        api_base=new_config.api_base,
        max_tokens=new_config.max_tokens,
        temperature=new_config.temperature,
        timeout=new_config.timeout,
        is_default=new_config.is_default,
        is_enabled=new_config.is_enabled,
        description=new_config.description,
        created_at=new_config.created_at,
        updated_at=new_config.updated_at,
        api_key_masked=_mask_api_key(new_config.api_key),
    )


@router.put("/{config_id}", response_model=LLMModelConfigResponse)
async def update_config(config_id: int, data: LLMModelConfigUpdate):
    """更新模型配置"""
    configs = _load_configs()

    for i, config in enumerate(configs):
        if config.id == config_id:
            # 检查名称是否与其他配置重复
            if data.name:
                for c in configs:
                    if c.id != config_id and c.name == data.name:
                        raise HTTPException(status_code=400, detail="配置名称已存在")

            # 如果设置为默认，取消其他默认
            if data.is_default:
                for c in configs:
                    c.is_default = False

            # 更新字段
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(config, key, value)

            config.updated_at = datetime.now()
            configs[i] = config
            _save_configs(configs)

            return LLMModelConfigResponse(
                id=config.id,
                name=config.name,
                provider=config.provider,
                model_name=config.model_name,
                api_base=config.api_base,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                timeout=config.timeout,
                is_default=config.is_default,
                is_enabled=config.is_enabled,
                description=config.description,
                created_at=config.created_at,
                updated_at=config.updated_at,
                api_key_masked=_mask_api_key(config.api_key),
            )

    raise HTTPException(status_code=404, detail="配置不存在")


@router.delete("/{config_id}")
async def delete_config(config_id: int):
    """删除模型配置"""
    configs = _load_configs()
    for i, config in enumerate(configs):
        if config.id == config_id:
            configs.pop(i)
            _save_configs(configs)
            return {"message": "删除成功"}
    raise HTTPException(status_code=404, detail="配置不存在")


@router.post("/{config_id}/set-default")
async def set_default(config_id: int):
    """设置默认模型"""
    configs = _load_configs()
    found = False

    for config in configs:
        if config.id == config_id:
            config.is_default = True
            found = True
        else:
            config.is_default = False

    if not found:
        raise HTTPException(status_code=404, detail="配置不存在")

    _save_configs(configs)
    return {"message": "设置成功"}


@router.post("/{config_id}/toggle")
async def toggle_config(config_id: int):
    """启用/禁用模型配置"""
    configs = _load_configs()

    for config in configs:
        if config.id == config_id:
            config.is_enabled = not config.is_enabled
            config.updated_at = datetime.now()
            _save_configs(configs)
            return {"is_enabled": config.is_enabled}

    raise HTTPException(status_code=404, detail="配置不存在")


@router.post("/{config_id}/test")
async def test_config(config_id: int):
    """测试模型配置"""
    configs = _load_configs()

    for config in configs:
        if config.id == config_id:
            if not config.is_enabled:
                raise HTTPException(status_code=400, detail="配置已禁用")

            try:
                import httpx

                # 构建测试请求
                headers = {
                    "Authorization": f"Bearer {config.api_key}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": config.model_name,
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10,
                }

                with httpx.Client(timeout=config.timeout) as client:
                    response = client.post(
                        f"{config.api_base}/chat/completions",
                        headers=headers,
                        json=payload,
                    )

                if response.status_code == 200:
                    return {"success": True, "message": "连接测试成功"}
                else:
                    return {"success": False, "message": f"API返回错误: {response.status_code}"}

            except Exception as e:
                return {"success": False, "message": f"连接测试失败: {str(e)}"}

    raise HTTPException(status_code=404, detail="配置不存在")