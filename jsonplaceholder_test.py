import requests
import json
import pytest
from typing import Dict, Any

class JSONPlaceholderAPITest:
    """Test suite for JSONPlaceholder API"""
    
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Python-API-Test/1.0'
        })
    
    def test_get_all_posts(self):
        """Test GET /posts - Retrieve all posts"""
        print("\n=== Testing GET /posts ===")
        
        response = self.session.get(f"{self.BASE_URL}/posts")
        
        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        posts = response.json()
        assert isinstance(posts, list), "Response should be a list"
        assert len(posts) == 100, f"Expected 100 posts, got {len(posts)}"
        
        # Check first post structure
        first_post = posts[0]
        required_fields = ['userId', 'id', 'title', 'body']
        for field in required_fields:
            assert field in first_post, f"Missing field: {field}"
        
        print(f"✓ Successfully retrieved {len(posts)} posts")
        print(f"✓ First post title: {first_post['title']}")
        return True
    
    def test_get_single_post(self):
        """Test GET /posts/{id} - Retrieve single post"""
        print("\n=== Testing GET /posts/1 ===")
        
        post_id = 1
        response = self.session.get(f"{self.BASE_URL}/posts/{post_id}")
        
        # Assertions
        assert response.status_code == 200
        
        post = response.json()
        assert post['id'] == post_id
        assert 'userId' in post
        assert 'title' in post
        assert 'body' in post
        
        print(f"✓ Retrieved post {post_id}: {post['title']}")
        return True
    
    def test_create_post(self):
        """Test POST /posts - Create new post"""
        print("\n=== Testing POST /posts ===")
        
        new_post = {
            'title': 'Test Post from Python',
            'body': 'This is a test post created by automation script',
            'userId': 1
        }
        
        response = self.session.post(f"{self.BASE_URL}/posts", json=new_post)
        
        # Assertions
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        created_post = response.json()
        assert created_post['title'] == new_post['title']
        assert created_post['body'] == new_post['body']
        assert created_post['userId'] == new_post['userId']
        assert 'id' in created_post
        
        print(f"✓ Created post with ID: {created_post['id']}")
        return created_post
    
    def test_update_post(self):
        """Test PUT /posts/{id} - Update existing post"""
        print("\n=== Testing PUT /posts/1 ===")
        
        post_id = 1
        updated_post = {
            'id': post_id,
            'title': 'Updated Post Title',
            'body': 'Updated post body content',
            'userId': 1
        }
        
        response = self.session.put(f"{self.BASE_URL}/posts/{post_id}", json=updated_post)
        
        # Assertions
        assert response.status_code == 200
        
        result = response.json()
        assert result['id'] == post_id
        assert result['title'] == updated_post['title']
        assert result['body'] == updated_post['body']
        
        print(f"✓ Updated post {post_id}")
        return True
    
    def test_partial_update_post(self):
        """Test PATCH /posts/{id} - Partially update post"""
        print("\n=== Testing PATCH /posts/1 ===")
        
        post_id = 1
        partial_update = {
            'title': 'Partially Updated Title'
        }
        
        response = self.session.patch(f"{self.BASE_URL}/posts/{post_id}", json=partial_update)
        
        # Assertions
        assert response.status_code == 200
        
        result = response.json()
        assert result['title'] == partial_update['title']
        assert result['id'] == post_id
        
        print(f"✓ Partially updated post {post_id}")
        return True
    
    def test_delete_post(self):
        """Test DELETE /posts/{id} - Delete post"""
        print("\n=== Testing DELETE /posts/1 ===")
        
        post_id = 1
        response = self.session.delete(f"{self.BASE_URL}/posts/{post_id}")
        
        # Assertions
        assert response.status_code == 200
        
        print(f"✓ Deleted post {post_id}")
        return True
    
    def test_get_users(self):
        """Test GET /users - Retrieve all users"""
        print("\n=== Testing GET /users ===")
        
        response = self.session.get(f"{self.BASE_URL}/users")
        
        # Assertions
        assert response.status_code == 200
        
        users = response.json()
        assert isinstance(users, list)
        assert len(users) == 10, f"Expected 10 users, got {len(users)}"
        
        # Check user structure
        first_user = users[0]
        required_fields = ['id', 'name', 'username', 'email']
        for field in required_fields:
            assert field in first_user, f"Missing field: {field}"
        
        print(f"✓ Retrieved {len(users)} users")
        return True
    
    def test_get_comments(self):
        """Test GET /comments - Retrieve all comments"""
        print("\n=== Testing GET /comments ===")
        
        response = self.session.get(f"{self.BASE_URL}/comments")
        
        # Assertions
        assert response.status_code == 200
        
        comments = response.json()
        assert isinstance(comments, list)
        assert len(comments) == 500, f"Expected 500 comments, got {len(comments)}"
        
        print(f"✓ Retrieved {len(comments)} comments")
        return True
    
    def test_get_post_comments(self):
        """Test GET /posts/{id}/comments - Get comments for specific post"""
        print("\n=== Testing GET /posts/1/comments ===")
        
        post_id = 1
        response = self.session.get(f"{self.BASE_URL}/posts/{post_id}/comments")
        
        # Assertions
        assert response.status_code == 200
        
        comments = response.json()
        assert isinstance(comments, list)
        
        # All comments should belong to the specified post
        for comment in comments:
            assert comment['postId'] == post_id
        
        print(f"✓ Retrieved {len(comments)} comments for post {post_id}")
        return True
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint - should return 404"""
        print("\n=== Testing invalid endpoint ===")
        
        response = self.session.get(f"{self.BASE_URL}/invalid-endpoint")
        
        # Assertions
        assert response.status_code == 404
        
        print("✓ Invalid endpoint correctly returned 404")
        return True
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting JSONPlaceholder API Tests")
        print("=" * 50)
        
        test_methods = [
            self.test_get_all_posts,
            self.test_get_single_post,
            self.test_create_post,
            self.test_update_post,
            self.test_partial_update_post,
            self.test_delete_post,
            self.test_get_users,
            self.test_get_comments,
            self.test_get_post_comments,
            self.test_invalid_endpoint
        ]
        
        passed = 0
        failed = 0
        
        for test_method in test_methods:
            try:
                test_method()
                passed += 1
                print(f"✅ {test_method.__name__} - PASSED")
            except Exception as e:
                failed += 1
                print(f"❌ {test_method.__name__} - FAILED: {str(e)}")
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed} passed, {failed} failed")
        print(f"🎯 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        return passed, failed

def main():
    """Main function to run tests"""
    tester = JSONPlaceholderAPITest()
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()