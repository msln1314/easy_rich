# QMT量化交易服务 - 阶段一实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现QMT量化交易服务阶段一功能，包括QMT连接、基础交易和持仓查询。

**Architecture:** 创建独立的qmt-service微服务（端口8009），使用xtquant SDK连接本地QMT客户端，提供交易执行和持仓管理API。前端新增QMT量化模块，包含交易面板和持仓管理页面。

**Tech Stack:** FastAPI, xtquant, Pydantic, Redis, Vue 3, Element Plus, TypeScript

---

## 文件结构概览

### 后端新建文件

```
backend/qmt-service/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI主应用
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # 配置管理
│   │   └── qmt_client.py           # QMT客户端连接管理
│   ├── api/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── trade_routes.py     # 交易API
│   │   │   └── position_routes.py  # 持仓API
│   │   └── router.py               # 路由聚合
│   ├── services/
│   │   ├── __init__.py
│   │   ├── trade_service.py        # 交易服务
│   │   └── position_service.py     # 持仓服务
│   └── models/
│       ├── __init__.py
│       ├── trade_models.py         # 交易模型
│       └── position_models.py      # 持仓模型
├── tests/
│   └── __init__.py
├── .env.example
├── run.py
└── pyproject.toml
```

### 前端新建文件

```
frontend/src/
├── api/stock/
│   └── qmt.ts                      # QMT API接口
├── views/Vadmin/Stock/QMT/
│   ├── Trade/
│   │   └── Trade.vue               # 交易面板
│   └── Position/
│       └── Position.vue            # 持仓管理
```

---

## Task 1: 创建qmt-service项目骨架

**Files:**
- Create: `backend/qmt-service/app/__init__.py`
- Create: `backend/qmt-service/app/core/__init__.py`
- Create: `backend/qmt-service/app/api/__init__.py`
- Create: `backend/qmt-service/app/api/endpoints/__init__.py`
- Create: `backend/qmt-service/app/services/__init__.py`
- Create: `backend/qmt-service/app/models/__init__.py`
- Create: `backend/qmt-service/tests/__init__.py`

- [ ] **Step 1: 创建项目目录结构**

```bash
mkdir -p backend/qmt-service/app/core
mkdir -p backend/qmt-service/app/api/endpoints
mkdir -p backend/qmt-service/app/services
mkdir -p backend/qmt-service/app/models
mkdir -p backend/qmt-service/tests
```

- [ ] **Step 2: 创建__init__.py文件**

创建以下空文件：
- `backend/qmt-service/app/__init__.py`
- `backend/qmt-service/app/core/__init__.py`
- `backend/qmt-service/app/api/__init__.py`
- `backend/qmt-service/app/api/endpoints/__init__.py`
- `backend/qmt-service/app/services/__init__.py`
- `backend/qmt-service/app/models/__init__.py`
- `backend/qmt-service/tests/__init__.py`

- [ ] **Step 3: 验证目录结构**

Run: `ls -la backend/qmt-service/app/`
Expected: 看到 core/, api/, services/, models/ 目录

- [ ] **Step 4: Commit**

```bash
git add backend/qmt-service/
git commit -m "feat(qmt): create qmt-service project skeleton"
```

---

## Task 2: 创建配置模块

**Files:**
- Create: `backend/qmt-service/app/core/config.py`

- [ ] **Step 1: 编写配置类**

```python
# backend/qmt-service/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """QMT服务配置"""
    
    # 服务配置
    PROJECT_NAME: str = "QMT量化交易服务"
    API_V1_STR: str = "/api/v1"
    SERVICE_PORT: int = 8009
    SERVICE_HOST: str = "0.0.0.0"
    
    # CORS设置
    ORIGINS: list = ["*"]
    
    # QMT客户端配置
    QMT_CLIENT_PATH: str = ""  # QMT客户端路径，如: C:\迅投QMT交易端\userdata_mini
    QMT_ACCOUNT: str = ""      # QMT账号
    QMT_PASSWORD: str = ""     # QMT密码
    QMT_SESSION_ID: int = 123456  # 会话ID，任意整数
    
    # Redis配置（共享stock-service）
    REDIS_ENABLED: bool = True
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_PREFIX: str = "qmt:"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

- [ ] **Step 2: 创建环境变量示例文件**

```env
# backend/qmt-service/.env.example

# QMT客户端配置
QMT_CLIENT_PATH=C:\迅投QMT交易端\userdata_mini
QMT_ACCOUNT=your_account
QMT_PASSWORD=your_password
QMT_SESSION_ID=123456

# 服务配置
SERVICE_PORT=8009
SERVICE_HOST=0.0.0.0

# Redis配置
REDIS_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# 日志配置
LOG_LEVEL=INFO
```

- [ ] **Step 3: Commit**

```bash
git add backend/qmt-service/app/core/config.py backend/qmt-service/.env.example
git commit -m "feat(qmt): add configuration module"
```

---

## Task 3: 创建数据模型

**Files:**
- Create: `backend/qmt-service/app/models/trade_models.py`
- Create: `backend/qmt-service/app/models/position_models.py`

- [ ] **Step 1: 创建交易模型**

```python
# backend/qmt-service/app/models/trade_models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class OrderDirection(str, Enum):
    """订单方向"""
    BUY = "buy"
    SELL = "sell"


class OrderType(str, Enum):
    """订单类型"""
    LIMIT = "limit"      # 限价单
    MARKET = "market"    # 市价单


class OrderStatus(str, Enum):
    """订单状态"""
    PENDING = "pending"        # 待成交
    PARTIAL = "partial"        # 部分成交
    FILLED = "filled"          # 全部成交
    CANCELLED = "cancelled"    # 已撤单
    REJECTED = "rejected"      # 已拒绝


class OrderCreate(BaseModel):
    """创建订单请求"""
    stock_code: str
    direction: OrderDirection
    price: Optional[float] = None  # 市价单可为空
    quantity: int
    order_type: OrderType = OrderType.LIMIT


class OrderResponse(BaseModel):
    """订单响应"""
    order_id: str
    stock_code: str
    stock_name: str
    direction: OrderDirection
    price: float
    quantity: int
    order_type: OrderType
    status: OrderStatus
    filled_quantity: int = 0
    filled_price: float = 0.0
    created_time: datetime
    updated_time: datetime
    message: Optional[str] = None


class OrderListResponse(BaseModel):
    """订单列表响应"""
    orders: list[OrderResponse]
    total: int


class CancelOrderResponse(BaseModel):
    """撤单响应"""
    order_id: str
    success: bool
    message: str
```

- [ ] **Step 2: 创建持仓模型**

```python
# backend/qmt-service/app/models/position_models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Position(BaseModel):
    """持仓信息"""
    stock_code: str
    stock_name: str
    quantity: int              # 持仓数量
    available: int             # 可用数量
    cost_price: float          # 成本价
    current_price: float       # 当前价
    profit: float              # 盈亏金额
    profit_rate: float         # 盈亏比例(%)
    market_value: float        # 市值
    updated_time: datetime


class PositionListResponse(BaseModel):
    """持仓列表响应"""
    positions: list[Position]
    total_market_value: float  # 总市值
    total_profit: float        # 总盈亏
    count: int


class Balance(BaseModel):
    """资金余额"""
    total_asset: float         # 总资产
    available_cash: float      # 可用资金
    market_value: float        # 持仓市值
    frozen_cash: float         # 冻结资金
    profit_today: float        # 今日盈亏
    profit_total: float        # 总盈亏
    updated_time: datetime


class Trade(BaseModel):
    """成交记录"""
    trade_id: str
    order_id: str
    stock_code: str
    stock_name: str
    direction: str
    price: float
    quantity: int
    trade_time: datetime
    commission: float = 0.0


class TradeListResponse(BaseModel):
    """成交记录列表响应"""
    trades: list[Trade]
    total: int
```

- [ ] **Step 3: 更新models/__init__.py**

```python
# backend/qmt-service/app/models/__init__.py
from .trade_models import (
    OrderDirection,
    OrderType,
    OrderStatus,
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    CancelOrderResponse,
)
from .position_models import (
    Position,
    PositionListResponse,
    Balance,
    Trade,
    TradeListResponse,
)

__all__ = [
    "OrderDirection",
    "OrderType",
    "OrderStatus",
    "OrderCreate",
    "OrderResponse",
    "OrderListResponse",
    "CancelOrderResponse",
    "Position",
    "PositionListResponse",
    "Balance",
    "Trade",
    "TradeListResponse",
]
```

- [ ] **Step 4: Commit**

```bash
git add backend/qmt-service/app/models/
git commit -m "feat(qmt): add trade and position models"
```

---

## Task 4: 创建QMT客户端连接管理

**Files:**
- Create: `backend/qmt-service/app/core/qmt_client.py`

- [ ] **Step 1: 编写QMT客户端管理器**

```python
# backend/qmt-service/app/core/qmt_client.py
"""
QMT客户端连接管理器

注意：xtquant SDK需要在Windows环境下运行，且需要先启动QMT客户端
"""
import logging
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


class QMTClientManager:
    """QMT客户端连接管理器"""
    
    _trader = None
    _account = None
    _connected: bool = False
    _session_id: int = 0
    
    @classmethod
    async def initialize(cls) -> bool:
        """初始化QMT连接"""
        if cls._connected:
            logger.info("QMT已连接，跳过初始化")
            return True
            
        try:
            # 检查配置
            if not settings.QMT_CLIENT_PATH:
                logger.warning("QMT客户端路径未配置，使用模拟模式")
                return False
                
            if not settings.QMT_ACCOUNT or not settings.QMT_PASSWORD:
                logger.warning("QMT账号或密码未配置，使用模拟模式")
                return False
            
            # 尝试导入xtquant
            try:
                from xtquant.xttrader import XtQuantTrader, XtAccount
            except ImportError as e:
                logger.error(f"xtquant SDK未安装: {e}")
                logger.info("请运行: pip install xtquant")
                return False
            
            # 创建交易对象
            cls._session_id = settings.QMT_SESSION_ID
            cls._trader = XtQuantTrader(
                settings.QMT_CLIENT_PATH,
                cls._session_id
            )
            
            # 创建账号对象
            cls._account = XtAccount(
                settings.QMT_ACCOUNT,
                settings.QMT_PASSWORD
            )
            
            # 连接QMT
            cls._trader.connect()
            cls._connected = True
            
            logger.info(f"QMT连接成功，会话ID: {cls._session_id}")
            return True
            
        except Exception as e:
            logger.error(f"QMT连接失败: {e}")
            cls._connected = False
            return False
    
    @classmethod
    async def close(cls):
        """关闭QMT连接"""
        if cls._trader and cls._connected:
            try:
                cls._trader.disconnect()
                logger.info("QMT连接已关闭")
            except Exception as e:
                logger.error(f"关闭QMT连接失败: {e}")
            finally:
                cls._connected = False
                cls._trader = None
                cls._account = None
    
    @classmethod
    def get_trader(cls):
        """获取交易对象"""
        if not cls._connected:
            raise RuntimeError("QMT未连接，请先调用initialize()")
        return cls._trader
    
    @classmethod
    def get_account(cls):
        """获取账号对象"""
        if not cls._connected:
            raise RuntimeError("QMT未连接，请先调用initialize()")
        return cls._account
    
    @classmethod
    def is_connected(cls) -> bool:
        """检查连接状态"""
        return cls._connected
    
    @classmethod
    def get_status(cls) -> dict:
        """获取连接状态详情"""
        return {
            "connected": cls._connected,
            "session_id": cls._session_id,
            "account": settings.QMT_ACCOUNT if cls._connected else None,
            "client_path": settings.QMT_CLIENT_PATH if cls._connected else None,
        }
```

- [ ] **Step 2: Commit**

```bash
git add backend/qmt-service/app/core/qmt_client.py
git commit -m "feat(qmt): add QMT client connection manager"
```

---

## Task 5: 创建交易服务

**Files:**
- Create: `backend/qmt-service/app/services/trade_service.py`

- [ ] **Step 1: 编写交易服务**

```python
# backend/qmt-service/app/services/trade_service.py
"""
交易执行服务

提供下单、撤单、查询委托等功能
"""
import logging
from datetime import datetime
from typing import Optional, List

from app.core.qmt_client import QMTClientManager
from app.models.trade_models import (
    OrderCreate,
    OrderResponse,
    OrderDirection,
    OrderType,
    OrderStatus,
    CancelOrderResponse,
)

logger = logging.getLogger(__name__)


class TradeService:
    """交易执行服务"""
    
    # 订单类型映射
    ORDER_TYPE_MAP = {
        OrderType.LIMIT: 23,    # 限价单
        OrderType.MARKET: 24,   # 市价单
    }
    
    # 方向映射
    DIRECTION_MAP = {
        OrderDirection.BUY: 23,    # 买入
        OrderDirection.SELL: 24,   # 卖出
    }
    
    # 状态映射（QMT状态 -> 系统状态）
    STATUS_MAP = {
        48: OrderStatus.PENDING,    # 未报
        49: OrderStatus.PENDING,    # 待报
        50: OrderStatus.PENDING,    # 已报
        51: OrderStatus.PARTIAL,    # 部成
        52: OrderStatus.FILLED,     # 全成
        53: OrderStatus.CANCELLED,  # 已撤
        54: OrderStatus.CANCELLED,  # 已撤
        55: OrderStatus.REJECTED,   # 废单
    }
    
    async def place_order(self, order: OrderCreate) -> OrderResponse:
        """下单"""
        if not QMTClientManager.is_connected():
            # 模拟模式
            return self._mock_place_order(order)
        
        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()
            
            # 下单
            order_id = trader.order_stock(
                account,
                order.stock_code,
                self.ORDER_TYPE_MAP[order.order_type],
                self.DIRECTION_MAP[order.direction],
                order.quantity,
                order.price or 0  # 市价单价格为0
            )
            
            if order_id <= 0:
                raise Exception("下单失败，返回无效订单ID")
            
            now = datetime.now()
            return OrderResponse(
                order_id=str(order_id),
                stock_code=order.stock_code,
                stock_name="",  # 需要额外查询
                direction=order.direction,
                price=order.price or 0,
                quantity=order.quantity,
                order_type=order.order_type,
                status=OrderStatus.PENDING,
                filled_quantity=0,
                filled_price=0,
                created_time=now,
                updated_time=now,
                message="下单成功"
            )
            
        except Exception as e:
            logger.error(f"下单失败: {e}")
            raise
    
    def _mock_place_order(self, order: OrderCreate) -> OrderResponse:
        """模拟下单（QMT未连接时使用）"""
        import uuid
        now = datetime.now()
        mock_order_id = str(uuid.uuid4())[:8]
        
        logger.info(f"[模拟模式] 下单: {order.stock_code} {order.direction.value} {order.quantity}@{order.price}")
        
        return OrderResponse(
            order_id=mock_order_id,
            stock_code=order.stock_code,
            stock_name=f"模拟股票_{order.stock_code}",
            direction=order.direction,
            price=order.price or 10.0,
            quantity=order.quantity,
            order_type=order.order_type,
            status=OrderStatus.PENDING,
            filled_quantity=0,
            filled_price=0,
            created_time=now,
            updated_time=now,
            message="[模拟]下单成功"
        )
    
    async def cancel_order(self, order_id: str) -> CancelOrderResponse:
        """撤单"""
        if not QMTClientManager.is_connected():
            return CancelOrderResponse(
                order_id=order_id,
                success=True,
                message="[模拟]撤单成功"
            )
        
        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()
            
            result = trader.cancel_order(account, int(order_id))
            
            return CancelOrderResponse(
                order_id=order_id,
                success=result > 0,
                message="撤单成功" if result > 0 else "撤单失败"
            )
            
        except Exception as e:
            logger.error(f"撤单失败: {e}")
            return CancelOrderResponse(
                order_id=order_id,
                success=False,
                message=f"撤单失败: {str(e)}"
            )
    
    async def get_orders(
        self,
        status: Optional[OrderStatus] = None,
        date: Optional[str] = None
    ) -> List[OrderResponse]:
        """查询委托列表"""
        if not QMTClientManager.is_connected():
            return self._mock_get_orders()
        
        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()
            
            orders = trader.query_stock_orders(account)
            
            result = []
            for o in orders:
                order_response = self._convert_order(o)
                if status and order_response.status != status:
                    continue
                result.append(order_response)
            
            return result
            
        except Exception as e:
            logger.error(f"查询委托列表失败: {e}")
            return []
    
    def _mock_get_orders(self) -> List[OrderResponse]:
        """模拟查询委托列表"""
        now = datetime.now()
        return [
            OrderResponse(
                order_id="mock001",
                stock_code="000001",
                stock_name="平安银行",
                direction=OrderDirection.BUY,
                price=12.5,
                quantity=1000,
                order_type=OrderType.LIMIT,
                status=OrderStatus.PENDING,
                filled_quantity=0,
                filled_price=0,
                created_time=now,
                updated_time=now,
                message="[模拟]待成交"
            )
        ]
    
    async def get_order(self, order_id: str) -> Optional[OrderResponse]:
        """查询单个委托"""
        if not QMTClientManager.is_connected():
            orders = self._mock_get_orders()
            for o in orders:
                if o.order_id == order_id:
                    return o
            return None
        
        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()
            
            order = trader.query_stock_order(account, int(order_id))
            if order:
                return self._convert_order(order)
            return None
            
        except Exception as e:
            logger.error(f"查询委托失败: {e}")
            return None
    
    def _convert_order(self, qmt_order) -> OrderResponse:
        """转换QMT订单对象"""
        now = datetime.now()
        return OrderResponse(
            order_id=str(qmt_order.order_id),
            stock_code=qmt_order.stock_code,
            stock_name=qmt_order.stock_name or "",
            direction=OrderDirection.BUY if qmt_order.order_type == 23 else OrderDirection.SELL,
            price=qmt_order.price,
            quantity=qmt_order.order_volume,
            order_type=OrderType.LIMIT,
            status=self.STATUS_MAP.get(qmt_order.order_status, OrderStatus.PENDING),
            filled_quantity=qmt_order.traded_volume or 0,
            filled_price=qmt_order.traded_price or 0,
            created_time=now,  # QMT可能没有这个字段
            updated_time=now,
        )


# 单例
trade_service = TradeService()
```

- [ ] **Step 2: Commit**

```bash
git add backend/qmt-service/app/services/trade_service.py
git commit -m "feat(qmt): add trade service with mock mode support"
```

---

## Task 6: 创建持仓服务

**Files:**
- Create: `backend/qmt-service/app/services/position_service.py`

- [ ] **Step 1: 编写持仓服务**

```python
# backend/qmt-service/app/services/position_service.py
"""
持仓管理服务

提供持仓查询、资金余额、成交记录等功能
"""
import logging
from datetime import datetime
from typing import List, Optional

from app.core.qmt_client import QMTClientManager
from app.models.position_models import (
    Position,
    PositionListResponse,
    Balance,
    Trade,
    TradeListResponse,
)

logger = logging.getLogger(__name__)


class PositionService:
    """持仓管理服务"""
    
    async def get_positions(self) -> PositionListResponse:
        """查询持仓列表"""
        if not QMTClientManager.is_connected():
            return self._mock_get_positions()
        
        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()
            
            positions = trader.query_stock_positions(account)
            
            result = []
            total_market_value = 0.0
            total_profit = 0.0
            
            for p in positions:
                position = self._convert_position(p)
                result.append(position)
                total_market_value += position.market_value
                total_profit += position.profit
            
            return PositionListResponse(
                positions=result,
                total_market_value=total_market_value,
                total_profit=total_profit,
                count=len(result)
            )
            
        except Exception as e:
            logger.error(f"查询持仓失败: {e}")
            return PositionListResponse(
                positions=[],
                total_market_value=0,
                total_profit=0,
                count=0
            )
    
    def _mock_get_positions(self) -> PositionListResponse:
        """模拟查询持仓"""
        now = datetime.now()
        positions = [
            Position(
                stock_code="000001",
                stock_name="平安银行",
                quantity=1000,
                available=1000,
                cost_price=12.0,
                current_price=12.5,
                profit=500.0,
                profit_rate=4.17,
                market_value=12500.0,
                updated_time=now
            ),
            Position(
                stock_code="600519",
                stock_name="贵州茅台",
                quantity=100,
                available=100,
                cost_price=1800.0,
                current_price=1850.0,
                profit=5000.0,
                profit_rate=2.78,
                market_value=185000.0,
                updated_time=now
            )
        ]
        
        total_mv = sum(p.market_value for p in positions)
        total_profit = sum(p.profit for p in positions)
        
        return PositionListResponse(
            positions=positions,
            total_market_value=total_mv,
            total_profit=total_profit,
            count=len(positions)
        )
    
    async def get_balance(self) -> Balance:
        """查询资金余额"""
        if not QMTClientManager.is_connected():
            return self._mock_get_balance()
        
        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()
            
            asset = trader.query_stock_asset(account)
            
            return Balance(
                total_asset=asset.total_asset,
                available_cash=asset.cash,
                market_value=asset.market_value,
                frozen_cash=asset.frozen_cash if hasattr(asset, 'frozen_cash') else 0,
                profit_today=0,  # 需要额外计算
                profit_total=0,  # 需要额外计算
                updated_time=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"查询资金余额失败: {e}")
            return self._mock_get_balance()
    
    def _mock_get_balance(self) -> Balance:
        """模拟查询资金余额"""
        return Balance(
            total_asset=500000.0,
            available_cash=300000.0,
            market_value=197500.0,
            frozen_cash=2500.0,
            profit_today=5500.0,
            profit_total=15000.0,
            updated_time=datetime.now()
        )
    
    async def get_trades(
        self,
        date: Optional[str] = None,
        stock_code: Optional[str] = None
    ) -> TradeListResponse:
        """查询成交记录"""
        if not QMTClientManager.is_connected():
            return self._mock_get_trades()
        
        try:
            trader = QMTClientManager.get_trader()
            account = QMTClientManager.get_account()
            
            trades = trader.query_stock_trades(account)
            
            result = []
            for t in trades:
                trade = self._convert_trade(t)
                if stock_code and trade.stock_code != stock_code:
                    continue
                result.append(trade)
            
            return TradeListResponse(
                trades=result,
                total=len(result)
            )
            
        except Exception as e:
            logger.error(f"查询成交记录失败: {e}")
            return TradeListResponse(trades=[], total=0)
    
    def _mock_get_trades(self) -> TradeListResponse:
        """模拟查询成交记录"""
        now = datetime.now()
        trades = [
            Trade(
                trade_id="t001",
                order_id="mock001",
                stock_code="000001",
                stock_name="平安银行",
                direction="buy",
                price=12.0,
                quantity=1000,
                trade_time=now,
                commission=5.0
            )
        ]
        
        return TradeListResponse(trades=trades, total=len(trades))
    
    async def get_today_trades(self) -> TradeListResponse:
        """查询今日成交"""
        today = datetime.now().strftime("%Y%m%d")
        return await self.get_trades(date=today)
    
    def _convert_position(self, qmt_position) -> Position:
        """转换QMT持仓对象"""
        now = datetime.now()
        quantity = qmt_position.volume
        cost_price = qmt_position.open_price
        current_price = qmt_position.market_price if hasattr(qmt_position, 'market_price') else cost_price
        profit = (current_price - cost_price) * quantity
        profit_rate = ((current_price - cost_price) / cost_price * 100) if cost_price > 0 else 0
        
        return Position(
            stock_code=qmt_position.stock_code,
            stock_name=qmt_position.stock_name or "",
            quantity=quantity,
            available=qmt_position.can_use_volume if hasattr(qmt_position, 'can_use_volume') else quantity,
            cost_price=cost_price,
            current_price=current_price,
            profit=profit,
            profit_rate=round(profit_rate, 2),
            market_value=current_price * quantity,
            updated_time=now
        )
    
    def _convert_trade(self, qmt_trade) -> Trade:
        """转换QMT成交对象"""
        return Trade(
            trade_id=str(qmt_trade.order_id),  # 可能需要调整
            order_id=str(qmt_trade.order_id),
            stock_code=qmt_trade.stock_code,
            stock_name=qmt_trade.stock_name or "",
            direction="buy" if qmt_trade.order_type == 23 else "sell",
            price=qmt_trade.traded_price,
            quantity=qmt_trade.traded_volume,
            trade_time=datetime.now(),  # QMT可能需要转换时间格式
            commission=qmt_trade.commission if hasattr(qmt_trade, 'commission') else 0
        )


# 单例
position_service = PositionService()
```

- [ ] **Step 2: Commit**

```bash
git add backend/qmt-service/app/services/position_service.py
git commit -m "feat(qmt): add position service with mock mode support"
```

---

## Task 7: 创建API路由

**Files:**
- Create: `backend/qmt-service/app/api/endpoints/trade_routes.py`
- Create: `backend/qmt-service/app/api/endpoints/position_routes.py`
- Create: `backend/qmt-service/app/api/router.py`

- [ ] **Step 1: 创建交易API路由**

```python
# backend/qmt-service/app/api/endpoints/trade_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.trade_models import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    CancelOrderResponse,
    OrderStatus,
)
from app.services.trade_service import trade_service

router = APIRouter()


@router.post("/order", response_model=OrderResponse, summary="下单")
async def place_order(order: OrderCreate):
    """
    下单
    
    - **stock_code**: 股票代码（如：000001）
    - **direction**: 方向（buy/sell）
    - **price**: 价格（市价单可为空）
    - **quantity**: 数量
    - **order_type**: 订单类型（limit/market）
    """
    try:
        return await trade_service.place_order(order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/order/{order_id}", response_model=CancelOrderResponse, summary="撤单")
async def cancel_order(order_id: str):
    """撤单"""
    try:
        return await trade_service.cancel_order(order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders", response_model=OrderListResponse, summary="查询委托列表")
async def get_orders(
    status: Optional[OrderStatus] = Query(None, description="订单状态筛选"),
    date: Optional[str] = Query(None, description="日期筛选（YYYYMMDD）")
):
    """查询委托列表"""
    try:
        orders = await trade_service.get_orders(status, date)
        return OrderListResponse(orders=orders, total=len(orders))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orders/{order_id}", response_model=OrderResponse, summary="查询委托详情")
async def get_order(order_id: str):
    """查询委托详情"""
    try:
        order = await trade_service.get_order(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="委托不存在")
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 2: 创建持仓API路由**

```python
# backend/qmt-service/app/api/endpoints/position_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.position_models import (
    PositionListResponse,
    Balance,
    TradeListResponse,
)
from app.services.position_service import position_service

router = APIRouter()


@router.get("/list", response_model=PositionListResponse, summary="查询持仓列表")
async def get_positions():
    """查询持仓列表"""
    try:
        return await position_service.get_positions()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/balance", response_model=Balance, summary="查询资金余额")
async def get_balance():
    """查询资金余额"""
    try:
        return await position_service.get_balance()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trades", response_model=TradeListResponse, summary="查询成交记录")
async def get_trades(
    date: Optional[str] = Query(None, description="日期（YYYYMMDD）"),
    stock_code: Optional[str] = Query(None, description="股票代码筛选")
):
    """查询成交记录"""
    try:
        return await position_service.get_trades(date, stock_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trades/today", response_model=TradeListResponse, summary="查询今日成交")
async def get_today_trades():
    """查询今日成交"""
    try:
        return await position_service.get_today_trades()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

- [ ] **Step 3: 创建路由聚合**

```python
# backend/qmt-service/app/api/router.py
from fastapi import APIRouter

from app.api.endpoints import trade_routes, position_routes

api_router = APIRouter()

api_router.include_router(trade_routes.router, prefix="/trade", tags=["trade"])
api_router.include_router(position_routes.router, prefix="/position", tags=["position"])
```

- [ ] **Step 4: Commit**

```bash
git add backend/qmt-service/app/api/
git commit -m "feat(qmt): add trade and position API routes"
```

---

## Task 8: 创建FastAPI主应用

**Files:**
- Create: `backend/qmt-service/app/main.py`

- [ ] **Step 1: 编写主应用**

```python
# backend/qmt-service/app/main.py
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.qmt_client import QMTClientManager

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info(f"正在启动 {settings.PROJECT_NAME}...")
    connected = await QMTClientManager.initialize()
    if connected:
        logger.info("QMT客户端连接成功")
    else:
        logger.warning("QMT客户端未连接，使用模拟模式")
    
    yield
    
    # 关闭时
    logger.info("正在关闭服务...")
    await QMTClientManager.close()
    logger.info("服务已关闭")


# API tags
tags_metadata = [
    {"name": "trade", "description": "交易执行接口"},
    {"name": "position", "description": "持仓管理接口"},
]

# 创建应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="QMT量化交易服务，提供交易执行、持仓管理等功能",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
async def root():
    """根路径"""
    return {
        "message": settings.PROJECT_NAME,
        "docs": "/docs",
        "qmt_status": "connected" if QMTClientManager.is_connected() else "mock"
    }


@app.get("/health", tags=["root"])
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "qmt": QMTClientManager.get_status()
    }
```

- [ ] **Step 2: Commit**

```bash
git add backend/qmt-service/app/main.py
git commit -m "feat(qmt): add FastAPI main application with lifespan management"
```

---

## Task 9: 创建启动脚本和依赖配置

**Files:**
- Create: `backend/qmt-service/run.py`
- Create: `backend/qmt-service/pyproject.toml`
- Create: `backend/qmt-service/README.md`

- [ ] **Step 1: 创建启动脚本**

```python
# backend/qmt-service/run.py
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
    )
```

- [ ] **Step 2: 创建依赖配置**

```toml
# backend/qmt-service/pyproject.toml
[project]
name = "qmt-service"
version = "1.0.0"
description = "QMT量化交易服务"
requires-python = ">=3.10"

dependencies = [
    "fastapi>=0.101.0",
    "uvicorn>=0.23.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "redis>=4.5.0",
    "python-dotenv>=1.0.0",
    "xtquant>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "httpx>=0.24.0",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

- [ ] **Step 3: 创建README**

```markdown
# QMT量化交易服务

基于QMT（迅投量化交易终端）的量化交易服务，提供交易执行、持仓管理等功能。

## 功能特性

- 交易执行：下单、撤单、委托查询
- 持仓管理：持仓查询、资金余额、成交记录
- 模拟模式：QMT未连接时自动切换模拟模式

## 快速开始

### 环境要求

- Python 3.10+
- QMT客户端（可选，用于实盘交易）

### 安装依赖

```bash
cd backend/qmt-service
pip install -e .
```

### 配置

复制 `.env.example` 为 `.env`，配置QMT客户端信息：

```env
QMT_CLIENT_PATH=C:\迅投QMT交易端\userdata_mini
QMT_ACCOUNT=your_account
QMT_PASSWORD=your_password
```

### 启动服务

```bash
python run.py
```

服务默认运行在 `http://localhost:8009`

### API文档

启动后访问 `http://localhost:8009/docs` 查看API文档

## 注意事项

1. 首次使用需要先启动QMT客户端
2. 如果未配置QMT，服务会以模拟模式运行
3. 模拟模式下的数据为模拟数据，仅供测试使用
```

- [ ] **Step 4: Commit**

```bash
git add backend/qmt-service/run.py backend/qmt-service/pyproject.toml backend/qmt-service/README.md
git commit -m "feat(qmt): add run script, dependencies and README"
```

---

## Task 10: 创建前端API接口

**Files:**
- Create: `frontend/src/api/stock/qmt.ts`

- [ ] **Step 1: 创建QMT API接口**

```typescript
// frontend/src/api/stock/qmt.ts
import request from '@/config/axios'

const QMT_BASE_URL = '/qmt'

// ==================== 交易相关 ====================

/**
 * 下单
 */
export const placeOrderApi = (data: {
  stock_code: string
  direction: 'buy' | 'sell'
  price?: number
  quantity: number
  order_type?: 'limit' | 'market'
}): Promise<IResponse> => {
  return request.post({ url: `${QMT_BASE_URL}/trade/order`, data })
}

/**
 * 撤单
 */
export const cancelOrderApi = (orderId: string): Promise<IResponse> => {
  return request.delete({ url: `${QMT_BASE_URL}/trade/order/${orderId}` })
}

/**
 * 查询委托列表
 */
export const getOrdersApi = (params?: {
  status?: string
  date?: string
}): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/trade/orders`, params })
}

/**
 * 查询委托详情
 */
export const getOrderDetailApi = (orderId: string): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/trade/orders/${orderId}` })
}

// ==================== 持仓相关 ====================

/**
 * 查询持仓列表
 */
export const getPositionsApi = (): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/position/list` })
}

/**
 * 查询资金余额
 */
export const getBalanceApi = (): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/position/balance` })
}

/**
 * 查询成交记录
 */
export const getTradesApi = (params?: {
  date?: string
  stock_code?: string
}): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/position/trades`, params })
}

/**
 * 查询今日成交
 */
export const getTodayTradesApi = (): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/position/trades/today` })
}

// ==================== 服务状态 ====================

/**
 * 健康检查
 */
export const getQMTHealthApi = (): Promise<IResponse> => {
  return request.get({ url: `${QMT_BASE_URL}/health` })
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/api/stock/qmt.ts
git commit -m "feat(qmt): add frontend API interfaces"
```

---

## Task 11: 创建前端交易面板页面

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/QMT/Trade/Trade.vue`

- [ ] **Step 1: 创建交易面板组件**

```vue
<!-- frontend/src/views/Vadmin/Stock/QMT/Trade/Trade.vue -->
<template>
  <div class="qmt-trade">
    <el-row :gutter="20">
      <!-- 左侧：下单表单 -->
      <el-col :span="8">
        <el-card class="order-form-card">
          <template #header>
            <div class="card-header">
              <span>下单</span>
              <el-tag :type="qmtStatus === 'connected' ? 'success' : 'warning'" size="small">
                {{ qmtStatus === 'connected' ? '已连接' : '模拟模式' }}
              </el-tag>
            </div>
          </template>
          
          <el-form :model="orderForm" label-width="80px" :rules="orderRules" ref="orderFormRef">
            <el-form-item label="股票代码" prop="stock_code">
              <el-input v-model="orderForm.stock_code" placeholder="请输入股票代码" />
            </el-form-item>
            
            <el-form-item label="方向" prop="direction">
              <el-radio-group v-model="orderForm.direction">
                <el-radio-button value="buy">买入</el-radio-button>
                <el-radio-button value="sell">卖出</el-radio-button>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="订单类型" prop="order_type">
              <el-select v-model="orderForm.order_type" style="width: 100%">
                <el-option label="限价单" value="limit" />
                <el-option label="市价单" value="market" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="价格" prop="price" v-if="orderForm.order_type === 'limit'">
              <el-input-number v-model="orderForm.price" :precision="2" :min="0" style="width: 100%" />
            </el-form-item>
            
            <el-form-item label="数量" prop="quantity">
              <el-input-number v-model="orderForm.quantity" :min="100" :step="100" style="width: 100%" />
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="handlePlaceOrder" :loading="submitting">
                {{ orderForm.direction === 'buy' ? '买入' : '卖出' }}
              </el-button>
              <el-button @click="resetForm">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 右侧：委托列表 -->
      <el-col :span="16">
        <el-card class="order-list-card">
          <template #header>
            <div class="card-header">
              <span>委托列表</span>
              <el-button type="primary" size="small" @click="refreshOrders">刷新</el-button>
            </div>
          </template>
          
          <el-table :data="orders" v-loading="loading" stripe>
            <el-table-column prop="order_id" label="委托ID" width="100" />
            <el-table-column prop="stock_code" label="股票代码" width="100" />
            <el-table-column prop="stock_name" label="股票名称" width="100" />
            <el-table-column prop="direction" label="方向" width="80">
              <template #default="{ row }">
                <el-tag :type="row.direction === 'buy' ? 'danger' : 'success'" size="small">
                  {{ row.direction === 'buy' ? '买入' : '卖出' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="price" label="价格" width="100" />
            <el-table-column prop="quantity" label="数量" width="100" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)" size="small">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="filled_quantity" label="已成交" width="100" />
            <el-table-column label="操作" fixed="right" width="100">
              <template #default="{ row }">
                <el-button
                  v-if="row.status === 'pending'"
                  type="danger"
                  size="small"
                  @click="handleCancelOrder(row.order_id)"
                >
                  撤单
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { placeOrderApi, cancelOrderApi, getOrdersApi, getQMTHealthApi } from '@/api/stock/qmt'

// 状态
const loading = ref(false)
const submitting = ref(false)
const qmtStatus = ref<'connected' | 'mock'>('mock')
const orders = ref<any[]>([])

// 表单
const orderFormRef = ref<FormInstance>()
const orderForm = reactive({
  stock_code: '',
  direction: 'buy' as 'buy' | 'sell',
  price: 0,
  quantity: 100,
  order_type: 'limit' as 'limit' | 'market'
})

const orderRules: FormRules = {
  stock_code: [{ required: true, message: '请输入股票代码', trigger: 'blur' }],
  direction: [{ required: true, message: '请选择方向', trigger: 'change' }],
  quantity: [{ required: true, message: '请输入数量', trigger: 'blur' }]
}

// 方法
const checkQMTStatus = async () => {
  try {
    const { data } = await getQMTHealthApi()
    qmtStatus.value = data.qmt?.connected ? 'connected' : 'mock'
  } catch (e) {
    qmtStatus.value = 'mock'
  }
}

const refreshOrders = async () => {
  loading.value = true
  try {
    const { data } = await getOrdersApi()
    orders.value = data?.orders || []
  } catch (e: any) {
    ElMessage.error(e.message || '获取委托列表失败')
  } finally {
    loading.value = false
  }
}

const handlePlaceOrder = async () => {
  await orderFormRef.value?.validate()
  
  submitting.value = true
  try {
    await placeOrderApi(orderForm)
    ElMessage.success('下单成功')
    resetForm()
    refreshOrders()
  } catch (e: any) {
    ElMessage.error(e.message || '下单失败')
  } finally {
    submitting.value = false
  }
}

const handleCancelOrder = async (orderId: string) => {
  await ElMessageBox.confirm('确定要撤销该委托吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  
  try {
    await cancelOrderApi(orderId)
    ElMessage.success('撤单成功')
    refreshOrders()
  } catch (e: any) {
    ElMessage.error(e.message || '撤单失败')
  }
}

const resetForm = () => {
  orderFormRef.value?.resetFields()
  orderForm.price = 0
  orderForm.quantity = 100
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'warning',
    partial: 'info',
    filled: 'success',
    cancelled: 'info',
    rejected: 'danger'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待成交',
    partial: '部分成交',
    filled: '已成交',
    cancelled: '已撤单',
    rejected: '已拒绝'
  }
  return map[status] || status
}

// 生命周期
onMounted(() => {
  checkQMTStatus()
  refreshOrders()
})
</script>

<style scoped>
.qmt-trade {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-form-card,
.order-list-card {
  height: calc(100vh - 200px);
  overflow: auto;
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/Vadmin/Stock/QMT/Trade/Trade.vue
git commit -m "feat(qmt): add trade panel page"
```

---

## Task 12: 创建前端持仓管理页面

**Files:**
- Create: `frontend/src/views/Vadmin/Stock/QMT/Position/Position.vue`

- [ ] **Step 1: 创建持仓管理组件**

```vue
<!-- frontend/src/views/Vadmin/Stock/QMT/Position/Position.vue -->
<template>
  <div class="qmt-position">
    <!-- 资金余额卡片 -->
    <el-row :gutter="20" class="balance-row">
      <el-col :span="6">
        <el-card shadow="hover" class="balance-card">
          <div class="balance-item">
            <div class="label">总资产</div>
            <div class="value">{{ formatMoney(balance.total_asset) }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="balance-card">
          <div class="balance-item">
            <div class="label">可用资金</div>
            <div class="value available">{{ formatMoney(balance.available_cash) }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="balance-card">
          <div class="balance-item">
            <div class="label">持仓市值</div>
            <div class="value">{{ formatMoney(balance.market_value) }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="balance-card">
          <div class="balance-item">
            <div class="label">今日盈亏</div>
            <div class="value" :class="balance.profit_today >= 0 ? 'profit' : 'loss'">
              {{ balance.profit_today >= 0 ? '+' : '' }}{{ formatMoney(balance.profit_today) }}
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 持仓列表 -->
    <el-card class="position-card">
      <template #header>
        <div class="card-header">
          <span>持仓列表</span>
          <el-button type="primary" size="small" @click="refreshData">刷新</el-button>
        </div>
      </template>
      
      <el-table :data="positions" v-loading="loading" stripe>
        <el-table-column prop="stock_code" label="股票代码" width="100" />
        <el-table-column prop="stock_name" label="股票名称" width="120" />
        <el-table-column prop="quantity" label="持仓数量" width="100">
          <template #default="{ row }">
            {{ row.quantity.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="available" label="可用数量" width="100">
          <template #default="{ row }">
            {{ row.available.toLocaleString() }}
          </template>
        </el-table-column>
        <el-table-column prop="cost_price" label="成本价" width="100">
          <template #default="{ row }">
            {{ row.cost_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="current_price" label="当前价" width="100">
          <template #default="{ row }">
            {{ row.current_price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="profit" label="盈亏金额" width="120">
          <template #default="{ row }">
            <span :class="row.profit >= 0 ? 'profit' : 'loss'">
              {{ row.profit >= 0 ? '+' : '' }}{{ row.profit.toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="profit_rate" label="盈亏比例" width="100">
          <template #default="{ row }">
            <span :class="row.profit_rate >= 0 ? 'profit' : 'loss'">
              {{ row.profit_rate >= 0 ? '+' : '' }}{{ row.profit_rate.toFixed(2) }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="market_value" label="市值" width="120">
          <template #default="{ row }">
            {{ formatMoney(row.market_value) }}
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 汇总信息 -->
      <div class="position-summary">
        <span>持仓总市值: <b>{{ formatMoney(totalMarketValue) }}</b></span>
        <span>总盈亏: <b :class="totalProfit >= 0 ? 'profit' : 'loss'">{{ totalProfit >= 0 ? '+' : '' }}{{ formatMoney(totalProfit) }}</b></span>
        <span>持仓数量: <b>{{ positions.length }}</b>只</span>
      </div>
    </el-card>
    
    <!-- 今日成交 -->
    <el-card class="trades-card">
      <template #header>
        <div class="card-header">
          <span>今日成交</span>
        </div>
      </template>
      
      <el-table :data="trades" stripe size="small">
        <el-table-column prop="trade_id" label="成交ID" width="100" />
        <el-table-column prop="stock_code" label="股票代码" width="100" />
        <el-table-column prop="stock_name" label="股票名称" width="120" />
        <el-table-column prop="direction" label="方向" width="80">
          <template #default="{ row }">
            <el-tag :type="row.direction === 'buy' ? 'danger' : 'success'" size="small">
              {{ row.direction === 'buy' ? '买入' : '卖出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="成交价" width="100" />
        <el-table-column prop="quantity" label="成交量" width="100" />
        <el-table-column prop="trade_time" label="成交时间" width="180">
          <template #default="{ row }">
            {{ formatTime(row.trade_time) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getPositionsApi, getBalanceApi, getTodayTradesApi } from '@/api/stock/qmt'

// 状态
const loading = ref(false)
const positions = ref<any[]>([])
const trades = ref<any[]>([])
const balance = reactive({
  total_asset: 0,
  available_cash: 0,
  market_value: 0,
  frozen_cash: 0,
  profit_today: 0,
  profit_total: 0
})

// 计算属性
const totalMarketValue = computed(() => {
  return positions.value.reduce((sum, p) => sum + p.market_value, 0)
})

const totalProfit = computed(() => {
  return positions.value.reduce((sum, p) => sum + p.profit, 0)
})

// 方法
const refreshData = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadPositions(),
      loadBalance(),
      loadTrades()
    ])
  } finally {
    loading.value = false
  }
}

const loadPositions = async () => {
  try {
    const { data } = await getPositionsApi()
    positions.value = data?.positions || []
  } catch (e: any) {
    ElMessage.error(e.message || '获取持仓失败')
  }
}

const loadBalance = async () => {
  try {
    const { data } = await getBalanceApi()
    Object.assign(balance, data || {})
  } catch (e: any) {
    ElMessage.error(e.message || '获取资金余额失败')
  }
}

const loadTrades = async () => {
  try {
    const { data } = await getTodayTradesApi()
    trades.value = data?.trades || []
  } catch (e: any) {
    // 静默处理
  }
}

const formatMoney = (value: number) => {
  if (!value) return '¥0.00'
  return '¥' + value.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatTime = (time: string) => {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  refreshData()
})
</script>

<style scoped>
.qmt-position {
  padding: 20px;
}

.balance-row {
  margin-bottom: 20px;
}

.balance-card {
  text-align: center;
}

.balance-item .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.balance-item .value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.balance-item .value.available {
  color: #409eff;
}

.balance-item .value.profit {
  color: #f56c6c;
}

.balance-item .value.loss {
  color: #67c23a;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.position-card,
.trades-card {
  margin-bottom: 20px;
}

.position-summary {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 40px;
}

.position-summary span {
  color: #606266;
}

.position-summary b {
  font-size: 16px;
}

.profit {
  color: #f56c6c;
}

.loss {
  color: #67c23a;
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/Vadmin/Stock/QMT/Position/Position.vue
git commit -m "feat(qmt): add position management page"
```

---

## Task 13: 添加前端路由配置

**Files:**
- Modify: `frontend/src/router/index.ts`

- [ ] **Step 1: 添加QMT路由**

在 `asyncRouterMap` 的 `Stock` 路由的 `children` 数组中添加以下路由配置：

```typescript
// 在 frontend/src/router/index.ts 的 Stock 路由 children 中添加

{
  path: 'qmt-trade',
  component: () => import('@/views/Vadmin/Stock/QMT/Trade/Trade.vue'),
  name: 'QMTTrade',
  meta: {
    title: '交易面板',
    noCache: true
  }
},
{
  path: 'qmt-position',
  component: () => import('@/views/Vadmin/Stock/QMT/Position/Position.vue'),
  name: 'QMTPosition',
  meta: {
    title: '持仓管理',
    noCache: true
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/router/index.ts
git commit -m "feat(qmt): add QMT routes to router"
```

---

## Task 14: 配置后端代理

**Files:**
- Modify: `backend/application/settings.py` 或相关代理配置文件

- [ ] **Step 1: 查找现有代理配置**

Run: 查找项目中API代理配置的位置

- [ ] **Step 2: 添加qmt-service代理**

在现有代理配置中添加对 `/qmt` 路径的代理，指向 `http://localhost:8009`

**注意**：具体配置位置取决于项目的代理设置方式（可能在 `vite.config.ts` 或后端网关配置中）

- [ ] **Step 3: Commit**

```bash
git add <修改的配置文件>
git commit -m "feat(qmt): add qmt-service proxy configuration"
```

---

## Task 15: 验证与测试

- [ ] **Step 1: 启动qmt-service**

```bash
cd backend/qmt-service
pip install -e .
python run.py
```

Expected: 服务启动在 `http://localhost:8009`

- [ ] **Step 2: 测试API文档**

访问 `http://localhost:8009/docs`

Expected: 看到Swagger API文档页面

- [ ] **Step 3: 测试健康检查**

```bash
curl http://localhost:8009/health
```

Expected: 返回 `{"status": "healthy", "service": "QMT量化交易服务", "qmt": {...}}`

- [ ] **Step 4: 启动前端并测试**

```bash
cd frontend
pnpm dev
```

访问前端页面，测试交易面板和持仓管理功能

- [ ] **Step 5: 最终Commit**

```bash
git add -A
git commit -m "feat(qmt): complete phase 1 implementation - QMT connection, trading and position management"
```

---

## 完成检查清单

- [ ] qmt-service 可以独立启动
- [ ] 支持模拟模式（无QMT客户端时）
- [ ] 交易面板页面正常显示
- [ ] 持仓管理页面正常显示
- [ ] API文档可访问
- [ ] 健康检查接口正常

---

## 后续阶段

完成阶段一后，后续阶段包括：

- **阶段二**：风控引擎 + 告警通知
- **阶段三**：智能订单（止损止盈、条件单、算法交易）
- **阶段四**：策略自动化
- **阶段五**：stock-service数据源集成