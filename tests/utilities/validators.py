from typing import Dict, List, Any

class ResponseValidator:
    """Validate API responses"""
    
    @staticmethod
    def validate_status_code(response, expected_code: int):
        """Validate HTTP status code"""
        assert response.status_code == expected_code, \
            f"Expected status {expected_code}, got {response.status_code}"
    
    @staticmethod
    def validate_json_structure(data: Dict, required_fields: List[str]):
        """Validate JSON structure has required fields"""
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
    
    @staticmethod
    def validate_list_response(data: List, expected_length: int = None):
        """Validate list response"""
        assert isinstance(data, list), "Response should be a list"
        if expected_length:
            assert len(data) == expected_length, \
                f"Expected {expected_length} items, got {len(data)}"
    
    @staticmethod
    def validate_post_structure(post: Dict):
        """Validate post object structure"""
        required_fields = ['userId', 'id', 'title', 'body']
        ResponseValidator.validate_json_structure(post, required_fields)
        assert isinstance(post['id'], int), "Post ID should be integer"
        assert isinstance(post['userId'], int), "User ID should be integer"
        assert len(post['title']) > 0, "Post title should not be empty"
    
    @staticmethod
    def validate_user_structure(user: Dict):
        """Validate user object structure"""
        required_fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
        ResponseValidator.validate_json_structure(user, required_fields)
        assert '@' in user['email'], "Invalid email format"
    
    @staticmethod
    def validate_comment_structure(comment: Dict):
        """Validate comment object structure"""
        required_fields = ['postId', 'id', 'name', 'email', 'body']
        ResponseValidator.validate_json_structure(comment, required_fields)
        assert '@' in comment['email'], "Invalid email format"