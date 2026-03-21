import time
import random
import threading
import requests
from typing import Optional, List


class ProxyPoolManager:
    """Redis-based proxy pool manager with auto-refresh and failover"""
    
    def __init__(
        self,
        redis_client=None,
        external_pool_url: str = "http://122.51.65.65:5010",
        key_prefix: str = "akshare:proxy_pool:",
        max_proxies: int = 100,
        min_proxies: int = 10
    ):
        self.redis_client = redis_client
        self.external_pool_url = external_pool_url.rstrip("/")
        self.key_prefix = key_prefix
        self.max_proxies = max_proxies
        self.min_proxies = min_proxies
        self._lock = threading.Lock()
        self._current_proxy: Optional[str] = None
        self._fail_count = 0
        self._max_fail = 3
        self._memory_proxies: List[str] = []
        
    def _get_redis(self):
        if self.redis_client:
            return self.redis_client
        try:
            import redis
            from app.core.config import settings
            if settings.REDIS_ENABLED:
                self.redis_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    password=settings.REDIS_PASSWORD,
                    decode_responses=True
                )
                return self.redis_client
        except Exception as e:
            print(f"[ProxyPool] Redis connection failed: {e}")
        return None
    
    def fetch_from_external_pool(self, count: int = 100) -> List[str]:
        proxies = []
        try:
            fetch_count = min(count, 50)
            for _ in range(fetch_count):
                try:
                    resp = requests.get(f"{self.external_pool_url}/get/", timeout=3)
                    content_type = resp.headers.get("Content-Type", "")
                    
                    if "json" in content_type:
                        data = resp.json()
                        if data.get("code") == 0 and "no proxy" in str(data.get("src", "")):
                            break
                        proxy = data.get("proxy") or data.get("http") or data.get("https")
                    else:
                        proxy = resp.text.strip()
                    
                    if proxy and proxy not in ("no proxy", "null") and len(proxy) > 5:
                        if not proxy.startswith("http"):
                            proxy = f"http://{proxy}"
                        if proxy not in proxies:
                            proxies.append(proxy)
                except Exception:
                    continue
                    
            print(f"[ProxyPool] Fetched {len(proxies)} proxies")
        except Exception as e:
            print(f"[ProxyPool] Fetch failed: {e}")
        return proxies
    
    def validate_proxy(self, proxy: str, timeout: int = 3) -> bool:
        test_urls = ["http://www.baidu.com"]
        for url in test_urls:
            try:
                resp = requests.get(
                    url,
                    proxies={"http": proxy, "https": proxy},
                    timeout=timeout,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                if resp.status_code == 200:
                    return True
            except Exception:
                continue
        return False
    
    def refresh_proxies(self, validate: bool = False) -> int:
        proxies = self.fetch_from_external_pool(self.max_proxies)
        if not proxies:
            return 0
        
        valid_proxies = proxies if not validate else [p for p in proxies if self.validate_proxy(p)]
        
        redis = self._get_redis()
        if redis:
            try:
                key = f"{self.key_prefix}available"
                redis.delete(key)
                if valid_proxies:
                    for proxy in valid_proxies:
                        redis.sadd(key, proxy)
                    redis.expire(key, 86400)
                print(f"[ProxyPool] Stored {len(valid_proxies)} proxies to Redis")
            except Exception as e:
                print(f"[ProxyPool] Redis store failed: {e}")
                self._memory_proxies = valid_proxies
        else:
            self._memory_proxies = valid_proxies
            print(f"[ProxyPool] Stored {len(valid_proxies)} proxies to memory")
        return len(valid_proxies)
    
    def get_proxy(self) -> Optional[str]:
        with self._lock:
            redis = self._get_redis()
            if redis:
                try:
                    proxy = redis.srandmember(f"{self.key_prefix}available")
                    if proxy:
                        return proxy
                except Exception:
                    pass
            if self._memory_proxies:
                return random.choice(self._memory_proxies)
            return None
    
    def mark_proxy_failed(self, proxy: str):
        with self._lock:
            redis = self._get_redis()
            if redis:
                try:
                    key = f"{self.key_prefix}available"
                    redis.srem(key, proxy)
                    redis.sadd(f"{self.key_prefix}failed", proxy)
                    count = redis.scard(key)
                    print(f"[ProxyPool] Proxy failed ({count} remaining)")
                    if count < self.min_proxies:
                        threading.Thread(target=self.refresh_proxies, daemon=True).start()
                except Exception as e:
                    print(f"[ProxyPool] Mark failed error: {e}")
            if proxy in self._memory_proxies:
                self._memory_proxies.remove(proxy)
    
    def next_proxy(self, mark_failed: bool = False) -> Optional[str]:
        with self._lock:
            if mark_failed and self._current_proxy:
                self.mark_proxy_failed(self._current_proxy)
                self._current_proxy = None
            if not self._current_proxy:
                self._current_proxy = self.get_proxy()
            return self._current_proxy
    
    def get_pool_status(self) -> dict:
        redis = self._get_redis()
        available = 0
        failed = 0
        if redis:
            try:
                available = redis.scard(f"{self.key_prefix}available")
                failed = redis.scard(f"{self.key_prefix}failed")
            except Exception:
                pass
        else:
            available = len(self._memory_proxies)
        return {
            "available": available,
            "failed": failed,
            "current_proxy": self._current_proxy,
            "min_proxies": self.min_proxies,
            "max_proxies": self.max_proxies,
            "needs_refresh": available < self.min_proxies
        }


_proxy_pool_manager: Optional[ProxyPoolManager] = None


def get_proxy_pool_manager() -> ProxyPoolManager:
    global _proxy_pool_manager
    if _proxy_pool_manager is None:
        from app.core.config import settings
        _proxy_pool_manager = ProxyPoolManager(external_pool_url=settings.AKSHARE_PROXY_POOL_URL)
    return _proxy_pool_manager


def init_proxy_pool(validate: bool = False) -> int:
    return get_proxy_pool_manager().refresh_proxies(validate=validate)
