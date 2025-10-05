import json
import os
import time

class Cache:
    def __init__(self, cache_file='cache.json', expire_seconds=3600):
        self.cache_file = cache_file
        self.expire_seconds = expire_seconds
        self.cache = self._load_cache()

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.expire_seconds:
                return entry['data']
            else:
                del self.cache[key]
                self._save_cache()
        return None

    def set(self, key, data):
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }
        self._save_cache()
    
    def is_cached(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['timestamp'] < self.expire_seconds:
                return True
            else:
                del self.cache[key]
                self._save_cache()
        return False
    
    def get_stats(self):
        total_requests = len(self.cache)
        cache_hits = sum(1 for entry in self.cache.values() 
                        if time.time() - entry['timestamp'] < self.expire_seconds)
        cache_misses = total_requests - cache_hits
        hit_rate = cache_hits / total_requests if total_requests > 0 else 0
        
        return {
            'total_requests': total_requests,
            'cache_hits': cache_hits,
            'cache_misses': cache_misses,
            'hit_rate': hit_rate
        }