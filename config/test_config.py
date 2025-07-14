
import os
from datetime import datetime

class APITestConfig:
    """Centralized configuration for API testing"""
    
    # API Configuration
    BASE_URL = "https://jsonplaceholder.typicode.com"
    TIMEOUT = 30
    MAX_RETRIES = 3
    
    # Environment
    ENVIRONMENT = os.getenv('TEST_ENV', 'test')
    
    # Report Configuration
    REPORTS_DIR = "reports"
    HTML_REPORTS_DIR = os.path.join(REPORTS_DIR, "html")
    JSON_REPORTS_DIR = os.path.join(REPORTS_DIR, "json")
    
    # Test Configuration
    INCLUDE_PERFORMANCE_TESTS = True
    INCLUDE_NEGATIVE_TESTS = True
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories"""
        directories = [
            cls.REPORTS_DIR,
            cls.HTML_REPORTS_DIR,
            cls.JSON_REPORTS_DIR
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)