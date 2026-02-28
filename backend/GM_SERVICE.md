# GM 服务集成说明

## 概述

`stock-akshare` 项目现已集成 GM（掘金量化）服务作为 akshare 的备用数据源，实现了自动降级机制，提高数据获取的可靠性。

## 架构设计

### 数据源优先级

```
1. AKShare（主要数据源）
   ↓ (失败时自动降级)
2. GM（掘金量化，备用数据源）
```

### 核心组件

#### 1. GMService (`app/services/gm_service.py`)

提供与掘金量化平台兼容的数据接口，包括：

- **概念板块接口**
  - `get_concept_boards()`: 获取概念板块列表
  - `get_concept_board_constituents()`: 获取概念板块成份股

- **行业板块接口**
  - `get_industry_boards()`: 获取行业板块列表
  - `get_industry_board_constituents()`: 获取行业板块成份股

#### 2. SectorService 改造 (`app/services/sector_service.py`)

所有数据获取方法都支持自动降级：

```python
async def get_concept_boards(self, fallback_to_gm: bool = True) -> List[ConceptBoard]:
    """
    获取概念板块列表
    优先使用 AKShare，失败时自动降级到 GM
    """
    # 尝试使用 AKShare 获取数据
    try:
        return await self._get_concept_boards_from_akshare()
    except Exception as e:
        # AKShare 失败，降级到 GM
        if fallback_to_gm and gm_service.is_available():
            return await gm_service.get_concept_boards()
        # 两个数据源都失败，抛出异常
        raise ValueError(f"无法获取概念板块数据: {str(e)}")
```

## 使用方法

### 基础使用（自动降级）

默认情况下，所有方法都启用自动降级：

```python
from app.services.sector_service import sector_service

# 自动降级：AKShare 失败时使用 GM
boards = await sector_service.get_concept_boards()
constituents = await sector_service.get_concept_board_constituents("融资融券")
industry_boards = await sector_service.get_industry_boards()
```

### 禁用自动降级

如果只想使用 AKShare，不使用 GM：

```python
# 禁用降级：仅使用 AKShare
boards = await sector_service.get_concept_boards(fallback_to_gm=False)
```

### 检查 GM 服务状态

```python
from app.services.gm_service import gm_service

# 检查 GM 服务是否可用
if gm_service.is_available():
    print("GM 服务可用")
else:
    print("GM 服务不可用")
```

## API 接口

所有现有的 API 接口保持不变，无需修改前端代码：

```
GET /api/sector/concept              # 获取概念板块列表（支持自动降级）
GET /api/sector/industry             # 获取行业板块列表（支持自动降级）
GET /api/sector/concept/by-symbol/constituents?symbol=融资融券  # 获取成份股
```

## 安装 GM SDK

如果需要启用 GM 服务，安装掘金量化 SDK：

```bash
cd stock-akshare
poetry add gm  # 或 pip install gm
```

## 配置说明

### GM SDK 配置

GM SDK 需要配置 Token 和服务器地址，通常在项目启动时设置：

```python
# 在 run.py 或 main.py 中
from gm.api import gm

# 设置 Token
gm.set_token("your_gm_token")

# 连接到掘金服务器（根据环境选择）
# 模拟环境
gm.init(token="your_gm_token", mode="模拟")
# 实盘环境
gm.init(token="your_gm_token", mode="实盘")
```

### 环境变量配置

建议使用环境变量管理配置：

```env
# GM 服务配置
GM_TOKEN=your_gm_token
GM_MODE=simulate  # simulate 或 real
```

## 日志输出

系统会记录详细的降级日志：

```
[INFO] 获取概念板块列表（优先 AKShare，失败时降级到 GM）
[DEBUG] 使用 AKShare 获取概念板块数据
[WARNING] AKShare 获取概念板块失败: 网络超时
[INFO] 降级使用 GM 获取概念板块
[INFO] GM 获取到 125 个概念板块
```

## 故障排查

### GM 服务不可用

如果看到以下日志：
```
[WARNING] 掘金量化 SDK 未安装，GM 服务将不可用
```

解决方法：
```bash
pip install gm
```

### GM Token 错误

如果看到以下日志：
```
[ERROR] 掘金量化 SDK 初始化失败: Token 无效
```

解决方法：
1. 检查 Token 是否正确
2. 确认 Token 是否过期
3. 联系掘金客服获取新的 Token

### 两个数据源都失败

如果看到以下日志：
```
[ERROR] 无法获取概念板块数据，AKShare 失败: xxx
[ERROR] GM 获取概念板块也失败: xxx
```

解决方法：
1. 检查网络连接
2. 检查 AKShare 服务状态
3. 检查 GM 服务配置
4. 查看详细错误日志

## 扩展新的数据源

如果需要添加其他数据源（如 QMT），可以按照以下步骤：

1. 创建新的服务类 `app/services/qmt_service.py`
2. 实现与 `GMService` 相同的接口
3. 在 `SectorService` 中添加降级逻辑

示例：

```python
# app/services/qmt_service.py
class QMTService:
    async def get_concept_boards(self) -> List[ConceptBoard]:
        # 实现 QMT 数据获取逻辑
        pass

# app/services/sector_service.py
from app.services.qmt_service import qmt_service

async def get_concept_boards(self) -> List[ConceptBoard]:
    try:
        return await self._get_concept_boards_from_akshare()
    except Exception as e:
        if fallback_to_gm and gm_service.is_available():
            return await gm_service.get_concept_boards()
        # 添加第三级降级
        if fallback_to_qmt and qmt_service.is_available():
            return await qmt_service.get_concept_boards()
        raise ValueError(f"无法获取概念板块数据")
```

## 性能优化建议

1. **缓存策略**：已启用缓存，避免重复请求
2. **并发控制**：限制并发请求数量，避免触发 API 限制
3. **超时设置**：为每个数据源设置合理的超时时间
4. **监控告警**：监控降级频率，及时发现问题

## 总结

GM 服务的集成提供了以下优势：

✅ **提高可靠性**：自动降级，确保数据获取不中断
✅ **统一接口**：与 akshare 接口完全兼容，无需修改前端代码
✅ **灵活配置**：支持启用/禁用降级，适应不同场景
✅ **易于扩展**：支持添加更多备用数据源

通过 GM 服务的集成，`stock-akshare` 项目的数据获取能力得到显著提升！
