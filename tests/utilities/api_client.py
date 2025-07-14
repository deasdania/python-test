
import requests
import time
from typing import Dict, Any, Optional
from config.test_config import APITestConfig

class APITestClient:
    """Reusable API client for testing"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'API-Test-Suite/2.0'
        })
        self.base_url = APITestConfig.BASE_URL
        self.timeout = APITestConfig.TIMEOUT
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """GET request with error handling"""
        url = f"{self.base_url}{endpoint}"
        return self._make_request('GET', url, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """POST request with error handling"""
        url = f"{self.base_url}{endpoint}"
        return self._make_request('POST', url, json=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """PUT request with error handling"""
        url = f"{self.base_url}{endpoint}"
        return self._make_request('PUT', url, json=data)
    
    def patch(self, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """PATCH request with error handling"""
        url = f"{self.base_url}{endpoint}"
        return self._make_request('PATCH', url, json=data)
    
    def delete(self, endpoint: str) -> requests.Response:
        """DELETE request with error handling"""
        url = f"{self.base_url}{endpoint}"
        return self._make_request('DELETE', url)
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make HTTP request with retry logic"""
        for attempt in range(APITestConfig.MAX_RETRIES):
            try:
                response = self.session.request(
                    method, url, timeout=self.timeout, **kwargs
                )
                return response
            except requests.exceptions.RequestException as e:
                if attempt == APITestConfig.MAX_RETRIES - 1:
                    raise e
                time.sleep(1)  # Wait before retry