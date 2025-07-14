from tests.utilities.api_client import APITestClient
from tests.utilities.validators import ResponseValidator

class SmokeTestSuite:
    """Quick smoke tests for basic API functionality"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = APITestClient()
        self.validator = ResponseValidator()
    
    def test_api_connectivity(self):
        """Test basic API connectivity"""
        response = self.client.get('/posts/1')
        self.validator.validate_status_code(response, 200)
    
    def test_all_main_endpoints(self):
        """Test all main endpoints are accessible"""
        endpoints = ['/posts', '/users', '/comments', '/albums', '/photos', '/todos']
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.validator.validate_status_code(response, 200)
            assert len(response.json()) > 0
