#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.1
# @Create Time    : 2026/3/1
# @File           : akshare_proxy_patch.py
# @IDE            : PyCharm
# @desc           : akshare 代理补丁（支持云端授权、本地配置、代理池等多种模式）

import time
import random
import threading
import requests
from typing import Optional, Dict

try:
    from app.services.proxy_pool_manager import get_proxy_pool_manager
except ImportError:
    get_proxy_pool_manager = None

__version__ = "0.2.13"

DEFAULT_AUTH_URL = "http://101.201.173.125:47001/api/akshare-auth"
REDIS_DISABLED_KEY = "akshare:patch:disabled"
REDIS_DISABLED_TTL = 86400  # 24 hours

_original_request = requests.Session.request
_auth_session = requests.Session()
_redis_client = None


def _get_redis():
    """Get Redis client lazily"""
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    try:
        import redis
        from app.core.config import settings

        if settings.REDIS_ENABLED:
            _redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
            )
            return _redis_client
    except Exception as e:
        print(f"[akshare补丁] Redis连接失败: {e}")
    return None


def is_patch_disabled() -> bool:
    """Check if patch is disabled in Redis (quota exhausted)"""
    r = _get_redis()
    if not r:
        return False
    try:
        return r.get(REDIS_DISABLED_KEY) == "true"
    except Exception:
        return False


def set_patch_disabled(disabled: bool = True):
    """Set patch disabled status in Redis with 24h TTL"""
    r = _get_redis()
    if not r:
        return
    try:
        if disabled:
            r.setex(REDIS_DISABLED_KEY, REDIS_DISABLED_TTL, "true")
            print(f"[akshare补丁] 已禁用云端授权 (24小时)")
        else:
            r.delete(REDIS_DISABLED_KEY)
    except Exception as e:
        print(f"[akshare补丁] Redis写入失败: {e}")


def clear_patch_disabled():
    """Clear patch disabled status"""
    set_patch_disabled(False)


def test_proxy(
    proxy: Optional[str] = None,
    test_url: str = "http://www.example.com",
    timeout: int = 10,
) -> bool:
    """
    测试代理是否可用（通过代理访问测试网站）

    Args:
        proxy: 代理地址，格式: http://ip:port
        test_url: 测试目标网站，默认 http://example.com
        timeout: 请求超时时间

    Returns:
        bool: 代理是否可用
    """
    proxies = {"http": proxy, "https": proxy} if proxy else None
    proxy_desc = proxy or "直连"

    try:
        print(f"[代理测试] 正在通过 {proxy_desc} 访问 {test_url} ...")
        resp = requests.get(
            test_url,
            proxies=proxies,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        if resp.status_code == 200:
            print(
                f"[代理测试] ✓ 成功! status={resp.status_code}, 长度={len(resp.text)}"
            )
            return True
        else:
            print(f"[代理测试] ✗ 失败! status={resp.status_code}")
            return False
    except Exception as e:
        print(f"[代理测试] ✗ 异常: {e}")
        return False


def fetch_eastmoney_cookie(
    proxy: Optional[str] = None, timeout: int = 10
) -> Dict[str, str]:
    """
    访问东财首页获取 Cookie（nid18 等关键字段）

    Args:
        proxy: 可选代理地址，格式: http://ip:port
        timeout: 请求超时时间

    Returns:
        dict: 包含 ua, nid18, nid18_create_time 等字段
    """
    url = "https://www.eastmoney.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    proxies = {"http": proxy, "https": proxy} if proxy else None

    try:
        session = requests.Session()
        resp = session.get(
            url, headers=headers, proxies=proxies, timeout=timeout, allow_redirects=True
        )
        resp.raise_for_status()

        # 从响应 Cookie 中提取关键字段
        cookies = session.cookies.get_dict()
        nid18 = cookies.get("nid18", "")
        nid18_create_time = cookies.get(
            "nid18_create_time", str(int(time.time() * 1000))
        )

        if not nid18:
            # 尝试从响应头 Set-Cookie 中解析
            set_cookie = resp.headers.get("Set-Cookie", "")
            for part in set_cookie.split("; "):
                if "nid18=" in part and not part.startswith("nid18_create_time"):
                    nid18 = part.split("=")[1] if "=" in part else ""
                if "nid18_create_time=" in part:
                    nid18_create_time = (
                        part.split("=")[1] if "=" in part else nid18_create_time
                    )

        result = {
            "ua": headers["User-Agent"],
            "nid18": nid18 or "090cd85fdab3bead76a0997310db6ffc",  # fallback
            "nid18_create_time": nid18_create_time or str(int(time.time() * 1000)),
            "proxy": proxy or "",
            "all_cookies": cookies,
        }
        print(
            f"[Cookie获取] 成功: nid18={result['nid18'][:16]}..., proxy={proxy or '直连'}"
        )
        return result

    except Exception as e:
        print(f"[Cookie获取] 失败: {e}，使用默认Cookie")
        return {
            "ua": headers["User-Agent"],
            "nid18": "090cd85fdab3bead76a0997310db6ffc",
            "nid18_create_time": str(int(time.time() * 1000)),
            "proxy": proxy or "",
            "all_cookies": {},
        }


# 东财接口域名列表
EASTMONEY_DOMAINS = [
    "fund.eastmoney.com",
    "push2.eastmoney.com",
    "push2his.eastmoney.com",
    "push2ex.eastmoney.com",
    "push2delay.eastmoney.com",
    "quote.eastmoney.com",
    "data.eastmoney.com",
    "datacenter-web.eastmoney.com",
    "emweb.securities.eastmoney.com",
]


class AuthCache:
    """授权缓存类"""

    def __init__(self):
        self.data = None
        self.expire_at = 0
        self.lock = threading.Lock()
        self.ttl = 20


_cache = AuthCache()


class RateLimiter:
    """令牌桶限流器，控制请求频率"""

    def __init__(self, min_interval: float = 0.5):
        """
        Args:
            min_interval: 两次请求之间最小间隔时间（秒），默认 0.5 秒
        """
        self.min_interval = min_interval
        self.last_request_time = 0.0
        self.lock = threading.Lock()

    def acquire(self):
        """阻塞等待直到可以发送下一个请求"""
        with self.lock:
            now = time.time()
            elapsed = now - self.last_request_time
            wait = self.min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            self.last_request_time = time.time()

    def set_interval(self, min_interval: float):
        """动态调整限流间隔"""
        self.min_interval = min_interval


_rate_limiter = RateLimiter(min_interval=0.5)


class ProxyPool:
    """
    免费代理池客户端
    兼容 proxy_pool 项目标准接口: https://github.com/AlexLiue/proxy_pool
    API:
        GET  /get/          -> 随机获取一个可用代理
        GET  /delete/?proxy=ip:port -> 删除失效代理
        GET  /all/          -> 获取全部代理（可选）
    """

    def __init__(self, pool_url: str = "http://127.0.0.1:5010"):
        """
        Args:
            pool_url: 代理池服务地址，默认 http://127.0.0.1:5010
        """
        self.pool_url = pool_url.rstrip("/")
        self._lock = threading.Lock()
        self._current_proxy: Optional[str] = None
        self._fail_count = 0
        self._max_fail = 3  # 单个代理最多失败次数后换代理

    def get(self) -> Optional[str]:
        """从代理池获取一个代理，返回格式: http://ip:port"""
        try:
            resp = _auth_session.get(f"{self.pool_url}/get/", timeout=5)
            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                data = resp.json()
                # 检测无代理情况: {"code":0,"src":"no proxy"}
                if data.get("code") == 0 and "no proxy" in str(data.get("src", "")):
                    print(f"[代理池] 无可用代理")
                    return None
                proxy = data.get("proxy") or data.get("http") or data.get("https")
            else:
                proxy = resp.text.strip()

            if proxy and proxy != "no proxy" and proxy != "null" and len(proxy) > 5:
                if not proxy.startswith("http"):
                    proxy = f"http://{proxy}"
                return proxy
        except Exception as e:
            print(f"[代理池] 获取代理失败: {e}")
        return None

    def delete(self, proxy: str):
        """删除失效代理"""
        raw = proxy.replace("http://", "").replace("https://", "")
        try:
            _auth_session.get(f"{self.pool_url}/delete/?proxy={raw}", timeout=3)
            print(f"[代理池] 已删除失效代理: {raw}")
        except Exception:
            pass

    def next_proxy(self, mark_failed: bool = False) -> Optional[str]:
        """
        获取下一个可用代理
        Args:
            mark_failed: 是否将当前代理标记为失败（失败次数超限则删除并换代理）
        """
        with self._lock:
            if mark_failed and self._current_proxy:
                self._fail_count += 1
                if self._fail_count >= self._max_fail:
                    self.delete(self._current_proxy)
                    self._current_proxy = None
                    self._fail_count = 0

            if not self._current_proxy:
                self._current_proxy = self.get()
                self._fail_count = 0

            return self._current_proxy


def get_auth_config_with_cache(
    auth_url: str, auth_token: str = "", version: str = __version__, ttl: int = 20
) -> Optional[dict]:
    """
    从远程授权服务器获取授权配置（带缓存）

    Args:
        auth_url: 授权接口完整 URL
        auth_token: 认证令牌（可选，部分公开服务不需要）
        version: 版本号
        ttl: 缓存时间（分钟）

    Returns:
        dict: 授权配置，包含 ua, nid18, nid18_create_time, proxy 等字段
    """
    now = time.time()

    if _cache.data and now < _cache.expire_at:
        return _cache.data

    with _cache.lock:
        if _cache.data and now < _cache.expire_at:
            return _cache.data

        try:
            params = {"token": auth_token, "version": version}
            resp = _auth_session.get(auth_url, params=params, timeout=10)

            # 检查响应状态和内容
            if resp.status_code != 200:
                print(f"[akshare补丁] 授权接口返回非200: status={resp.status_code}")
                return _cache.data

            text = resp.text.strip()
            if not text:
                print(f"[akshare补丁] 授权接口返回空响应")
                return _cache.data

            # 尝试解析 JSON
            try:
                data = resp.json()
            except Exception as json_err:
                print(f"[akshare补丁] 授权接口返回非JSON: {text[:200]}")
                return _cache.data

            if data.get("ua"):
                _cache.data = data
                _cache.expire_at = now + ttl * 60
                clear_patch_disabled()
                print(
                    f"[akshare补丁] 授权成功: proxy={data.get('proxy', '直连')[:50]}..."
                )
                return data

            error_msg = data.get("error_msg", "")
            print(f"[akshare补丁] 授权失败: {error_msg}")

            # 检测积分用完或TOKEN无效，设置禁用标记
            if (
                "积分" in error_msg
                or "用完" in error_msg
                or "TOKEN 无效" in error_msg
                or "积分不足" in error_msg
            ):
                set_patch_disabled(True)
                print(f"[akshare补丁] 检测到授权问题，禁用云端授权24小时")

        except Exception as e:
            print(f"[akshare补丁] 请求授权接口异常: {e}")

        return _cache.data


def _build_patched_request(
    get_auth_res_fn, retry: int, timeout: int = 30, min_interval: float = 0.5
):
    """
    构建 patched_request 方法的工厂函数

    Args:
        get_auth_res_fn: 获取 auth_res 的函数，签名为 () -> Optional[dict]
        retry: 重试次数
        timeout: 请求超时时间（秒），默认 30
        min_interval: 两次请求最小间隔（秒），默认 0.5，设为 0 则不限流
    """
    _rate_limiter.set_interval(min_interval)

    def patched_request(self, method, url, **kwargs):
        """修补后的请求方法"""
        # 检查是否为目标域名（东方财富接口）
        is_target = any(d in (url or "") for d in EASTMONEY_DOMAINS)

        # 如果不是目标域名，直接使用原始请求
        if not is_target:
            return _original_request(self, method, url, **kwargs)

        # 限流：等待满足最小间隔 + 随机抖动（防止分页请求被识别为爬虫）
        if min_interval > 0:
            _rate_limiter.acquire()
            jitter = random.uniform(0, min_interval * 0.5)
            if jitter > 0:
                time.sleep(jitter)

        print(f"[akshare补丁] 拦截请求: {method} {url}")

        # 重试逻辑
        for attempt in range(retry):
            auth_res = get_auth_res_fn()
            if not auth_res:
                time.sleep(0.05)
                continue

            # 处理 Headers：复制一份避免污染原始 kwargs
            headers = dict(kwargs.get("headers") or {})
            headers["User-Agent"] = auth_res["ua"]
            headers["Cookie"] = (
                f"nid18={auth_res['nid18']}; nid18_create_time={auth_res['nid18_create_time']}"
            )
            kwargs["headers"] = headers
            # proxy 为空时不设置代理，直接使用本机网络
            if auth_res.get("proxy"):
                kwargs["proxies"] = {
                    "http": auth_res["proxy"],
                    "https": auth_res["proxy"],
                }
            kwargs["timeout"] = timeout

            try:
                resp = _original_request(self, method, url, **kwargs)
                if resp.ok and resp.content:
                    # 检测是否被封禁（东财封禁时返回 200 但携带特定错误码）
                    try:
                        data = resp.json()
                        rc = data.get("rc", 0) if isinstance(data, dict) else 0
                        if rc in (10002, 10003, -100):
                            wait = 1.0 + random.uniform(0, 0.5)
                            print(
                                f"[akshare补丁] 检测到封禁 rc={rc}，退避 {wait:.1f}s 后重试 {attempt + 1}/{retry}"
                            )
                            time.sleep(wait)
                            with _cache.lock:
                                _cache.expire_at = 0
                            continue
                    except Exception:
                        pass
                    return resp

                # 响应异常，随机退避后重试
                wait = 0.1 + random.uniform(0, 0.3)
                print(
                    f"[akshare补丁] 响应异常 status={resp.status_code}，退避 {wait:.1f}s 后重试 {attempt + 1}/{retry}"
                )
                with _cache.lock:
                    _cache.expire_at = 0
                time.sleep(wait)
            except Exception as e:
                wait = 0.1 + random.uniform(0, 0.3)
                print(
                    f"[akshare补丁] 请求异常，退避 {wait:.1f}s 后重试 {attempt + 1}/{retry}: {e}"
                )
                with _cache.lock:
                    _cache.expire_at = 0
                time.sleep(wait)

        # 全部重试失败，使用原始请求兜底
        print("[akshare补丁] 全部重试失败，使用原始请求兜底")
        return _original_request(self, method, url, **kwargs)

    return patched_request


def install_patch(
    auth_url: str = DEFAULT_AUTH_URL,
    auth_token: str = "",
    version: str = __version__,
    retry: int = 3,
    timeout: int = 30,
    min_interval: float = 0.5,
):
    """
    安装 akshare 代理补丁（云端模式，通过远程授权服务器获取代理配置）

    Args:
        auth_url: 授权接口完整 URL，默认为公共授权服务
        auth_token: 认证令牌（可选，部分公开服务不需要）
        version: 版本号
        retry: 重试次数，默认为 30
        timeout: 请求超时时间（秒）
        min_interval: 两次请求最小间隔（秒）
    """

    def get_auth_res():
        return get_auth_config_with_cache(auth_url, auth_token, version)

    requests.Session.request = _build_patched_request(
        get_auth_res, retry, timeout, min_interval
    )
    print(f"[akshare补丁] 已安装（云端模式），授权服务: {auth_url}")


def install_patch_default(
    auth_token: str = "",
    version: str = __version__,
    retry: int = 3,
    timeout: int = 30,
    min_interval: float = 0.5,
):
    """
    使用默认公共授权服务安装补丁

    Args:
        auth_token: 认证令牌（可选）
        version: 版本号
        retry: 重试次数
        timeout: 请求超时时间（秒）
        min_interval: 两次请求最小间隔（秒）
    """
    return install_patch(
        DEFAULT_AUTH_URL, auth_token, version, retry, timeout, min_interval
    )


def install_patch_from_url(
    auth_url: str,
    auth_token: str = "",
    version: str = __version__,
    retry: int = 3,
    timeout: int = 30,
    min_interval: float = 0.5,
):
    """
    从指定 URL 获取授权配置并安装补丁

    Args:
        auth_url: 授权接口完整 URL
        auth_token: 认证令牌（可选）
        version: 版本号
        retry: 重试次数
        timeout: 请求超时时间（秒）
        min_interval: 两次请求最小间隔（秒）
    """
    return install_patch(auth_url, auth_token, version, retry, timeout, min_interval)


def install_patch_with_redis_pool(
    ua: str = None,
    nid18: str = None,
    nid18_create_time: str = None,
    retry: int = 3,
    timeout: int = 30,
    min_interval: float = 0.2,
):
    """
    Install patch with Redis-backed proxy pool manager.
    Auto-fetches and caches proxies, auto-switches on ban.
    """
    if get_proxy_pool_manager is None:
        print("[akshare补丁] Redis代理池不可用，使用直连模式")
        return install_patch_auto(timeout=timeout, min_interval=min_interval)

    manager = get_proxy_pool_manager()
    status = manager.get_pool_status()

    if status["available"] < status["min_proxies"]:
        print(f"[akshare补丁] 代理池不足({status['available']})，正在获取...")
        manager.refresh_proxies(validate=False)

    if ua is None:
        auth_res = fetch_eastmoney_cookie(timeout=10)
        ua = auth_res["ua"]
        nid18 = auth_res["nid18"]
        nid18_create_time = auth_res["nid18_create_time"]

    _rate_limiter.set_interval(min_interval)

    def patched_request(self, method, url, **kwargs):
        is_target = any(d in (url or "") for d in EASTMONEY_DOMAINS)
        if not is_target:
            return _original_request(self, method, url, **kwargs)

        if min_interval > 0:
            _rate_limiter.acquire()

        for attempt in range(retry):
            proxy = manager.next_proxy(mark_failed=(attempt > 0))

            if not proxy:
                print("[akshare补丁] 无可用代理，直连")
                return _original_request(self, method, url, **kwargs)

            headers = dict(kwargs.get("headers") or {})
            headers["User-Agent"] = ua
            headers["Cookie"] = f"nid18={nid18}; nid18_create_time={nid18_create_time}"
            kwargs["headers"] = headers
            kwargs["proxies"] = {"http": proxy, "https": proxy}
            kwargs["timeout"] = timeout

            try:
                resp = _original_request(self, method, url, **kwargs)
                if resp.ok and resp.content:
                    try:
                        data = resp.json()
                        rc = data.get("rc", 0) if isinstance(data, dict) else 0
                        if rc in (10002, 10003, -100):
                            print(f"[akshare补丁] 封禁 rc={rc}，切换代理")
                            manager.next_proxy(mark_failed=True)
                            continue
                    except Exception:
                        pass
                    return resp
                print(f"[akshare补丁] 响应异常 {resp.status_code}，切换代理")
            except Exception as e:
                print(f"[akshare补丁] 请求异常，切换代理: {str(e)[:50]}")
                manager.next_proxy(mark_failed=True)

        print("[akshare补丁] 重试耗尽，直连")
        return _original_request(self, method, url, **kwargs)

    requests.Session.request = patched_request
    print(
        f"[akshare补丁] 已安装（Redis代理池模式），可用代理: {manager.get_pool_status()['available']}"
    )


def install_patch_local(
    ua: str,
    nid18: str,
    nid18_create_time: str,
    proxy: Optional[str] = None,
    retry: int = 3,
    timeout: int = 30,
    min_interval: float = 0.5,
):
    """
    安装 akshare 代理补丁（本地模式，直接指定认证信息，无需远程授权服务器）

    auth_res 示例（云端返回的格式）:
        {
            'proxy': 'http://user:pass@ip:port',  # 可选，不填则直连
            'nid18': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            'nid18_create_time': '1769821785641',
            'ua': 'Mozilla/5.0 ...'
        }

    Args:
        ua: User-Agent 字符串
        nid18: 东财 nid18 cookie 值
        nid18_create_time: 东财 nid18_create_time cookie 值
        proxy: 代理地址，格式: http://user:pass@ip:port，不填则直连
        retry: 重试次数，默认为 3
        timeout: 请求超时时间（秒），默认 30
        min_interval: 两次请求最小间隔（秒），默认 0.5，设为 0 则不限流
    """
    # 本地静态 auth_res，结构与云端返回一致
    static_auth_res = {
        "proxy": proxy or "",
        "ua": ua,
        "nid18": nid18,
        "nid18_create_time": nid18_create_time,
    }

    def get_auth_res():
        return static_auth_res

    requests.Session.request = _build_patched_request(
        get_auth_res, retry, timeout, min_interval
    )
    if proxy:
        print(
            f"[akshare补丁] 已安装（本地模式），代理: {proxy}，超时: {timeout}s，限流间隔: {min_interval}s"
        )
    else:
        print(
            f"[akshare补丁] 已安装（本地模式），直连（不使用代理），超时: {timeout}s，限流间隔: {min_interval}s"
        )


def install_patch_with_pool(
    ua: str,
    nid18: str,
    nid18_create_time: str,
    pool_url: str = "http://127.0.0.1:5010",
    retry: int = 3,
    timeout: int = 30,
    min_interval: float = 1.0,
):
    """
    安装 akshare 代理补丁（代理池模式，从 proxy_pool 服务动态获取代理）

    兼容 proxy_pool 项目: https://github.com/AlexLiue/proxy_pool
    代理池每次请求失败超过 max_fail 次后自动换代理，失效代理自动从池中删除。

    Args:
        ua: User-Agent 字符串
        nid18: 东财 nid18 cookie 值
        nid18_create_time: 东财 nid18_create_time cookie 值
        pool_url: 代理池服务地址，默认 http://127.0.0.1:5010
        retry: 重试次数，默认 5
        timeout: 请求超时时间（秒），默认 30
        min_interval: 两次请求最小间隔（秒），默认 1.0
    """
    pool = ProxyPool(pool_url=pool_url)

    def get_auth_res():
        proxy = pool.next_proxy()
        return {
            "proxy": proxy or "",
            "ua": ua,
            "nid18": nid18,
            "nid18_create_time": nid18_create_time,
        }

    # 代理池模式下，请求失败时需要通知代理池换代理
    # 重写 _build_patched_request 中的失败回调
    _rate_limiter.set_interval(min_interval)

    def patched_request(self, method, url, **kwargs):
        is_target = any(d in (url or "") for d in EASTMONEY_DOMAINS)
        if not is_target:
            return _original_request(self, method, url, **kwargs)

        if min_interval > 0:
            _rate_limiter.acquire()
            jitter = random.uniform(0, min_interval * 0.5)
            if jitter > 0:
                time.sleep(jitter)

        print(f"[akshare补丁] 拦截请求: {method} {url}")

        for attempt in range(retry):
            proxy = pool.next_proxy()
            auth_res = {
                "proxy": proxy or "",
                "ua": ua,
                "nid18": nid18,
                "nid18_create_time": nid18_create_time,
            }

            headers = dict(kwargs.get("headers") or {})
            headers["User-Agent"] = auth_res["ua"]
            headers["Cookie"] = (
                f"nid18={auth_res['nid18']}; nid18_create_time={auth_res['nid18_create_time']}"
            )
            kwargs["headers"] = headers
            if auth_res.get("proxy"):
                kwargs["proxies"] = {
                    "http": auth_res["proxy"],
                    "https": auth_res["proxy"],
                }
            kwargs["timeout"] = timeout

            try:
                resp = _original_request(self, method, url, **kwargs)
                if resp.ok and resp.content:
                    try:
                        data = resp.json()
                        rc = data.get("rc", 0) if isinstance(data, dict) else 0
                        if rc in (10002, 10003, -100):
                            wait = 1.0 + random.uniform(0, 0.5)
                            print(
                                f"[akshare补丁] 封禁 rc={rc}，换代理并退避 {wait:.1f}s，重试 {attempt + 1}/{retry}"
                            )
                            pool.next_proxy(mark_failed=True)
                            time.sleep(wait)
                            continue
                    except Exception:
                        pass
                    return resp

                wait = 0.1 + random.uniform(0, 0.3)
                print(
                    f"[akshare补丁] 响应异常 status={resp.status_code}，换代理并退避 {wait:.1f}s，重试 {attempt + 1}/{retry}"
                )
                pool.next_proxy(mark_failed=True)
                time.sleep(wait)
            except Exception as e:
                wait = 0.1 + random.uniform(0, 0.3)
                print(
                    f"[akshare补丁] 请求异常，换代理并退避 {wait:.1f}s，重试 {attempt + 1}/{retry}: {e}"
                )
                pool.next_proxy(mark_failed=True)
                time.sleep(wait)

        print("[akshare补丁] 全部重试失败，使用原始请求兜底")
        return _original_request(self, method, url, **kwargs)

    requests.Session.request = patched_request
    print(
        f"[akshare补丁] 已安装（代理池模式），代理池: {pool_url}，超时: {timeout}s，限流间隔: {min_interval}s"
    )


def install_patch_auto(
    proxy: Optional[str] = None,
    pool_url: Optional[str] = None,
    retry: int = 3,
    timeout: int = 30,
    min_interval: float = 0.5,
):
    """
    安装 akshare 代理补丁（自动Cookie模式，访问东财首页获取最新Cookie）

    自动访问 https://www.eastmoney.com/ 获取 nid18、nid18_create_time 等关键Cookie，
    无需手动填写。支持配合代理或代理池使用。

    Args:
        proxy: 可选固定代理地址，格式: http://ip:port
        pool_url: 可选代理池地址（如提供则优先使用代理池），格式: http://ip:port
        retry: 重试次数，默认 3
        timeout: 请求超时时间（秒），默认 30
        min_interval: 两次请求最小间隔（秒），默认 0.5
    """
    # 获取初始Cookie
    initial_proxy = proxy
    if pool_url:
        # 先从代理池获取一个代理来请求Cookie
        temp_pool = ProxyPool(pool_url=pool_url)
        initial_proxy = temp_pool.get()

    auth_res = fetch_eastmoney_cookie(proxy=initial_proxy, timeout=10)

    if pool_url:
        # 代理池模式：动态轮换代理
        pool = ProxyPool(pool_url=pool_url)
        pool._current_proxy = initial_proxy

        def get_auth_res():
            # 每次请求前检查是否需要刷新Cookie（简化处理：固定使用初始Cookie）
            return auth_res

        _rate_limiter.set_interval(min_interval)

        def patched_request(self, method, url, **kwargs):
            is_target = any(d in (url or "") for d in EASTMONEY_DOMAINS)
            if not is_target:
                return _original_request(self, method, url, **kwargs)

            if min_interval > 0:
                _rate_limiter.acquire()
                jitter = random.uniform(0, min_interval * 0.5)
                if jitter > 0:
                    time.sleep(jitter)

            print(f"[akshare补丁] 拦截请求: {method} {url}")

            for attempt in range(retry):
                current_proxy = pool.next_proxy()

                headers = dict(kwargs.get("headers") or {})
                headers["User-Agent"] = auth_res["ua"]
                headers["Cookie"] = (
                    f"nid18={auth_res['nid18']}; nid18_create_time={auth_res['nid18_create_time']}"
                )
                kwargs["headers"] = headers
                if current_proxy:
                    kwargs["proxies"] = {"http": current_proxy, "https": current_proxy}
                kwargs["timeout"] = timeout

                try:
                    resp = _original_request(self, method, url, **kwargs)
                    if resp.ok and resp.content:
                        try:
                            data = resp.json()
                            rc = data.get("rc", 0) if isinstance(data, dict) else 0
                            if rc in (10002, 10003, -100):
                                wait = 1.0 + random.uniform(0, 0.5)
                                print(
                                    f"[akshare补丁] 封禁 rc={rc}，换代理并退避 {wait:.1f}s，重试 {attempt + 1}/{retry}"
                                )
                                pool.next_proxy(mark_failed=True)
                                time.sleep(wait)
                                continue
                        except Exception:
                            pass
                        return resp

                    wait = 0.1 + random.uniform(0, 0.3)
                    print(
                        f"[akshare补丁] 响应异常，换代理并退避 {wait:.1f}s，重试 {attempt + 1}/{retry}"
                    )
                    pool.next_proxy(mark_failed=True)
                    time.sleep(wait)
                except Exception as e:
                    wait = 0.1 + random.uniform(0, 0.3)
                    print(
                        f"[akshare补丁] 请求异常，换代理并退避 {wait:.1f}s，重试 {attempt + 1}/{retry}: {e}"
                    )
                    pool.next_proxy(mark_failed=True)
                    time.sleep(wait)

            print("[akshare补丁] 全部重试失败，使用原始请求兜底")
            return _original_request(self, method, url, **kwargs)

        requests.Session.request = patched_request
        print(
            f"[akshare补丁] 已安装（自动Cookie+代理池模式），代理池: {pool_url}，超时: {timeout}s"
        )

    else:
        # 固定代理或直连模式
        def get_auth_res():
            return auth_res

        requests.Session.request = _build_patched_request(
            get_auth_res, retry, timeout, min_interval
        )
        if proxy:
            print(
                f"[akshare补丁] 已安装（自动Cookie+固定代理模式），代理: {proxy}，超时: {timeout}s"
            )
        else:
            print(f"[akshare补丁] 已安装（自动Cookie+直连模式），超时: {timeout}s")


def uninstall_patch():
    """卸载 akshare 代理补丁，恢复原始请求方法"""
    requests.Session.request = _original_request
    print("[akshare补丁] 已卸载")


def get_patch_status() -> dict:
    """
    获取补丁状态

    Returns:
        dict: 包含补丁状态信息
    """
    return {
        "installed": requests.Session.request != _original_request,
        "cache_data": _cache.data,
        "cache_expire_at": _cache.expire_at,
    }


def clear_cache():
    """清除授权缓存（云端模式下有效）"""
    with _cache.lock:
        _cache.data = None
        _cache.expire_at = 0
    print("[akshare补丁] 授权缓存已清除")


# -----------------------------------------------------------------------
# 使用示例
#
# 【方式1：使用默认公共授权服务（推荐）】
# from app.utils.akshare_proxy_patch import install_patch_default
# install_patch_default(timeout=60)
#
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
#
# 【方式3：使用本地配置（无需远程服务）】
# from app.utils.akshare_proxy_patch import install_patch_local
# install_patch_local(
#     ua="Mozilla/5.0 ...",
#     nid18="0b6b01ec6206d93c0f1ea184e711daaa",
#     nid18_create_time="1769821785641",
#     proxy="http://ip:port",  # 可选
#     timeout=60
# )
#
#
# 【方式4：使用外部代理池】
# from app.utils.akshare_proxy_patch import install_patch_with_pool
# install_patch_with_pool(
#     ua="Mozilla/5.0 ...",
#     nid18="0b6b01ec6206d93c0f1ea184e711daaa",
#     nid18_create_time="1769821785641",
#     pool_url="http://127.0.0.1:5010",
#     timeout=60
# )
#
#
# 【方式5：自动获取 Cookie 模式】
# from app.utils.akshare_proxy_patch import install_patch_auto
# install_patch_auto(timeout=60)
# -----------------------------------------------------------------------
