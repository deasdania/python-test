
import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def api_client():
    """Create a requests session for API testing"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'Python-API-Test/1.0'
    })
    return session

class TestJSONPlaceholderAPI:
    """Pytest class for JSONPlaceholder API tests"""
    
    def test_get_all_posts(self, api_client):
        """Test GET /posts - Retrieve all posts"""
        response = api_client.get(f"{BASE_URL}/posts")
        
        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) == 100
        
        # Check first post structure
        first_post = posts[0]
        required_fields = ['userId', 'id', 'title', 'body']
        for field in required_fields:
            assert field in first_post
    
    def test_get_single_post(self, api_client):
        """Test GET /posts/{id} - Retrieve single post"""
        post_id = 1
        response = api_client.get(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 200
        post = response.json()
        assert post['id'] == post_id
        assert 'userId' in post
        assert 'title' in post
        assert 'body' in post
    
    def test_create_post(self, api_client):
        """Test POST /posts - Create new post"""
        new_post = {
            'title': 'Test Post from Pytest',
            'body': 'This is a test post created by pytest',
            'userId': 1
        }
        
        response = api_client.post(f"{BASE_URL}/posts", json=new_post)
        
        assert response.status_code == 201
        created_post = response.json()
        assert created_post['title'] == new_post['title']
        assert created_post['body'] == new_post['body']
        assert created_post['userId'] == new_post['userId']
        assert 'id' in created_post
    
    def test_update_post(self, api_client):
        """Test PUT /posts/{id} - Update existing post"""
        post_id = 1
        updated_post = {
            'id': post_id,
            'title': 'Updated Post Title',
            'body': 'Updated post body content',
            'userId': 1
        }
        
        response = api_client.put(f"{BASE_URL}/posts/{post_id}", json=updated_post)
        
        assert response.status_code == 200
        result = response.json()
        assert result['id'] == post_id
        assert result['title'] == updated_post['title']
    
    def test_delete_post(self, api_client):
        """Test DELETE /posts/{id} - Delete post"""
        post_id = 1
        response = api_client.delete(f"{BASE_URL}/posts/{post_id}")
        
        assert response.status_code == 200
    
    def test_get_users(self, api_client):
        """Test GET /users - Retrieve all users"""
        response = api_client.get(f"{BASE_URL}/users")
        
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        assert len(users) == 10
    
    def test_invalid_endpoint(self, api_client):
        """Test invalid endpoint - should return 404"""
        response = api_client.get(f"{BASE_URL}/invalid-endpoint")
        assert response.status_code == 404
    
    @pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
    def test_multiple_posts(self, api_client, post_id):
        """Test multiple posts using parameterized tests"""
        response = api_client.get(f"{BASE_URL}/posts/{post_id}")
        assert response.status_code == 200
        post = response.json()
        assert post['id'] == post_id