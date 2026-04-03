# AI股票分析平台实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建完整的AI股票分析平台，包含6个功能模块：AI对话助手、AI分析师工作台、AI研报中心、市场洞察、盘后复盘、每日自动分析。

**Architecture:** 采用FastAPI后端 + Vue3前端架构。后端实现多Agent协调器，参考daily_stock_analysis项目的Agent Pipeline设计。前端实现6个独立页面，通过SSE实现流式响应。

**Tech Stack:** FastAPI, Vue 3, TypeScript, Element Plus, SSE, LiteLLM, Redis

**Learned Patterns (from valuecell & TradingAgents):**
- 三层配置系统: 环境变量 > .env > YAML
- Provider回退链: 主Provider失败自动切换备用
- 统一事件类型: BaseResponse基类 + 具体事件子类
- Agent辩论状态: TypedDict状态管理

---

## 文件结构规划

### 后端文件 (backend/stock-service/app/)

```
api/endpoints/
├── ai_chat_routes.py          # AI对话接口
├── ai_agent_routes.py         # 多Agent分析接口
├── ai_report_routes.py        # 研报接口
├── ai_market_routes.py        # 市场洞察接口
├── ai_review_routes.py        # 盘后复盘接口
└── ai_schedule_routes.py      # 定时任务接口

services/
├── ai/
│   ├── __init__.py
│   ├── llm_adapter.py         # LLM适配器 (LiteLLM)
│   ├── tool_registry.py       # 工具注册中心
│   ├── agent_orchestrator.py  # 多Agent协调器
│   ├── context.py             # Agent上下文
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py      # Agent基类
│   │   ├── technical_agent.py # 技术分析Agent
│   │   ├── fundamental_agent.py # 基本面Agent
│   │   ├── news_agent.py      # 消息面Agent
│   │   ├── risk_agent.py      # 风控Agent
│   │   └── decision_agent.py  # 决策Agent
│   ├── skills/
│   │   ├── __init__.py
│   │   └── defaults.py        # 默认策略
│   └── tools/
│       ├── __init__.py
│       └── stock_tools.py     # 股票数据工具
├── ai_chat_service.py         # 对话服务
├── ai_report_service.py       # 研报服务
├── ai_market_service.py       # 市场洞察服务
├── ai_review_service.py       # 盘后复盘服务
└── ai_schedule_service.py     # 定时任务服务

models/
└── ai_models.py               # AI相关数据模型
```

### 前端文件 (frontend/src/)

```
views/Vadmin/Stock/AI/
├── Chat/
│   ├── Chat.vue
│   └── components/
│       ├── StockInfoPanel.vue
│       ├── ChatArea.vue
│       ├── QuickQuestions.vue
│       └── ChatHistory.vue
├── Workbench/
│   ├── Workbench.vue
│   └── components/
│       ├── AnalysisConfig.vue
│       ├── AgentCard.vue
│       ├── AgentPanel.vue
│       ├── DebateRecord.vue
│       ├── SynthesisResult.vue
│       └── FollowUpChat.vue
├── Report/
│   ├── Report.vue
│   └── components/
│       ├── ReportConfig.vue
│       ├── ReportContent.vue
│       ├── ReportToc.vue
│       ├── ReportExport.vue
│       └── ReportHistory.vue
├── MarketInsight/
│   ├── MarketInsight.vue
│   └── components/
│       ├── MarketOverview.vue
│       ├── SectorRotation.vue
│       ├── CapitalFlow.vue
│       ├── HotSpotDiscovery.vue
│       └── AIMarketInterpret.vue
├── DailyReview/
│   ├── DailyReview.vue
│   └── components/
│       ├── DailyReviewReport.vue
│       ├── TradingSummary.vue
│       ├── OpportunityDiscovery.vue
│       ├── RiskWarning.vue
│       └── ReviewHistory.vue
├── Schedule/
│   ├── Schedule.vue
│   └── components/
│       ├── ScheduleConfig.vue
│       ├── StockPool.vue
│       ├── PushConfig.vue
│       └── AnalysisHistory.vue
└── components/
    ├── ModelSelector.vue
    └── StockSearch.vue

api/stock/
└── ai.ts                      # AI相关API
```

---

## Phase 1: 基础架构

### Task 1.1: 创建AI数据模型

**Files:**
- Create: `backend/stock-service/app/models/ai_models.py`

- [ ] **Step 1: 创建AI数据模型文件**

```python
# backend/stock-service/app/models/ai_models.py
# -*- coding: utf-8 -*-
"""
AI分析相关数据模型
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel


class Signal(str, Enum):
    """交易信号"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"


class StageStatus(str, Enum):
    """阶段状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# ========== 请求模型 ==========

class ChatRequest(BaseModel):
    """对话请求"""
    stock_code: str
    message: str
    conversation_id: Optional[str] = None
    model: Optional[str] = None


class AgentAnalyzeRequest(BaseModel):
    """多Agent分析请求"""
    stock_code: str
    query: Optional[str] = ""
    mode: str = "standard"  # quick, standard, full, specialist
    agents: List[str] = ["technical", "fundamental", "news", "risk"]


class ReportGenerateRequest(BaseModel):
    """研报生成请求"""
    stock_code: str
    period: str = "短线"
    dimensions: List[str] = ["technical", "fundamental", "news", "fund_flow", "risk"]
    agents: List[str] = ["technical", "fundamental", "news", "risk"]


class MarketInterpretRequest(BaseModel):
    """市场解读请求"""
    focus: List[str] = []
    depth: str = "standard"


class DailyReviewRequest(BaseModel):
    """每日复盘请求"""
    date: Optional[str] = None
    include_sectors: bool = True
    include_capital_flow: bool = True
    include_outlook: bool = True


class ScheduleCreateRequest(BaseModel):
    """创建定时任务请求"""
    name: str
    cron: str
    stock_pool: List[str]
    agents: List[str]
    push_channels: List[str] = []


# ========== 响应模型 ==========

@dataclass
class AgentOpinion:
    """Agent观点"""
    agent_name: str = ""
    agent_type: str = ""
    signal: str = ""
    confidence: float = 0.0
    reasoning: str = ""
    key_points: List[str] = field(default_factory=list)
    key_levels: Dict[str, float] = field(default_factory=dict)
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StageResult:
    """阶段执行结果"""
    stage_name: str = ""
    status: StageStatus = StageStatus.PENDING
    opinion: Optional[AgentOpinion] = None
    error: Optional[str] = None
    duration_s: float = 0.0
    tokens_used: int = 0


@dataclass
class AgentContext:
    """Agent上下文"""
    query: str = ""
    stock_code: str = ""
    stock_name: str = ""
    session_id: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    opinions: List[AgentOpinion] = field(default_factory=list)
    risk_flags: List[Dict[str, Any]] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SynthesisResult:
    """综合研判结果"""
    conclusion: str = "hold"
    confidence: float = 0.0
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    risk_level: str = "中等"
    operation_advice: str = ""
    key_factors: List[str] = field(default_factory=list)


class ChatResponse(BaseModel):
    """对话响应"""
    content: str
    conversation_id: str
    model: str
    tokens_used: int = 0


class AgentAnalyzeResponse(BaseModel):
    """多Agent分析响应"""
    stock_code: str
    stock_name: str
    opinions: List[Dict[str, Any]]
    synthesis: Dict[str, Any]
    debate: List[Dict[str, Any]]
    duration_s: float
    tokens_used: int


class ReportResponse(BaseModel):
    """研报响应"""
    report_id: str
    stock_code: str
    stock_name: str
    content: str
    conclusion: Dict[str, Any]
    created_at: str


class MarketOverviewResponse(BaseModel):
    """市场概览响应"""
    indices: List[Dict[str, Any]]
    up_down_distribution: Dict[str, Any]
    fear_greed_index: float
    market_sentiment: str


class DailyReviewResponse(BaseModel):
    """每日复盘响应"""
    date: str
    market_summary: str
    sector_analysis: List[Dict[str, Any]]
    capital_flow: Dict[str, Any]
    outlook: str
    ai_suggestions: str
```

- [ ] **Step 2: 验证文件创建成功**

Run: `python -c "from app.models.ai_models import ChatRequest; print('OK')"`
Expected: OK

- [ ] **Step 3: 提交**

```bash
git add backend/stock-service/app/models/ai_models.py
git commit -m "feat(ai): add AI data models"
```

---

### Task 1.2: 创建LLM适配器

**Files:**
- Create: `backend/stock-service/app/services/ai/__init__.py`
- Create: `backend/stock-service/app/services/ai/llm_adapter.py`

- [ ] **Step 1: 创建ai模块目录**

```bash
mkdir -p backend/stock-service/app/services/ai/agents
mkdir -p backend/stock-service/app/services/ai/skills
mkdir -p backend/stock-service/app/services/ai/tools
```

- [ ] **Step 2: 创建__init__.py**

```python
# backend/stock-service/app/services/ai/__init__.py
# -*- coding: utf-8 -*-
"""AI服务模块"""
```

- [ ] **Step 3: 创建LLM适配器**

```python
# backend/stock-service/app/services/ai/llm_adapter.py
# -*- coding: utf-8 -*-
"""
LLM适配器 - 支持多种大模型接口
"""
import os
from typing import Dict, List, Any, Optional, AsyncGenerator
import httpx
import json


class LLMConfig:
    """LLM配置"""
    def __init__(
        self,
        provider: str = "openai",
        model: str = "gpt-4",
        api_key: str = "",
        api_base: str = "",
        max_tokens: int = 4000,
        temperature: float = 0.7,
        timeout: int = 120,
    ):
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout


class LLMToolAdapter:
    """LLM工具适配器 - 支持Function Calling"""

    def __init__(self, config: LLMConfig = None):
        self.config = config or LLMConfig()
        self.client = httpx.AsyncClient(timeout=self.config.timeout)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
        tool_choice: str = "auto",
    ) -> Dict[str, Any]:
        """发送对话请求"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice

        response = await self.client.post(
            f"{self.config.api_base}/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    async def chat_stream(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """流式对话"""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "stream": True,
        }

        if tools:
            payload["tools"] = tools

        async with self.client.stream(
            "POST",
            f"{self.config.api_base}/chat/completions",
            headers=headers,
            json=payload,
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        yield json.loads(data)
                    except json.JSONDecodeError:
                        continue

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()


# 预设模型配置
MODEL_CONFIGS = {
    "gpt-4": LLMConfig(provider="openai", model="gpt-4"),
    "gpt-3.5-turbo": LLMConfig(provider="openai", model="gpt-3.5-turbo"),
    "deepseek-chat": LLMConfig(
        provider="deepseek",
        model="deepseek-chat",
        api_base="https://api.deepseek.com/v1",
    ),
    "qwen-max": LLMConfig(
        provider="aliyun",
        model="qwen-max",
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    ),
}


def get_llm_adapter(model: str = "gpt-4") -> LLMToolAdapter:
    """获取LLM适配器"""
    config = MODEL_CONFIGS.get(model, LLMConfig(model=model))
    return LLMToolAdapter(config)
```

- [ ] **Step 4: 验证LLM适配器**

Run: `python -c "from app.services.ai.llm_adapter import LLMToolAdapter; print('OK')"`
Expected: OK

- [ ] **Step 5: 提交**

```bash
git add backend/stock-service/app/services/ai/
git commit -m "feat(ai): add LLM adapter"
```

---

### Task 1.3: 创建工具注册中心

**Files:**
- Create: `backend/stock-service/app/services/ai/tool_registry.py`

- [ ] **Step 1: 创建工具注册中心**

```python
# backend/stock-service/app/services/ai/tool_registry.py
# -*- coding: utf-8 -*-
"""
工具注册中心 - Agent可调用的工具集
"""
from dataclasses import dataclass
from typing import Callable, List, Optional, Any, Dict
import inspect


@dataclass
class ToolParameter:
    """工具参数"""
    name: str
    type: str  # string, number, integer, boolean, array, object
    description: str
    required: bool = True
    enum: Optional[List[str]] = None
    default: Any = None


@dataclass
class ToolDefinition:
    """工具定义"""
    name: str
    description: str
    parameters: List[ToolParameter]
    handler: Callable
    category: str = "data"  # data, analysis, search, action

    def _params_json_schema(self) -> dict:
        """生成参数JSON Schema"""
        properties: Dict[str, Any] = {}
        required: List[str] = []

        for p in self.parameters:
            prop: Dict[str, Any] = {"type": p.type, "description": p.description}
            if p.enum:
                prop["enum"] = p.enum
            properties[p.name] = prop
            if p.required:
                required.append(p.name)

        schema = {"type": "object", "properties": properties}
        if required:
            schema["required"] = required
        return schema

    def to_openai_tool(self) -> dict:
        """转换为OpenAI工具格式"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self._params_json_schema(),
            },
        }


class ToolRegistry:
    """工具注册中心"""

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool_def: ToolDefinition) -> None:
        """注册工具"""
        self._tools[tool_def.name] = tool_def

    def unregister(self, name: str) -> None:
        """注销工具"""
        self._tools.pop(name, None)

    def get(self, name: str) -> Optional[ToolDefinition]:
        """获取工具"""
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[ToolDefinition]:
        """列出工具"""
        tools = list(self._tools.values())
        if category:
            tools = [t for t in tools if t.category == category]
        return tools

    def list_names(self) -> List[str]:
        """列出工具名称"""
        return list(self._tools.keys())

    def execute(self, name: str, **kwargs) -> Any:
        """执行工具"""
        tool_def = self._tools.get(name)
        if tool_def is None:
            raise KeyError(f"Tool '{name}' not found")
        return tool_def.handler(**kwargs)

    def to_openai_tools(self) -> List[dict]:
        """转换为OpenAI工具列表"""
        return [t.to_openai_tool() for t in self._tools.values()]


# 工具装饰器
_default_registry: Optional[ToolRegistry] = None


def get_default_registry() -> ToolRegistry:
    """获取默认注册中心"""
    global _default_registry
    if _default_registry is None:
        _default_registry = ToolRegistry()
    return _default_registry


def tool(
    name: str,
    description: str,
    category: str = "data",
    parameters: Optional[List[ToolParameter]] = None,
    registry: Optional[ToolRegistry] = None,
):
    """工具装饰器"""
    def decorator(func: Callable) -> Callable:
        # 自动推断参数
        params = parameters or _infer_parameters(func)

        tool_def = ToolDefinition(
            name=name,
            description=description,
            parameters=params,
            handler=func,
            category=category,
        )

        target_registry = registry or get_default_registry()
        target_registry.register(tool_def)

        func._tool_definition = tool_def
        return func

    return decorator


def _infer_parameters(func: Callable) -> List[ToolParameter]:
    """从函数签名推断参数"""
    sig = inspect.signature(func)
    hints = getattr(func, '__annotations__', {})
    params: List[ToolParameter] = []

    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    for param_name, param in sig.parameters.items():
        if param_name in ("self", "cls"):
            continue

        hint = hints.get(param_name, str)
        param_type = type_map.get(hint, "string")

        has_default = param.default is not inspect.Parameter.empty

        params.append(ToolParameter(
            name=param_name,
            type=param_type,
            description=f"Parameter: {param_name}",
            required=not has_default,
            default=param.default if has_default else None,
        ))

    return params
```

- [ ] **Step 2: 验证工具注册中心**

Run: `python -c "from app.services.ai.tool_registry import ToolRegistry; r = ToolRegistry(); print('OK')"`
Expected: OK

- [ ] **Step 3: 提交**

```bash
git add backend/stock-service/app/services/ai/tool_registry.py
git commit -m "feat(ai): add tool registry"
```

---

### Task 1.4: 创建Agent基类和协调器

**Files:**
- Create: `backend/stock-service/app/services/ai/context.py`
- Create: `backend/stock-service/app/services/ai/agents/__init__.py`
- Create: `backend/stock-service/app/services/ai/agents/base_agent.py`
- Create: `backend/stock-service/app/services/ai/agent_orchestrator.py`

- [ ] **Step 1: 创建Agent上下文**

```python
# backend/stock-service/app/services/ai/context.py
# -*- coding: utf-8 -*-
"""
Agent上下文 - 多Agent数据传递
"""
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class AgentContext:
    """Agent共享上下文"""
    query: str = ""
    stock_code: str = ""
    stock_name: str = ""
    session_id: str = ""

    # 收集的数据
    data: Dict[str, Any] = field(default_factory=dict)

    # Agent观点
    opinions: List["AgentOpinion"] = field(default_factory=list)

    # 风险标记
    risk_flags: List[Dict[str, Any]] = field(default_factory=list)

    # 元数据
    meta: Dict[str, Any] = field(default_factory=dict)

    # 时间戳
    created_at: float = field(default_factory=time.time)

    def add_opinion(self, opinion: "AgentOpinion") -> None:
        """添加观点"""
        if opinion.timestamp == 0:
            opinion.timestamp = time.time()
        self.opinions.append(opinion)

    def add_risk_flag(self, category: str, description: str, severity: str = "medium") -> None:
        """添加风险标记"""
        self.risk_flags.append({
            "category": category,
            "description": description,
            "severity": severity,
            "timestamp": time.time(),
        })

    def get_data(self, key: str, default: Any = None) -> Any:
        """获取数据"""
        return self.data.get(key, default)

    def set_data(self, key: str, value: Any) -> None:
        """设置数据"""
        self.data[key] = value

    @property
    def has_risk_flags(self) -> bool:
        """是否有风险标记"""
        return len(self.risk_flags) > 0

    @classmethod
    def create(cls, stock_code: str, query: str = "") -> "AgentContext":
        """创建上下文"""
        return cls(
            query=query,
            stock_code=stock_code,
            session_id=str(uuid.uuid4()),
        )
```

- [ ] **Step 2: 创建Agent基类**

```python
# backend/stock-service/app/services/ai/agents/__init__.py
# -*- coding: utf-8 -*-
"""Agent模块"""
from .base_agent import BaseAgent

__all__ = ["BaseAgent"]
```

```python
# backend/stock-service/app/services/ai/agents/base_agent.py
# -*- coding: utf-8 -*-
"""
Agent基类
"""
import time
import json
from abc import ABC, abstractmethod
from typing import Optional, List, Callable, Dict, Any

from app.services.ai.context import AgentContext
from app.services.ai.tool_registry import ToolRegistry
from app.services.ai.llm_adapter import LLMToolAdapter
from app.models.ai_models import AgentOpinion, StageResult, StageStatus


class BaseAgent(ABC):
    """Agent基类"""

    agent_name: str = "base"
    agent_type: str = "base"
    tool_names: Optional[List[str]] = None
    max_steps: int = 6

    def __init__(
        self,
        tool_registry: ToolRegistry,
        llm_adapter: LLMToolAdapter,
        skill_instructions: str = "",
    ):
        self.tool_registry = tool_registry
        self.llm_adapter = llm_adapter
        self.skill_instructions = skill_instructions

    @abstractmethod
    def system_prompt(self, ctx: AgentContext) -> str:
        """返回系统提示词"""
        pass

    @abstractmethod
    def build_user_message(self, ctx: AgentContext) -> str:
        """构建用户消息"""
        pass

    def post_process(self, ctx: AgentContext, raw_text: str) -> Optional[AgentOpinion]:
        """后处理LLM输出"""
        return None

    def run(
        self,
        ctx: AgentContext,
        progress_callback: Callable[[str], None] = None,
        timeout_seconds: float = None,
    ) -> StageResult:
        """执行Agent分析"""
        t0 = time.time()
        result = StageResult(
            stage_name=self.agent_name,
            status=StageStatus.RUNNING,
        )

        try:
            # 构建消息
            messages = self._build_messages(ctx)

            # 获取工具
            tools = self._get_tools()

            if progress_callback:
                progress_callback(f"🤖 {self.agent_name} 开始分析...")

            # 调用LLM
            import asyncio
            response = asyncio.run(self.llm_adapter.chat(messages, tools=tools))

            # 处理响应
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

            # 处理工具调用
            tool_calls = response.get("choices", [{}])[0].get("message", {}).get("tool_calls", [])
            for tool_call in tool_calls:
                tool_name = tool_call.get("function", {}).get("name", "")
                tool_args = json.loads(tool_call.get("function", {}).get("arguments", "{}"))

                if progress_callback:
                    progress_callback(f"🔧 调用工具: {tool_name}")

                try:
                    tool_result = self.tool_registry.execute(tool_name, **tool_args)
                    ctx.set_data(f"tool_{tool_name}", tool_result)
                except Exception as e:
                    if progress_callback:
                        progress_callback(f"⚠️ 工具调用失败: {e}")

            result.tokens_used = response.get("usage", {}).get("total_tokens", 0)
            result.meta["raw_text"] = content

            # 后处理
            opinion = self.post_process(ctx, content)
            if opinion:
                opinion.agent_name = self.agent_name
                opinion.agent_type = self.agent_type
                ctx.add_opinion(opinion)
                result.opinion = opinion

            result.status = StageStatus.COMPLETED
            if progress_callback:
                progress_callback(f"✅ {self.agent_name} 分析完成")

        except Exception as e:
            result.status = StageStatus.FAILED
            result.error = str(e)
            if progress_callback:
                progress_callback(f"❌ {self.agent_name} 分析失败: {e}")

        finally:
            result.duration_s = round(time.time() - t0, 2)

        return result

    def _build_messages(self, ctx: AgentContext) -> List[Dict[str, str]]:
        """构建消息列表"""
        messages = [
            {"role": "system", "content": self.system_prompt(ctx)},
        ]

        # 注入预取数据
        cached_data = self._inject_cached_data(ctx)
        if cached_data:
            messages.append({"role": "user", "content": cached_data})
            messages.append({"role": "assistant", "content": "好的，我已获取相关数据。"})

        messages.append({"role": "user", "content": self.build_user_message(ctx)})
        return messages

    def _inject_cached_data(self, ctx: AgentContext) -> str:
        """注入缓存数据"""
        parts = []
        for key, value in ctx.data.items():
            if value is not None:
                try:
                    serialized = json.dumps(value, ensure_ascii=False, default=str)
                except:
                    serialized = str(value)
                if len(serialized) > 5000:
                    serialized = serialized[:5000] + "...(truncated)"
                parts.append(f"[{key}]\n{serialized}")
        return "\n\n".join(parts) if parts else ""

    def _get_tools(self) -> List[Dict[str, Any]]:
        """获取可用工具"""
        if self.tool_names is None:
            return self.tool_registry.to_openai_tools()

        tools = []
        for name in self.tool_names:
            tool_def = self.tool_registry.get(name)
            if tool_def:
                tools.append(tool_def.to_openai_tool())
        return tools
```

- [ ] **Step 3: 创建Agent协调器**

```python
# backend/stock-service/app/services/ai/agent_orchestrator.py
# -*- coding: utf-8 -*-
"""
多Agent协调器
"""
import time
import uuid
from typing import List, Dict, Any, Optional, Callable

from app.services.ai.context import AgentContext
from app.services.ai.tool_registry import ToolRegistry
from app.services.ai.llm_adapter import LLMToolAdapter, get_llm_adapter
from app.services.ai.agents.base_agent import BaseAgent
from app.models.ai_models import (
    AgentOpinion, StageResult, StageStatus, SynthesisResult,
    AgentAnalyzeResponse,
)

VALID_MODES = ("quick", "standard", "full", "specialist")


class AgentOrchestrator:
    """多Agent协调器"""

    def __init__(
        self,
        mode: str = "standard",
        model: str = "gpt-4",
        config: Dict = None,
    ):
        self.mode = mode if mode in VALID_MODES else "standard"
        self.model = model
        self.config = config or {}

        self.tool_registry = ToolRegistry()
        self.llm_adapter = get_llm_adapter(model)

        # 注册默认工具
        self._register_default_tools()

    def _register_default_tools(self):
        """注册默认工具"""
        from app.services.ai.tools.stock_tools import register_stock_tools
        register_stock_tools(self.tool_registry)

    def _build_agent_chain(self) -> List[BaseAgent]:
        """构建Agent链"""
        from app.services.ai.agents.technical_agent import TechnicalAgent
        from app.services.ai.agents.fundamental_agent import FundamentalAgent
        from app.services.ai.agents.news_agent import NewsAgent
        from app.services.ai.agents.risk_agent import RiskAgent
        from app.services.ai.agents.decision_agent import DecisionAgent

        agents = []

        if self.mode == "quick":
            agents = [
                TechnicalAgent(self.tool_registry, self.llm_adapter),
                DecisionAgent(self.tool_registry, self.llm_adapter),
            ]
        elif self.mode == "standard":
            agents = [
                TechnicalAgent(self.tool_registry, self.llm_adapter),
                NewsAgent(self.tool_registry, self.llm_adapter),
                DecisionAgent(self.tool_registry, self.llm_adapter),
            ]
        elif self.mode == "full":
            agents = [
                TechnicalAgent(self.tool_registry, self.llm_adapter),
                FundamentalAgent(self.tool_registry, self.llm_adapter),
                NewsAgent(self.tool_registry, self.llm_adapter),
                RiskAgent(self.tool_registry, self.llm_adapter),
                DecisionAgent(self.tool_registry, self.llm_adapter),
            ]
        elif self.mode == "specialist":
            agents = [
                TechnicalAgent(self.tool_registry, self.llm_adapter),
                FundamentalAgent(self.tool_registry, self.llm_adapter),
                NewsAgent(self.tool_registry, self.llm_adapter),
                RiskAgent(self.tool_registry, self.llm_adapter),
                DecisionAgent(self.tool_registry, self.llm_adapter),
            ]

        return agents

    async def run(
        self,
        stock_code: str,
        query: str = "",
        progress_callback: Callable[[str], None] = None,
    ) -> AgentAnalyzeResponse:
        """执行分析"""
        t0 = time.time()

        # 创建上下文
        ctx = AgentContext.create(stock_code=stock_code, query=query)

        # 预取数据
        await self._prefetch_data(ctx, progress_callback)

        # 构建Agent链
        agents = self._build_agent_chain()

        # 执行分析
        stage_results: List[StageResult] = []
        total_tokens = 0

        for agent in agents:
            result = agent.run(ctx, progress_callback)
            stage_results.append(result)
            total_tokens += result.tokens_used

            if result.status == StageStatus.FAILED:
                if progress_callback:
                    progress_callback(f"⚠️ {agent.agent_name} 执行失败: {result.error}")

        # 生成辩论
        debate = self._generate_debate(ctx)

        # 综合研判
        synthesis = self._synthesize(ctx)

        duration = round(time.time() - t0, 2)

        return AgentAnalyzeResponse(
            stock_code=stock_code,
            stock_name=ctx.stock_name or stock_code,
            opinions=[self._opinion_to_dict(o) for o in ctx.opinions],
            synthesis=self._synthesis_to_dict(synthesis),
            debate=debate,
            duration_s=duration,
            tokens_used=total_tokens,
        )

    async def _prefetch_data(self, ctx: AgentContext, progress_callback=None):
        """预取数据"""
        if progress_callback:
            progress_callback("📊 获取股票数据...")

        try:
            # 获取股票基本信息
            from app.services.stock_service import StockService
            stock_service = StockService()

            # 获取股票信息
            info = await stock_service.get_stock_info(ctx.stock_code)
            if info:
                ctx.stock_name = info.get("name", ctx.stock_code)
                ctx.set_data("stock_info", info)

            # 获取实时行情
            quote = await stock_service.get_realtime_quote(ctx.stock_code)
            if quote:
                ctx.set_data("realtime_quote", quote)

            # 获取K线数据
            kline = await stock_service.get_daily_kline(ctx.stock_code, days=60)
            if kline:
                ctx.set_data("daily_kline", kline)

            if progress_callback:
                progress_callback("✅ 数据获取完成")

        except Exception as e:
            if progress_callback:
                progress_callback(f"⚠️ 数据获取失败: {e}")

    def _generate_debate(self, ctx: AgentContext) -> List[Dict[str, Any]]:
        """生成辩论"""
        if len(ctx.opinions) < 2:
            return []

        debate = []
        for i, opinion in enumerate(ctx.opinions):
            debate.append({
                "agent_name": opinion.agent_name,
                "agent_type": opinion.agent_type,
                "content": opinion.reasoning[:500] if opinion.reasoning else "",
                "signal": opinion.signal,
                "confidence": opinion.confidence,
            })

        return debate

    def _synthesize(self, ctx: AgentContext) -> SynthesisResult:
        """综合研判"""
        if not ctx.opinions:
            return SynthesisResult()

        # 简单加权综合
        signal_scores = {
            "strong_buy": 2,
            "buy": 1,
            "hold": 0,
            "sell": -1,
            "strong_sell": -2,
        }

        total_weight = 0
        weighted_score = 0
        total_confidence = 0

        for opinion in ctx.opinions:
            weight = opinion.confidence
            score = signal_scores.get(opinion.signal.lower(), 0)
            weighted_score += score * weight
            total_weight += weight
            total_confidence += opinion.confidence

        avg_score = weighted_score / total_weight if total_weight > 0 else 0
        avg_confidence = total_confidence / len(ctx.opinions) if ctx.opinions else 0

        if avg_score > 1:
            conclusion = "buy"
        elif avg_score > 0.3:
            conclusion = "hold_bullish"
        elif avg_score < -1:
            conclusion = "sell"
        elif avg_score < -0.3:
            conclusion = "hold_bearish"
        else:
            conclusion = "hold"

        return SynthesisResult(
            conclusion=conclusion,
            confidence=min(1.0, avg_confidence * 1.1),
            risk_level="中等" if abs(avg_score) < 1 else "偏高" if avg_score > 0 else "偏低",
            operation_advice=self._generate_operation_advice(conclusion, ctx),
        )

    def _generate_operation_advice(self, conclusion: str, ctx: AgentContext) -> str:
        """生成操作建议"""
        if conclusion == "buy":
            return "建议逢低分批建仓，控制仓位在3-5成，设置止损位。"
        elif conclusion == "sell":
            return "建议逐步减仓或观望，规避风险。"
        elif conclusion == "hold_bullish":
            return "可持有观望，关注支撑位，逢低可小仓介入。"
        elif conclusion == "hold_bearish":
            return "谨慎持有，注意风险，破位及时止损。"
        else:
            return "建议观望为主，等待明确信号。"

    def _opinion_to_dict(self, opinion: AgentOpinion) -> Dict[str, Any]:
        """转换观点为字典"""
        return {
            "agent_name": opinion.agent_name,
            "agent_type": opinion.agent_type,
            "signal": opinion.signal,
            "confidence": opinion.confidence,
            "reasoning": opinion.reasoning,
            "key_points": opinion.key_points,
            "key_levels": opinion.key_levels,
        }

    def _synthesis_to_dict(self, synthesis: SynthesisResult) -> Dict[str, Any]:
        """转换综合结果为字典"""
        return {
            "conclusion": synthesis.conclusion,
            "confidence": synthesis.confidence,
            "target_price": synthesis.target_price,
            "stop_loss": synthesis.stop_loss,
            "risk_level": synthesis.risk_level,
            "operation_advice": synthesis.operation_advice,
            "key_factors": synthesis.key_factors,
        }
```

- [ ] **Step 4: 提交基础架构代码**

```bash
git add backend/stock-service/app/services/ai/
git commit -m "feat(ai): add agent orchestrator and base agent"
```

---

### Task 1.5: 创建具体Agent实现

**Files:**
- Create: `backend/stock-service/app/services/ai/agents/technical_agent.py`
- Create: `backend/stock-service/app/services/ai/agents/fundamental_agent.py`
- Create: `backend/stock-service/app/services/ai/agents/news_agent.py`
- Create: `backend/stock-service/app/services/ai/agents/risk_agent.py`
- Create: `backend/stock-service/app/services/ai/agents/decision_agent.py`

- [ ] **Step 1: 创建技术分析Agent**

```python
# backend/stock-service/app/services/ai/agents/technical_agent.py
# -*- coding: utf-8 -*-
"""
技术分析Agent
"""
import re
from typing import Optional, List

from .base_agent import BaseAgent
from app.services.ai.context import AgentContext
from app.models.ai_models import AgentOpinion


class TechnicalAgent(BaseAgent):
    """技术分析Agent"""

    agent_name = "technical"
    agent_type = "technical"
    tool_names = ["get_realtime_quote", "get_daily_kline", "analyze_trend"]

    SYSTEM_PROMPT = """你是一位资深技术分析师，拥有20年A股技术分析经验。

请基于提供的数据进行技术面分析，关注以下维度：
1. K线形态分析
2. 均线系统（MA5, MA10, MA20, MA60）
3. 技术指标（MACD, KDJ, RSI）
4. 成交量分析
5. 支撑位和压力位

输出格式要求：
- 判断：看多/看空/中性
- 置信度：0-100%
- 关键点位：支撑位、压力位
- 详细分析：包含各维度的具体分析

请确保分析客观、专业，并给出明确的操作建议。"""

    def system_prompt(self, ctx: AgentContext) -> str:
        return self.SYSTEM_PROMPT

    def build_user_message(self, ctx: AgentContext) -> str:
        stock_name = ctx.stock_name or ctx.stock_code
        return f"""请分析 {stock_name}({ctx.stock_code}) 的技术面。

{ctx.query if ctx.query else '请给出技术分析结论。'}"""

    def post_process(self, ctx: AgentContext, raw_text: str) -> Optional[AgentOpinion]:
        """解析LLM输出"""
        opinion = AgentOpinion(
            agent_name=self.agent_name,
            agent_type=self.agent_type,
        )

        # 解析判断
        if "看多" in raw_text or "买入" in raw_text:
            opinion.signal = "buy"
        elif "看空" in raw_text or "卖出" in raw_text:
            opinion.signal = "sell"
        else:
            opinion.signal = "hold"

        # 解析置信度
        confidence_match = re.search(r"置信度[：:]\s*(\d+)%?", raw_text)
        if confidence_match:
            opinion.confidence = float(confidence_match.group(1)) / 100
        else:
            opinion.confidence = 0.6

        opinion.reasoning = raw_text
        opinion.raw_data["analysis"] = raw_text

        return opinion
```

- [ ] **Step 2: 创建其他Agent** (fundamental, news, risk, decision)

由于篇幅限制，其他Agent的实现结构类似，分别关注：
- FundamentalAgent: 基本面分析（PE, PB, ROE, 营收增长等）
- NewsAgent: 消息面分析（新闻、公告、政策等）
- RiskAgent: 风险评估（仓位建议、止损位等）
- DecisionAgent: 综合决策（汇总其他Agent观点）

- [ ] **Step 3: 提交Agent实现**

```bash
git add backend/stock-service/app/services/ai/agents/
git commit -m "feat(ai): add specific agents (technical, fundamental, news, risk, decision)"
```

---

### Task 1.6: 创建股票数据工具

**Files:**
- Create: `backend/stock-service/app/services/ai/tools/__init__.py`
- Create: `backend/stock-service/app/services/ai/tools/stock_tools.py`

- [ ] **Step 1: 创建股票数据工具**

```python
# backend/stock-service/app/services/ai/tools/__init__.py
# -*- coding: utf-8 -*-
"""工具模块"""
```

```python
# backend/stock-service/app/services/ai/tools/stock_tools.py
# -*- coding: utf-8 -*-
"""
股票数据工具
"""
import akshare as ak
from typing import Dict, List, Any

from app.services.ai.tool_registry import ToolRegistry, tool, ToolParameter


def register_stock_tools(registry: ToolRegistry):
    """注册股票数据工具"""

    @tool(
        name="get_realtime_quote",
        description="获取股票实时行情数据",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码"),
        ],
        registry=registry,
    )
    def get_realtime_quote(stock_code: str) -> Dict[str, Any]:
        """获取实时行情"""
        try:
            df = ak.stock_zh_a_spot_em()
            row = df[df['代码'] == stock_code]
            if row.empty:
                return {"error": f"股票 {stock_code} 未找到"}

            data = row.iloc[0].to_dict()
            return {
                "code": data.get("代码"),
                "name": data.get("名称"),
                "price": float(data.get("最新价", 0)),
                "change_percent": float(data.get("涨跌幅", 0)),
                "change": float(data.get("涨跌额", 0)),
                "volume": float(data.get("成交量", 0)),
                "amount": float(data.get("成交额", 0)),
                "high": float(data.get("最高", 0)),
                "low": float(data.get("最低", 0)),
                "open": float(data.get("今开", 0)),
                "pre_close": float(data.get("昨收", 0)),
            }
        except Exception as e:
            return {"error": str(e)}

    @tool(
        name="get_daily_kline",
        description="获取股票日K线历史数据",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码"),
            ToolParameter(name="days", type="integer", description="获取天数", default=60),
        ],
        registry=registry,
    )
    def get_daily_kline(stock_code: str, days: int = 60) -> List[Dict[str, Any]]:
        """获取日K线"""
        try:
            df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", adjust="qfq")
            if df.empty:
                return []

            df = df.tail(days)
            return df.to_dict("records")
        except Exception as e:
            return [{"error": str(e)}]

    @tool(
        name="analyze_trend",
        description="分析股票趋势",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码"),
        ],
        registry=registry,
    )
    def analyze_trend(stock_code: str) -> Dict[str, Any]:
        """分析趋势"""
        try:
            kline = get_daily_kline(stock_code, 30)
            if not kline or "error" in kline[0]:
                return {"error": "无法获取K线数据"}

            closes = [float(k.get("收盘", 0)) for k in kline[-20:]]

            # 简单趋势判断
            ma5 = sum(closes[-5:]) / 5
            ma10 = sum(closes[-10:]) / 10
            ma20 = sum(closes[-20:]) / 20

            trend = "up" if ma5 > ma10 > ma20 else "down" if ma5 < ma10 < ma20 else "sideways"

            return {
                "trend": trend,
                "ma5": round(ma5, 2),
                "ma10": round(ma10, 2),
                "ma20": round(ma20, 2),
                "latest_close": closes[-1] if closes else 0,
            }
        except Exception as e:
            return {"error": str(e)}

    @tool(
        name="get_stock_news",
        description="获取股票相关新闻",
        parameters=[
            ToolParameter(name="stock_code", type="string", description="股票代码"),
        ],
        registry=registry,
    )
    def get_stock_news(stock_code: str) -> List[Dict[str, Any]]:
        """获取股票新闻"""
        try:
            df = ak.stock_news_em(symbol=stock_code)
            if df.empty:
                return []
            return df.head(10).to_dict("records")
        except Exception as e:
            return [{"error": str(e)}]
```

- [ ] **Step 2: 提交工具代码**

```bash
git add backend/stock-service/app/services/ai/tools/
git commit -m "feat(ai): add stock data tools"
```

---

## Phase 2: API路由

### Task 2.1: 创建AI对话API

**Files:**
- Create: `backend/stock-service/app/api/endpoints/ai_chat_routes.py`

- [ ] **Step 1: 创建AI对话路由**

```python
# backend/stock-service/app/api/endpoints/ai_chat_routes.py
# -*- coding: utf-8 -*-
"""
AI对话接口
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from typing import Optional
import json
import uuid

from app.models.ai_models import ChatRequest, ChatResponse
from app.services.ai.llm_adapter import get_llm_adapter

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """AI对话"""
    llm = get_llm_adapter(request.model or "gpt-4")

    messages = [
        {"role": "system", "content": "你是一位专业的股票分析师，请基于数据给出客观、专业的分析建议。"},
        {"role": "user", "content": f"股票代码: {request.stock_code}\n问题: {request.message}"},
    ]

    try:
        response = await llm.chat(messages)
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")

        return ChatResponse(
            content=content,
            conversation_id=request.conversation_id or str(uuid.uuid4()),
            model=request.model or "gpt-4",
            tokens_used=response.get("usage", {}).get("total_tokens", 0),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """AI对话流式响应"""
    llm = get_llm_adapter(request.model or "gpt-4")

    messages = [
        {"role": "system", "content": "你是一位专业的股票分析师，请基于数据给出客观、专业的分析建议。"},
        {"role": "user", "content": f"股票代码: {request.stock_code}\n问题: {request.message}"},
    ]

    async def generate():
        try:
            async for chunk in llm.chat_stream(messages):
                delta = chunk.get("choices", [{}])[0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    yield {"data": json.dumps({"content": content})}
            yield {"data": "[DONE]"}
        except Exception as e:
            yield {"data": json.dumps({"error": str(e)})}

    return EventSourceResponse(generate())
```

- [ ] **Step 2: 提交**

```bash
git add backend/stock-service/app/api/endpoints/ai_chat_routes.py
git commit -m "feat(ai): add AI chat API"
```

---

### Task 2.2: 创建多Agent分析API

**Files:**
- Create: `backend/stock-service/app/api/endpoints/ai_agent_routes.py`

- [ ] **Step 1: 创建多Agent分析路由**

```python
# backend/stock-service/app/api/endpoints/ai_agent_routes.py
# -*- coding: utf-8 -*-
"""
多Agent分析接口
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from typing import Optional
import json

from app.models.ai_models import AgentAnalyzeRequest, AgentAnalyzeResponse
from app.services.ai.agent_orchestrator import AgentOrchestrator

router = APIRouter()


@router.post("/analyze", response_model=AgentAnalyzeResponse)
async def analyze(request: AgentAnalyzeRequest):
    """多Agent分析"""
    orchestrator = AgentOrchestrator(
        mode=request.mode,
        model="gpt-4",  # 可配置
    )

    try:
        result = await orchestrator.run(
            stock_code=request.stock_code,
            query=request.query or "",
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/stream")
async def analyze_stream(request: AgentAnalyzeRequest):
    """多Agent分析流式响应"""

    async def generate():
        orchestrator = AgentOrchestrator(mode=request.mode)

        progress_messages = []

        def progress_callback(msg: str):
            progress_messages.append(msg)

        try:
            yield {"data": json.dumps({"type": "start", "message": "开始分析..."})}

            result = await orchestrator.run(
                stock_code=request.stock_code,
                query=request.query or "",
                progress_callback=progress_callback,
            )

            for msg in progress_messages:
                yield {"data": json.dumps({"type": "progress", "message": msg})}

            yield {"data": json.dumps({
                "type": "result",
                "data": result.model_dump(),
            })}

        except Exception as e:
            yield {"data": json.dumps({"type": "error", "message": str(e)})}

    return EventSourceResponse(generate())
```

- [ ] **Step 2: 提交**

```bash
git add backend/stock-service/app/api/endpoints/ai_agent_routes.py
git commit -m "feat(ai): add multi-agent analysis API"
```

---

### Task 2.3: 更新路由注册

**Files:**
- Modify: `backend/stock-service/app/api/router.py`

- [ ] **Step 1: 添加AI路由注册**

在 `router.py` 中添加：

```python
# 在文件开头添加导入
try:
    from app.api.endpoints import ai_chat_routes
except ImportError:
    ai_chat_routes = None

try:
    from app.api.endpoints import ai_agent_routes
except ImportError:
    ai_agent_routes = None

# 在 api_router.include_router 部分添加
if ai_chat_routes:
    api_router.include_router(
        ai_chat_routes.router, prefix="/ai", tags=["ai-chat"]
    )
if ai_agent_routes:
    api_router.include_router(
        ai_agent_routes.router, prefix="/ai/agents", tags=["ai-agents"]
    )
```

- [ ] **Step 2: 提交**

```bash
git add backend/stock-service/app/api/router.py
git commit -m "feat(ai): register AI routes"
```

---

## 进度概览

### 已完成 (Phase 1-2 基础架构)
- [x] AI数据模型 (`ai_models.py`)
- [x] LLM配置模型 (`llm_config_models.py`)
- [x] LLM适配器 (`llm_adapter.py`)
- [x] 工具注册中心 (`tool_registry.py`)
- [x] Agent上下文 (`context.py`)
- [x] Agent协调器 (`agent_orchestrator.py`)
- [x] Agent基类和具体Agent实现
- [x] 股票数据工具 (`stock_tools.py`)
- [x] AI对话API (`ai_chat_routes.py`)
- [x] 多Agent分析API (`ai_agent_routes.py`)
- [x] LLM配置管理API (`llm_config_routes.py`)
- [x] 前端AI对话页面 (`Chat.vue`)
- [x] 前端分析师工作台 (`Workbench.vue`)
- [x] 前端LLM配置页面 (`LLMConfig.vue`)
- [x] 路由配置

### 待优化 (应用学习成果)

#### Phase 2.5: 架构优化 (基于valuecell/TradingAgents学习)

**Task 2.5.1: 模型工厂优化 - Provider回退链**

- [ ] **Step 1: 创建三层配置系统**

新建: `backend/stock-service/app/services/ai/config/`

```python
# config/manager.py - 三层配置管理器
class ConfigManager:
    """配置优先级: 环境变量 > .env > YAML"""

    def __init__(self, config_dir: str = "configs"):
        self.config_dir = Path(config_dir)
        self._yaml_config = self._load_yaml()
        self._env_config = self._load_env()

    def get(self, key: str, default: Any = None) -> Any:
        # 优先级: 环境变量 > .env > YAML
        if os.getenv(key):
            return os.getenv(key)
        if key in self._env_config:
            return self._env_config[key]
        return self._yaml_config.get(key, default)
```

- [ ] **Step 2: 创建模型工厂 (参考valuecell)**

```python
# adapters/models/factory.py - 模型工厂
class ModelFactory:
    _providers = {
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
        "aliyun": AliyunProvider,
        "zhipu": ZhipuProvider,
    }

    def create_model_for_agent(
        self,
        agent_name: str,
        use_fallback: bool = True,
        **kwargs
    ):
        """为特定Agent创建模型，支持自动回退"""
        config = self.config_manager.get_agent_config(agent_name)

        # Provider回退链
        if use_fallback and config.fallback_providers:
            providers = [config.primary_provider] + config.fallback_providers
            for provider in providers:
                try:
                    return self._create(provider, config)
                except Exception:
                    continue
            raise RuntimeError("All providers failed")
        return self._create(config.primary_provider, config)
```

- [ ] **Step 3: 创建Agent配置YAML**

```yaml
# configs/agents/default.yaml
agents:
  technical_agent:
    primary_model:
      provider: "openai"
      model_id: "gpt-4"
      provider_models:  # 不同Provider的模型映射
        deepseek: "deepseek-chat"
        aliyun: "qwen-max"
    fallback_providers: ["deepseek", "aliyun"]
    max_tokens: 4000
    temperature: 0.7

  fundamental_agent:
    primary_model:
      provider: "deepseek"
      model_id: "deepseek-chat"
    fallback_providers: ["openai"]
    max_tokens: 6000
    temperature: 0.5
```

**Task 2.5.2: 统一流式事件系统**

- [ ] **Step 1: 定义统一事件类型**

```python
# services/ai/events.py
class StreamEventType(str, Enum):
    MESSAGE_CHUNK = "message_chunk"
    TOOL_CALL_STARTED = "tool_call_started"
    TOOL_CALL_COMPLETED = "tool_call_completed"
    REASONING_STARTED = "reasoning_started"
    REASONING = "reasoning"
    REASONING_COMPLETED = "reasoning_completed"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    STAGE_PROGRESS = "stage_progress"

class BaseStreamEvent(BaseModel):
    event: StreamEventType
    timestamp: float = Field(default_factory=time.time)
    data: Dict[str, Any] = {}

class MessageChunkEvent(BaseStreamEvent):
    event: StreamEventType = StreamEventType.MESSAGE_CHUNK
    content: str = ""

class ToolCallEvent(BaseStreamEvent):
    event: StreamEventType = StreamEventType.TOOL_CALL_STARTED
    tool_name: str = ""
    arguments: Dict[str, Any] = {}

class AgentEvent(BaseStreamEvent):
    event: StreamEventType = StreamEventType.AGENT_STARTED
    agent_name: str = ""
    agent_type: str = ""
```

- [ ] **Step 2: 更新SSE响应格式**

```python
# 统一SSE格式
async def generate_stream():
    async for event in orchestrator.stream():
        yield f"data: {event.model_dump_json()}\n\n"
    yield "data: [DONE]\n\n"
```

**Task 2.5.3: Agent辩论状态管理**

- [ ] **Step 1: 定义辩论状态 (参考TradingAgents)**

```python
# services/ai/states.py
from typing import TypedDict, Annotated

class AgentDebateState(TypedDict):
    """Agent辩论状态"""
    bull_history: Annotated[str, "多头观点历史"]
    bear_history: Annotated[str, "空头观点历史"]
    judge_decision: Annotated[str, "最终判断"]
    debate_round: Annotated[int, "辩论轮次"]
    max_rounds: Annotated[int, "最大轮次"]

class MultiAgentState(TypedDict):
    """多Agent状态"""
    stock_code: str
    stock_name: str
    query: str
    technical_report: str
    fundamental_report: str
    news_report: str
    risk_assessment: str
    final_decision: str
    debate_state: AgentDebateState
```

- [ ] **Step 2: 实现辩论Agent**

```python
# agents/debate_agents.py
class BullResearcher(BaseAgent):
    """多头研究员"""
    agent_name = "bull_researcher"
    agent_type = "debate"

    def system_prompt(self, ctx: AgentContext) -> str:
        return """你是一位多头研究员，负责从看多角度分析股票。
        请基于数据给出支持买入的论据，反驳空头观点。"""

class BearResearcher(BaseAgent):
    """空头研究员"""
    agent_name = "bear_researcher"
    agent_type = "debate"

    def system_prompt(self, ctx: AgentContext) -> str:
        return """你是一位空头研究员，负责从看空角度分析股票。
        请基于数据给出支持卖出的论据，反驳多头观点。"""

class DebateJudge(BaseAgent):
    """辩论法官"""
    agent_name = "debate_judge"
    agent_type = "decision"

    def run_debate(self, state: AgentDebateState) -> str:
        """根据多空辩论做出最终判断"""
        pass
```

**Task 2.5.4: 后台生产者模式**

- [ ] **Step 1: 实现后台生产者 (参考valuecell编排器)**

```python
# services/ai/orchestrator.py
class AgentOrchestrator:
    async def process_with_queue(
        self,
        user_input: str,
        emit: Callable[[BaseStreamEvent], None]
    ) -> AsyncGenerator[BaseStreamEvent, None]:
        """后台生产者模式，确保断线后任务继续执行"""
        queue: asyncio.Queue[Optional[BaseStreamEvent]] = asyncio.Queue()

        async def producer():
            try:
                async for event in self._run_session(user_input):
                    await queue.put(event)
            finally:
                await queue.put(None)  # 结束标记

        asyncio.create_task(producer())

        while True:
            event = await queue.get()
            if event is None:
                break
            yield event
```

---

## Phase 3-7 详细任务

### Task 3.1: 创建AI API文件

**Files:**
- Create: `frontend/src/api/stock/ai.ts`

- [ ] **Step 1: 创建AI API**

```typescript
// frontend/src/api/stock/ai.ts
import request from '@/config/axios'

// ========== AI对话 ==========
export const aiChat = (data: {
  stock_code: string
  message: string
  conversation_id?: string
  model?: string
}) => {
  return request.post({ url: '/ai/chat', data })
}

// ========== 多Agent分析 ==========
export const agentAnalyze = (data: {
  stock_code: string
  query?: string
  mode?: string
  agents?: string[]
}) => {
  return request.post({ url: '/ai/agents/analyze', data })
}

// ========== 研报生成 ==========
export const generateReport = (data: {
  stock_code: string
  period?: string
  dimensions?: string[]
  agents?: string[]
}) => {
  return request.post({ url: '/ai/report/generate', data })
}

export const getReport = (reportId: string) => {
  return request.get({ url: `/ai/report/${reportId}` })
}

export const exportReport = (reportId: string, format: string = 'pdf') => {
  return request.get({ url: `/ai/report/${reportId}/export`, params: { format } })
}

// ========== 市场洞察 ==========
export const getMarketOverview = () => {
  return request.get({ url: '/ai/market/overview' })
}

export const getSectorRotation = () => {
  return request.get({ url: '/ai/market/sectors' })
}

export const getCapitalFlow = () => {
  return request.get({ url: '/ai/market/capital-flow' })
}

export const interpretMarket = (data: { focus?: string[]; depth?: string }) => {
  return request.post({ url: '/ai/market/interpret', data })
}

// ========== 盘后复盘 ==========
export const getDailyReview = (params: { date?: string }) => {
  return request.get({ url: '/ai/review/daily', params })
}

export const getTradingSummary = (params: { date?: string }) => {
  return request.get({ url: '/ai/review/trading-summary', params })
}

export const discoverOpportunities = (data: {
  focus_sectors?: string[]
  risk_preference?: string
}) => {
  return request.post({ url: '/ai/review/opportunities', data })
}

export const getRiskWarnings = () => {
  return request.get({ url: '/ai/review/risk-warnings' })
}

// ========== 定时任务 ==========
export const createSchedule = (data: {
  name: string
  cron: string
  stock_pool: string[]
  agents: string[]
  push_channels?: string[]
}) => {
  return request.post({ url: '/ai/schedule/create', data })
}

export const getScheduleList = () => {
  return request.get({ url: '/ai/schedule/list' })
}

export const deleteSchedule = (scheduleId: string) => {
  return request.delete({ url: `/ai/schedule/${scheduleId}` })
}
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/api/stock/ai.ts
git commit -m "feat(frontend): add AI API"
```

---

### Task 3.2: 创建AI对话助手页面

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/AI/Chat/Chat.vue`
- Create: `frontend/src/views/Vadmin/Stock/AI/Chat/components/StockInfoPanel.vue`
- Create: `frontend/src/views/Vadmin/Stock/AI/Chat/components/ChatArea.vue`

- [ ] **Step 1: 创建主页面 Chat.vue**

由于代码较长，这里给出关键结构：

```vue
<!-- frontend/src/views/Vadmin/Stock/AI/Chat/Chat.vue -->
<template>
  <div class="ai-chat-container">
    <el-row :gutter="20">
      <!-- 左侧：股票信息面板 -->
      <el-col :span="6">
        <StockInfoPanel
          :stock-code="stockCode"
          @select="handleStockSelect"
        />
      </el-col>

      <!-- 右侧：对话区域 -->
      <el-col :span="18">
        <ChatArea
          :stock-code="stockCode"
          :messages="messages"
          :loading="loading"
          @send="handleSend"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { aiChat } from '@/api/stock/ai'
import StockInfoPanel from './components/StockInfoPanel.vue'
import ChatArea from './components/ChatArea.vue'

const stockCode = ref('')
const loading = ref(false)
const messages = reactive<Array<{ role: string; content: string }>>([])

const handleStockSelect = (code: string) => {
  stockCode.value = code
}

const handleSend = async (message: string) => {
  if (!stockCode.value) {
    ElMessage.warning('请先选择股票')
    return
  }

  messages.push({ role: 'user', content: message })
  loading.value = true

  try {
    const res = await aiChat({
      stock_code: stockCode.value,
      message,
    })
    messages.push({ role: 'assistant', content: res.data.content })
  } catch (error) {
    ElMessage.error('分析失败')
  } finally {
    loading.value = false
  }
}
</script>
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/views/Vadmin/Stock/AI/Chat/
git commit -m "feat(frontend): add AI chat page"
```

---

### Task 3.3: 创建分析师工作台页面

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/AI/Workbench/Workbench.vue`
- Create: `frontend/src/views/Vadmin/Stock/AI/Workbench/components/AgentCard.vue`
- Create: `frontend/src/views/Vadmin/Stock/AI/Workbench/components/SynthesisResult.vue`

- [ ] **Step 1: 创建工作台主页面**

关键组件结构，实际实现需要更完整的代码。

- [ ] **Step 2: 提交**

```bash
git add frontend/src/views/Vadmin/Stock/AI/Workbench/
git commit -m "feat(frontend): add AI workbench page"
```

---

### Task 3.4: 添加路由配置

**Files:**
- Modify: `frontend/src/router/index.ts`

- [ ] **Step 1: 添加AI模块路由**

在 `asyncRouterMap` 的 `Stock` children 中添加：

```typescript
{
  path: 'ai-chat',
  component: () => import('@/views/Vadmin/Stock/AI/Chat/Chat.vue'),
  name: 'AIChat',
  meta: { title: 'AI对话助手', noCache: true }
},
{
  path: 'ai-workbench',
  component: () => import('@/views/Vadmin/Stock/AI/Workbench/Workbench.vue'),
  name: 'AIWorkbench',
  meta: { title: 'AI分析师工作台', noCache: true }
},
{
  path: 'ai-report',
  component: () => import('@/views/Vadmin/Stock/AI/Report/Report.vue'),
  name: 'AIReport',
  meta: { title: 'AI研报中心', noCache: true }
},
{
  path: 'ai-market-insight',
  component: () => import('@/views/Vadmin/Stock/AI/MarketInsight/MarketInsight.vue'),
  name: 'AIMarketInsight',
  meta: { title: '市场洞察', noCache: true }
},
{
  path: 'ai-daily-review',
  component: () => import('@/views/Vadmin/Stock/AI/DailyReview/DailyReview.vue'),
  name: 'AIDailyReview',
  meta: { title: '盘后复盘', noCache: true }
},
{
  path: 'ai-schedule',
  component: () => import('@/views/Vadmin/Stock/AI/Schedule/Schedule.vue'),
  name: 'AISchedule',
  meta: { title: '每日自动分析', noCache: true }
},
```

- [ ] **Step 2: 提交**

```bash
git add frontend/src/router/index.ts
git commit -m "feat(frontend): add AI routes"
```

---

## 实施说明

### 执行方式

此计划可通过以下方式执行：

1. **Subagent-Driven (推荐)**: 每个Task由独立的子Agent执行，主Agent在任务间进行review

2. **Inline Execution**: 在当前会话中按步骤执行，批量执行并在检查点review

### 验证方式

每个Phase完成后进行集成测试：

```bash
# 启动后端
cd backend/stock-service && uvicorn app.main:app --reload

# 测试API
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Content-Type: application/json" \
  -d '{"stock_code": "000001", "message": "分析一下这只股票"}'

curl -X POST http://localhost:8000/api/v1/ai/agents/analyze \
  -H "Content-Type: application/json" \
  -d '{"stock_code": "000001", "mode": "standard"}'
```

### 后续Phase

Phase 4-7的详细任务在此省略，结构类似：

- Phase 4: 研报中心（研报生成、展示、导出）
- Phase 5: 市场洞察（市场概览、板块轮动、资金流向）
- Phase 6: 盘后复盘（每日报告、机会挖掘、风险预警）
- Phase 7: 定时任务（调度配置、推送通知）

每个Phase包含：后端API → 前端页面 → 路由配置 → 测试验证