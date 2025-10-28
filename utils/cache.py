import redis
import json
from config.settings import settings

class CacheManager:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL)
            self.redis_client.ping()  # Test connection
        except redis.ConnectionError:
            self.redis_client = None
            print("Redis não disponível - usando cache em memória")
            self.memory_cache = {}
    
    def get(self, key: str):
        """Obtém valor do cache"""
        if self.redis_client:
            try:
                cached = self.redis_client.get(key)
                return cached.decode() if cached else None
            except:
                return None
        else:
            return self.memory_cache.get(key)
    
    def set(self, key: str, value: str, expire: int = 3600):
        """Define valor no cache"""
        if self.redis_client:
            try:
                self.redis_client.setex(key, expire, value)
            except:
                pass
        else:
            self.memory_cache[key] = value
    
    def delete(self, key: str):
        """Remove valor do cache"""
        if self.redis_client:
            try:
                self.redis_client.delete(key)
            except:
                pass
        else:
            self.memory_cache.pop(key, None)