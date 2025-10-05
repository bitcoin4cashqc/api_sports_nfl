import requests
import time
from .cache import Cache

class BaseAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://v1.american-football.api-sports.io"
        self.headers = {
            'x-apisports-key': self.api_key
        }
        self.cache = Cache()
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests to respect rate limits

    def _get(self, endpoint, params=None):
        # Check cache first
        key = f"{endpoint}_{str(params)}"
        cached = self.cache.get(key)
        if cached:
            # Add cache indicator
            cached_data = cached.copy()
            cached_data['from_cache'] = True
            return cached_data
        
        # Rate limiting: wait if needed
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last_request)
        
        # Make the request
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            # Update last request time
            self.last_request_time = time.time()
            
            # Handle HTTP errors
            if response.status_code == 401:
                return {
                    "error": "Authentication failed - Invalid API key",
                    "status_code": response.status_code,
                    "endpoint": endpoint,
                    "params": params
                }
            elif response.status_code == 403:
                return {
                    "error": "Access forbidden - Check API subscription plan",
                    "status_code": response.status_code,
                    "endpoint": endpoint,
                    "params": params
                }
            elif response.status_code == 429:
                return {
                    "error": "Rate limit exceeded - Too many requests",
                    "status_code": response.status_code,
                    "endpoint": endpoint,
                    "params": params
                }
            elif response.status_code != 200:
                return {
                    "error": f"HTTP {response.status_code} - {response.reason}",
                    "status_code": response.status_code,
                    "endpoint": endpoint,
                    "params": params,
                    "raw_response": response.text
                }
            
            # Try to parse JSON
            try:
                data = response.json()
            except ValueError as e:
                return {
                    "error": "JSON parsing failed",
                    "status_code": response.status_code,
                    "endpoint": endpoint,
                    "params": params,
                    "raw_response": response.text
                }
            
            # Add metadata
            data['from_cache'] = False
            data['status_code'] = response.status_code
            data['endpoint'] = endpoint
            data['params'] = params
            
           
            # Cache successful responses
            self.cache.set(key, data)
            return data
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Request failed: {str(e)}",
                "endpoint": endpoint,
                "params": params
            }