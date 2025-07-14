from tests.utilities.api_client import APITestClient
from tests.utilities.validators import ResponseValidator

class TestUsers:
    """Comprehensive tests for Users API endpoints"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = APITestClient()
        self.validator = ResponseValidator()
    
    def test_get_all_users(self):
        """Test GET /users - Retrieve all users"""
        response = self.client.get('/users')
        
        self.validator.validate_status_code(response, 200)
        users = response.json()
        self.validator.validate_list_response(users, 10)
        
        # Validate first user structure
        self.validator.validate_user_structure(users[0])
    
    def test_get_single_user(self):
        """Test GET /users/{id} - Retrieve single user"""
        user_id = 1
        response = self.client.get(f'/users/{user_id}')
        
        self.validator.validate_status_code(response, 200)
        user = response.json()
        self.validator.validate_user_structure(user)
        assert user['id'] == user_id
    
    def test_get_user_posts(self):
        """Test GET /users/{id}/posts - Get user's posts"""
        user_id = 1
        response = self.client.get(f'/users/{user_id}/posts')
        
        self.validator.validate_status_code(response, 200)
        posts = response.json()
        
        assert len(posts) > 0
        for post in posts:
            assert post['userId'] == user_id
    
    def test_get_user_albums(self):
        """Test GET /users/{id}/albums - Get user's albums"""
        user_id = 1
        response = self.client.get(f'/users/{user_id}/albums')
        
        self.validator.validate_status_code(response, 200)
        albums = response.json()
        
        assert len(albums) > 0
        for album in albums:
            assert album['userId'] == user_id