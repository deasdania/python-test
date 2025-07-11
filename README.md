# JSONPlaceholder API Test Suite

A comprehensive Python automation test suite for the JSONPlaceholder API (https://jsonplaceholder.typicode.com). This project demonstrates REST API testing using Python's `requests` library and `pytest` framework.

## 🎯 Project Overview

This test suite covers all major HTTP methods and endpoints of the JSONPlaceholder API:
- **GET** requests (retrieve data)
- **POST** requests (create data)
- **PUT** requests (update data)
- **PATCH** requests (partial update)
- **DELETE** requests (delete data)

## 📋 Features

- ✅ **Comprehensive API Testing** - Tests all CRUD operations
- ✅ **Two Testing Approaches** - Standard Python script and pytest framework
- ✅ **Detailed Assertions** - Validates response codes, data structure, and content
- ✅ **Error Handling** - Tests invalid endpoints and error scenarios
- ✅ **Parameterized Tests** - Tests multiple scenarios efficiently
- ✅ **HTML Reports** - Generate detailed test reports
- ✅ **Clean Code Structure** - Well-organized and documented

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project:**
```bash
git clone <repository-url>
cd jsonplaceholder-api-tests
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running Tests

#### Option 1: Standard Python Script
```bash
python jsonplaceholder_test.py
```

#### Option 2: Pytest Framework
```bash
# Basic run
pytest pytest_jsonplaceholder.py -v

# With HTML report
pytest pytest_jsonplaceholder.py -v --html=report.html --self-contained-html

# Run specific test
pytest pytest_jsonplaceholder.py::TestJSONPlaceholderAPI::test_get_all_posts -v
```

## 📁 Project Structure

```
jsonplaceholder-api-tests/
│
├── jsonplaceholder_test.py      # Main test script (class-based)
├── pytest_jsonplaceholder.py   # Pytest version with fixtures
├── requirements.txt             # Python dependencies
├── README.md                   # This file
└── report.html                 # Generated HTML report (after running)
```

## 🧪 Test Coverage

### Endpoints Tested

| Method | Endpoint | Description | Test Function |
|--------|----------|-------------|---------------|
| GET | `/posts` | Get all posts | `test_get_all_posts` |
| GET | `/posts/{id}` | Get single post | `test_get_single_post` |
| POST | `/posts` | Create new post | `test_create_post` |
| PUT | `/posts/{id}` | Update post | `test_update_post` |
| PATCH | `/posts/{id}` | Partial update | `test_partial_update_post` |
| DELETE | `/posts/{id}` | Delete post | `test_delete_post` |
| GET | `/users` | Get all users | `test_get_users` |
| GET | `/comments` | Get all comments | `test_get_comments` |
| GET | `/posts/{id}/comments` | Get post comments | `test_get_post_comments` |
| GET | `/invalid-endpoint` | Test error handling | `test_invalid_endpoint` |

### What Each Test Validates

- **Response Status Codes** (200, 201, 404)
- **Response Data Structure** (JSON format, required fields)
- **Data Integrity** (correct IDs, relationships)
- **CRUD Operations** (Create, Read, Update, Delete)
- **Error Handling** (invalid endpoints)

## 📊 Sample Output

```
🚀 Starting JSONPlaceholder API Tests
==================================================

=== Testing GET /posts ===
✓ Successfully retrieved 100 posts
✓ First post title: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
✅ test_get_all_posts - PASSED

=== Testing GET /posts/1 ===
✓ Retrieved post 1: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
✅ test_get_single_post - PASSED

=== Testing POST /posts ===
✓ Created post with ID: 101
✅ test_create_post - PASSED

=== Testing PUT /posts/1 ===
✓ Updated post 1
✅ test_update_post - PASSED

=== Testing PATCH /posts/1 ===
✓ Partially updated post 1
✅ test_partial_update_post - PASSED

=== Testing DELETE /posts/1 ===
✓ Deleted post 1
✅ test_delete_post - PASSED

=== Testing GET /users ===
✓ Retrieved 10 users
✅ test_get_users - PASSED

=== Testing GET /comments ===
✓ Retrieved 500 comments
✅ test_get_comments - PASSED

=== Testing GET /posts/1/comments ===
✓ Retrieved 5 comments for post 1
✅ test_get_post_comments - PASSED

=== Testing invalid endpoint ===
✓ Invalid endpoint correctly returned 404
✅ test_invalid_endpoint - PASSED

==================================================
📊 Test Results: 10 passed, 0 failed
🎯 Success Rate: 100.0%
```

## 🔧 Advanced Usage

### Running Tests with Coverage
```bash
pip install pytest-cov
pytest pytest_jsonplaceholder.py --cov=. --cov-report=html
```

### Quic run with config
```bash
python run_tests.py
```

### Running Tests in Parallel
```bash
pip install pytest-xdist
pytest pytest_jsonplaceholder.py -n auto
```

### Filtering Tests
```bash
# Run only GET tests
pytest pytest_jsonplaceholder.py -k "get" -v

# Run only POST and PUT tests
pytest pytest_jsonplaceholder.py -k "post or put" -v
```

### Generate html report
```bash
python -m pytest pytest_jsonplaceholder.py -v --html=report.html --self-contained-html --css=custom.css
```
### Custom Test Markers
```bash
# Run only critical tests (if marked with @pytest.mark.critical)
pytest pytest_jsonplaceholder.py -m critical
```

## 📝 Customization

### Adding New Tests

1. **In the main script (`jsonplaceholder_test.py`):**
```python
def test_your_new_test(self):
    """Test description"""
    print("\n=== Testing your endpoint ===")
    
    response = self.session.get(f"{self.BASE_URL}/your-endpoint")
    
    assert response.status_code == 200
    # Add your assertions here
    
    print("✓ Your test passed")
    return True
```

2. **In pytest version (`pytest_jsonplaceholder.py`):**
```python
def test_your_new_test(self, api_client):
    """Test description"""
    response = api_client.get(f"{BASE_URL}/your-endpoint")
    
    assert response.status_code == 200
    # Add your assertions here
```

### Environment Configuration

Create a `config.py` file for different environments:
```python
import os

class Config:
    BASE_URL = os.getenv('API_BASE_URL', 'https://jsonplaceholder.typicode.com')
    TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))
    
class TestConfig(Config):
    BASE_URL = 'https://jsonplaceholder.typicode.com'
    
class ProductionConfig(Config):
    BASE_URL = 'https://your-production-api.com'
```

## 🛠️ Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| requests | >=2.31.0 | HTTP requests library |
| pytest | >=7.4.0 | Testing framework |
| pytest-html | >=3.2.0 | HTML report generation |

## 📚 Learning Resources

### API Testing Concepts
- **REST API Fundamentals** - HTTP methods, status codes, headers
- **Test Automation** - Assertions, test organization, reporting
- **Python Testing** - unittest, pytest, fixtures

### Useful Links
- [JSONPlaceholder API Documentation](https://jsonplaceholder.typicode.com/guide/)
- [Requests Library Documentation](https://requests.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [REST API Testing Best Practices](https://restfulapi.net/rest-api-testing/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔍 Troubleshooting

### Common Issues

1. **Import Error**: Make sure you have installed all dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. **Network Issues**: Check your internet connection and firewall settings

3. **Python Version**: Ensure you're using Python 3.7 or higher
   ```bash
   python --version
   ```

4. **Virtual Environment**: Make sure your virtual environment is activated
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

### Getting Help

- Check the [Issues](https://github.com/your-repo/issues) page
- Review the API documentation
- Ensure all prerequisites are met

## 🎯 Next Steps

After running these tests successfully, you can:

1. **Extend the test suite** with more complex scenarios
2. **Add performance testing** with response time validation
3. **Implement data-driven testing** with CSV/JSON test data
4. **Add authentication testing** for secured APIs
5. **Create CI/CD pipeline** integration
6. **Add API contract testing** with schema validation

---

**Happy Testing! 🚀**

For questions or suggestions, please open an issue or contact the maintainers.