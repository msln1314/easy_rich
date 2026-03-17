# akshare-proxy-patch 补丁工具增强计划

## TL;DR

> **快速摘要**: 完善 akshare 代理补丁工具，支持从外部授权服务获取代理配置，支持完整自定义 URL。
> 
> **交付物**:
> - 修改 `install_patch` 函数支持完整 URL
> - 新增 `install_patch_from_url` 函数从指定 URL 获取配置
> - 完善授权配置缓存机制
> - 更新 main.py 使用新的补丁安装方式

**预计工作量**: Quick（约30分钟）
**并行执行**: NO - 顺序实现
**关键路径**: 修改补丁文件 → 更新 main.py

---

## Context

### 原始需求

用户希望 akshare_proxy_patch 工具支持：
1. 使用外部代理池
2. 使用别人提供的接口获取代理配置

### 授权服务信息

**授权 URL**: `http://101.201.173.125:47001/api/akshare-auth?token=&version=0.2.13`

**返回数据示例**:
```json
{
  "proxy": "http://helloyie:7B333A2001041ED2E130BAEA2EC9CF6B@36.111.166.221:45001",
  "nid18": "0b6b01ec6206d93c0f1ea184e711daaa",
  "nid18_create_time": "1769821785641",
  "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
}
```

### 现有代码问题

1. `install_patch(auth_ip, auth_token)` 函数 URL 格式硬编码：
   ```python
   auth_url = f"http://{auth_ip}:47001/api/akshare-auth"
   ```
   无法支持完整的自定义 URL

2. 没有支持版本号参数

3. 没有默认使用公共授权服务的能力

---

## Work Objectives

### 核心目标

完善 akshare_proxy_patch 工具，支持灵活配置代理获取方式。

### 具体交付物

- [x] `install_patch` 函数支持完整 URL 参数
- [x] 新增 `install_patch_from_url` 函数
- [x] 新增 `install_patch_default` 使用默认公共授权服务
- [x] 更新 `get_auth_config_with_cache` 支持完整 URL 和版本参数
- [x] 更新 main.py 使用新的补丁安装方式

### Definition of Done

- [x] 可以通过完整 URL 调用授权服务
- [x] 可以使用默认公共授权服务一键安装补丁
- [x] 原有功能保持兼容

### Must Have

- 支持完整自定义授权 URL
- 支持版本号参数
- 支持默认公共授权服务

### Must NOT Have

- 不破坏现有 API 兼容性
- 不删除现有函数

---

## Verification Strategy

### 测试策略

- **单元测试**: 使用 mock 测试各函数
- **集成测试**: 实际调用授权服务验证返回数据
- **手动验证**: 启动 stock-service 验证补丁生效

### QA Scenarios

每个 TODO 都包含具体的 QA 场景。

---

## Execution Strategy

### 顺序执行

```
Step 1: 修改 akshare_proxy_patch.py（核心功能）
    ├── 1.1 更新 get_auth_config_with_cache 支持 version 参数
    ├── 1.2 修改 install_patch 支持 auth_url 参数
    ├── 1.3 新增 install_patch_from_url 函数
    └── 1.4 新增 install_patch_default 函数

Step 2: 更新 main.py（集成使用）
    └── 2.1 使用新的补丁安装方式
```

---

## TODOs

- [x] 1. 更新 get_auth_config_with_cache 函数

  **What to do**:
  - 添加 `version` 参数支持
  - 支持完整 URL（不再拆分 IP 和端口）
  - 请求参数包含 version
  
  **文件**: `backend/stock-service/app/utils/akshare_proxy_patch.py`
  
  **修改内容**:
  ```python
  def get_auth_config_with_cache(
      auth_url: str, 
      auth_token: str = "", 
      version: str = __version__,
      ttl: int = 20
  ) -> Optional[dict]:
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 2
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] 函数签名包含 version 参数
  - [ ] 请求时传递 version 参数
  - [ ] 支持完整 URL

  **QA Scenarios**:
  ```
  Scenario: 测试授权配置获取
    Tool: Bash (curl)
    Steps:
      1. curl "http://101.201.173.125:47001/api/akshare-auth?token=&version=0.2.13"
      2. 验证返回 JSON 包含 proxy, nid18, ua 字段
    Expected Result: 返回有效配置
    Evidence: .sisyphus/evidence/task-1-auth-config.txt
  ```

---

- [x] 2. 修改 install_patch 函数支持完整 URL

  **What to do**:
  - 修改参数：`auth_url` 替代 `auth_ip`
  - 保持向后兼容（如果传入 IP，自动拼接 URL）
  - 添加 `version` 参数
  
  **文件**: `backend/stock-service/app/utils/akshare_proxy_patch.py`

  **修改内容**:
  ```python
  def install_patch(
      auth_url: str = DEFAULT_AUTH_URL,
      auth_token: str = "",
      version: str = __version__,
      retry: int = 30,
      timeout: int = 30,
      min_interval: float = 0.5
  ):
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 3
  - **Blocked By**: Task 1

  **Acceptance Criteria**:
  - [ ] 支持完整 URL 参数
  - [ ] 支持版本号参数
  - [ ] 原有调用方式仍可用（向后兼容）

---

- [x] 3. 新增便捷函数

  **What to do**:
  - 新增 `install_patch_default()` - 使用默认公共授权服务
  - 新增 `install_patch_from_url(url, token, version)` - 从指定 URL 获取配置
  
  **文件**: `backend/stock-service/app/utils/akshare_proxy_patch.py`

  **新增代码**:
  ```python
  def install_patch_default(
      auth_token: str = "",
      version: str = __version__,
      retry: int = 30,
      timeout: int = 30,
      min_interval: float = 0.5
  ):
      """使用默认公共授权服务安装补丁"""
      return install_patch(DEFAULT_AUTH_URL, auth_token, version, retry, timeout, min_interval)

  def install_patch_from_url(
      auth_url: str,
      auth_token: str = "",
      version: str = __version__,
      retry: int = 30,
      timeout: int = 30,
      min_interval: float = 0.5
  ):
      """从指定 URL 获取授权配置并安装补丁"""
      return install_patch(auth_url, auth_token, version, retry, timeout, min_interval)
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 4
  - **Blocked By**: Task 2

  **Acceptance Criteria**:
  - [ ] `install_patch_default()` 可用
  - [ ] `install_patch_from_url()` 可用
  - [ ] 添加默认常量 `DEFAULT_AUTH_URL`

---

- [x] 4. 更新 main.py 使用新补丁安装方式

  **What to do**:
  - 更新补丁安装代码，使用新的便捷函数
  - 支持通过环境变量配置授权服务
  
  **文件**: `backend/stock-service/app/main.py`

  **修改内容**:
  ```python
  # 加载 AKShare 代理补丁
  try:
      from app.utils.akshare_proxy_patch import install_patch_default
      
      # 从环境变量获取配置，或使用默认值
      auth_token = os.getenv("AKSHARE_AUTH_TOKEN", "")
      version = os.getenv("AKSHARE_VERSION", "0.2.13")
      
      install_patch_default(auth_token=auth_token, version=version, timeout=60)
      print("[Stock Service] AKShare 代理补丁已加载")
  except Exception as e:
      print(f"[Stock Service] AKShare 代理补丁加载失败: {e}")
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 5
  - **Blocked By**: Task 3

  **Acceptance Criteria**:
  - [ ] 使用 `install_patch_default` 安装补丁
  - [ ] 支持环境变量配置
  - [ ] 启动时打印补丁加载状态

  **QA Scenarios**:
  ```
  Scenario: 测试补丁安装
    Tool: Bash
    Steps:
      1. cd backend/stock-service
      2. uv run python -c "from app.utils.akshare_proxy_patch import install_patch_default; install_patch_default()"
      3. 验证输出包含 "[akshare补丁] 已安装"
    Expected Result: 补丁安装成功
    Evidence: .sisyphus/evidence/task-4-patch-install.txt
  ```

---

- [x] 5. 更新使用示例文档

  **What to do**:
  - 更新文件末尾的使用示例
  - 添加新的使用方式说明
  
  **文件**: `backend/stock-service/app/utils/akshare_proxy_patch.py`

  **修改内容**:
  ```python
  # -----------------------------------------------------------------------
  # 使用示例
  #
  # 【方式1：使用默认公共授权服务（推荐）】
  # from app.utils.akshare_proxy_patch import install_patch_default
  # install_patch_default(timeout=60)
  #
  # 【方式2：使用自定义授权服务】
  # from app.utils.akshare_proxy_patch import install_patch_from_url
  # install_patch_from_url(
  #     auth_url="http://your-server/api/akshare-auth",
  #     auth_token="your_token",
  #     version="0.2.13",
  #     timeout=60
  # )
  #
  # 【方式3：使用外部代理池】
  # from app.utils.akshare_proxy_patch import install_patch_with_pool
  # install_patch_with_pool(
  #     ua="Mozilla/5.0 ...",
  #     nid18="xxx",
  #     nid18_create_time="xxx",
  #     pool_url="http://127.0.0.1:5010",
  #     timeout=60
  # )
  # -----------------------------------------------------------------------
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: None
  - **Blocked By**: Task 4

---

## Final Verification Wave

- [x] F1. 代码质量检查
  运行 `python -m py_compile` 检查语法，验证导入正常。

- [x] F2. 功能验证
  启动 stock-service，验证补丁正常加载，验证 AKShare 接口调用正常。

---

## Commit Strategy

- **Commit**: YES
- **Message**: `feat(stock-service): enhance akshare proxy patch with flexible auth URL support`
- **Files**: 
  - `backend/stock-service/app/utils/akshare_proxy_patch.py`
  - `backend/stock-service/app/main.py`

---

## Success Criteria

### Verification Commands

```bash
# 测试授权服务可用
curl "http://101.201.173.125:47001/api/akshare-auth?token=&version=0.2.13"

# 测试补丁安装
cd backend/stock-service
uv run python -c "from app.utils.akshare_proxy_patch import install_patch_default; install_patch_default(timeout=60)"

# 启动服务验证
uv run python run.py
```

### Final Checklist

- [x] 所有 Must Have 功能实现
- [x] 原有 API 保持兼容
- [x] 补丁安装正常
- [x] 授权服务调用正常