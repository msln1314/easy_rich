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