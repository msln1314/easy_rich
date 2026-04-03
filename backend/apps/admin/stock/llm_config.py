# -*- coding: utf-8 -*-
"""LLM模型配置管理接口"""
import json
import logging
from typing import List
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, HTTPException

from apps.admin.stock.schemas.llm_config import (
    LLMModelConfigCreate,
    LLMModelConfigUpdate,
    LLMModelConfigOut,
    ProviderInfo,
    PROVIDER_INFO,
)

router = APIRouter()
logger = logging.getLogger(__name__)

# 配置文件路径
CONFIG_DIR = Path("config")
CONFIG_FILE = CONFIG_DIR / "llm_models.json"


def _ensure_config_dir():
    """确保配置目录存在"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _load_configs() -> List[dict]:
    """加载配置"""
    _ensure_config_dir()
    if not CONFIG_FILE.exists():
        return []
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载LLM配置失败: {e}")
        return []


def _save_configs(configs: List[dict]):
    """保存配置"""
    _ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(configs, f, ensure_ascii=False, indent=2, default=str)


def _mask_api_key(api_key: str) -> str:
    """脱敏API Key"""
    if not api_key or len(api_key) <= 8:
        return "****"
    return api_key[:4] + "****" + api_key[-4:]


def _get_next_id(configs: List[dict]) -> int:
    """获取下一个ID"""
    if not configs:
        return 1
    return max(c.get("id", 0) for c in configs) + 1


def _config_to_response(config: dict) -> LLMModelConfigOut:
    """配置字典转响应模型"""
    return LLMModelConfigOut(
        id=config["id"],
        name=config["name"],
        provider=config["provider"],
        model_name=config["model_name"],
        api_base=config["api_base"],
        max_tokens=config.get("max_tokens", 4000),
        temperature=config.get("temperature", 0.7),
        timeout=config.get("timeout", 120),
        is_default=config.get("is_default", False),
        is_enabled=config.get("is_enabled", True),
        description=config.get("description"),
        created_at=config.get("created_at"),
        updated_at=config.get("updated_at"),
        api_key_masked=_mask_api_key(config.get("api_key", "")),
    )


@router.get("/providers", response_model=List[ProviderInfo])
async def get_providers():
    """获取支持的模型提供商列表"""
    return PROVIDER_INFO


@router.get("/list", response_model=List[LLMModelConfigOut])
async def list_configs():
    """获取所有模型配置列表"""
    configs = _load_configs()
    return [_config_to_response(c) for c in configs]


@router.get("/{config_id}", response_model=LLMModelConfigOut)
async def get_config(config_id: int):
    """获取单个模型配置"""
    configs = _load_configs()
    for config in configs:
        if config.get("id") == config_id:
            return _config_to_response(config)
    raise HTTPException(status_code=404, detail="配置不存在")


@router.post("/create", response_model=LLMModelConfigOut)
async def create_config(data: LLMModelConfigCreate):
    """创建模型配置"""
    configs = _load_configs()

    # 检查名称是否重复
    for c in configs:
        if c.get("name") == data.name:
            raise HTTPException(status_code=400, detail="配置名称已存在")

    # 如果设置为默认，取消其他默认
    if data.is_default:
        for c in configs:
            c["is_default"] = False

    now = datetime.now().isoformat()
    new_config = data.model_dump()
    new_config["id"] = _get_next_id(configs)
    new_config["created_at"] = now
    new_config["updated_at"] = now

    configs.append(new_config)
    _save_configs(configs)

    return _config_to_response(new_config)


@router.put("/{config_id}", response_model=LLMModelConfigOut)
async def update_config(config_id: int, data: LLMModelConfigUpdate):
    """更新模型配置"""
    configs = _load_configs()

    for i, config in enumerate(configs):
        if config.get("id") == config_id:
            # 检查名称是否与其他配置重复
            if data.name:
                for c in configs:
                    if c.get("id") != config_id and c.get("name") == data.name:
                        raise HTTPException(status_code=400, detail="配置名称已存在")

            # 如果设置为默认，取消其他默认
            if data.is_default:
                for c in configs:
                    c["is_default"] = False

            # 更新字段
            update_data = data.model_dump(exclude_unset=True)
            config.update(update_data)
            config["updated_at"] = datetime.now().isoformat()
            configs[i] = config
            _save_configs(configs)

            return _config_to_response(config)

    raise HTTPException(status_code=404, detail="配置不存在")


@router.delete("/{config_id}")
async def delete_config(config_id: int):
    """删除模型配置"""
    configs = _load_configs()
    for i, config in enumerate(configs):
        if config.get("id") == config_id:
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
        if config.get("id") == config_id:
            config["is_default"] = True
            found = True
        else:
            config["is_default"] = False

    if not found:
        raise HTTPException(status_code=404, detail="配置不存在")

    _save_configs(configs)
    return {"message": "设置成功"}


@router.post("/{config_id}/toggle")
async def toggle_config(config_id: int):
    """启用/禁用模型配置"""
    configs = _load_configs()

    for config in configs:
        if config.get("id") == config_id:
            config["is_enabled"] = not config.get("is_enabled", True)
            config["updated_at"] = datetime.now().isoformat()
            _save_configs(configs)
            return {"is_enabled": config["is_enabled"]}

    raise HTTPException(status_code=404, detail="配置不存在")


@router.post("/{config_id}/test")
async def test_config(config_id: int):
    """测试模型配置"""
    configs = _load_configs()

    for config in configs:
        if config.get("id") == config_id:
            if not config.get("is_enabled", True):
                raise HTTPException(status_code=400, detail="配置已禁用")

            try:
                import httpx

                headers = {
                    "Authorization": f"Bearer {config.get('api_key', '')}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": config.get("model_name", ""),
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10,
                }

                timeout = config.get("timeout", 120)
                api_base = config.get("api_base", "")

                with httpx.Client(timeout=timeout) as client:
                    response = client.post(
                        f"{api_base}/chat/completions",
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