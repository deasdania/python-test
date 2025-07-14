import pytest
from tests.utilities.api_client import APITestClient
from tests.utilities.validators import ResponseValidator

class TestPosts:
    """Comprehensive tests for Posts API endpoints"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.client = APITestClient()
        self.validator = ResponseValidator()
    
    def test_get_all_posts(self):
        """Test GET /posts - Retrieve all posts"""
        response = self.client.get('/posts')
        
        self.validator.validate_status_code(response, 200)
        posts = response.json()
        self.validator.validate_list_response(posts, 100)
        
        # Validate first post structure
        self.validator.validate_post_structure(posts[0])
    
    def test_get_single_post(self):
        """Test GET /posts/{id} - Retrieve single post"""
        post_id = 1
        response = self.client.get(f'/posts/{post_id}')
        
        self.validator.validate_status_code(response, 200)
        post = response.json()
        self.validator.validate_post_structure(post)
        assert post['id'] == post_id
    
    @pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
    def test_get_multiple_posts(self, post_id):
        """Test multiple post IDs"""
        response = self.client.get(f'/posts/{post_id}')
        
        self.validator.validate_status_code(response, 200)
        post = response.json()
        assert post['id'] == post_id
    
    def test_create_post(self):
        """Test POST /posts - Create new post"""
        new_post = {
            'title': 'Test Post Creation',
            'body': 'This is a test post created by automated test suite',
            'userId': 1
        }
        
        response = self.client.post('/posts', new_post)
        
        self.validator.validate_status_code(response, 201)
        created_post = response.json()
        
        assert created_post['title'] == new_post['title']
        assert created_post['body'] == new_post['body']
        assert created_post['userId'] == new_post['userId']
        assert 'id' in created_post
    
    def test_update_post(self):
        """Test PUT /posts/{id} - Update existing post"""
        post_id = 1
        updated_post = {
            'id': post_id,
            'title': 'Updated Post Title',
            'body': 'Updated post body content',
            'userId': 1
        }
        
        response = self.client.put(f'/posts/{post_id}', updated_post)
        
        self.validator.validate_status_code(response, 200)
        result = response.json()
        assert result['title'] == updated_post['title']
        assert result['body'] == updated_post['body']
    
    def test_patch_post(self):
        """Test PATCH /posts/{id} - Partially update post"""
        post_id = 1
        partial_update = {'title': 'Partially Updated Title'}
        
        response = self.client.patch(f'/posts/{post_id}', partial_update)
        
        self.validator.validate_status_code(response, 200)
        result = response.json()
        assert result['title'] == partial_update['title']
    
    def test_delete_post(self):
        """Test DELETE /posts/{id} - Delete post"""
        post_id = 1
        response = self.client.delete(f'/posts/{post_id}')
        
        self.validator.validate_status_code(response, 200)
    
    def test_get_posts_by_user(self):
        """Test GET /posts?userId={id} - Get posts by user"""
        user_id = 1
        response = self.client.get('/posts', params={'userId': user_id})
        
        self.validator.validate_status_code(response, 200)
        posts = response.json()
        
        assert len(posts) > 0
        for post in posts:
            assert post['userId'] == user_id
    
    def test_invalid_post_id(self):
        """Test GET /posts/{invalid_id} - Error handling"""
        invalid_id = 99999
        response = self.client.get(f'/posts/{invalid_id}')
        
        # JSONPlaceholder returns 404 for non-existent resources
        self.validator.validate_status_code(response, 404)