from tests.utilities.api_client import APITestClient
from tests.utilities.validators import ResponseValidator

class TestComments:
    """Comprehensive tests for Comments API endpoints"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = APITestClient()
        self.validator = ResponseValidator()
    
    def test_get_all_comments(self):
        """Test GET /comments - Retrieve all comments"""
        response = self.client.get('/comments')
        
        self.validator.validate_status_code(response, 200)
        comments = response.json()
        self.validator.validate_list_response(comments, 500)
        
        # Validate first comment structure
        self.validator.validate_comment_structure(comments[0])
    
    def test_get_post_comments(self):
        """Test GET /posts/{id}/comments - Get comments for post"""
        post_id = 1
        response = self.client.get(f'/posts/{post_id}/comments')
        
        self.validator.validate_status_code(response, 200)
        comments = response.json()
        
        assert len(comments) > 0
        for comment in comments:
            assert comment['postId'] == post_id