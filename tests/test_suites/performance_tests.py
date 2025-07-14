import time

from tests.utilities.api_client import APITestClient
from tests.utilities.validators import ResponseValidator

class PerformanceTestSuite:
    """Performance tests for API endpoints"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = APITestClient()
        self.validator = ResponseValidator()
    
    def test_response_time_get_posts(self):
        """Test response time for GET /posts"""
        start_time = time.time()
        response = self.client.get('/posts')
        end_time = time.time()
        
        response_time = end_time - start_time
        self.validator.validate_status_code(response, 200)
        assert response_time < 2.0, f"Response time {response_time:.3f}s exceeds 2s threshold"
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return self.client.get('/posts/1')
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            
            for future in concurrent.futures.as_completed(futures):
                response = future.result()
                self.validator.validate_status_code(response, 200)