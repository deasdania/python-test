import os
from datetime import datetime

class TestConfig:
    """Configuration settings for API testing"""
    
    # API Configuration
    BASE_URL = "https://jsonplaceholder.typicode.com"
    TIMEOUT = 30  # seconds
    
    # Report Configuration
    REPORTS_DIR = "html"  # Directory to store HTML reports
    REPORT_NAME = f"api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    # Test Configuration
    INCLUDE_PERFORMANCE_TESTS = True
    MAX_RETRIES = 3
    
    # Environment
    ENVIRONMENT = os.getenv('TEST_ENV', 'test')
    
    @classmethod
    def get_report_path(cls):
        """Get the full path for the report file"""
        return os.path.join(cls.REPORTS_DIR, cls.REPORT_NAME)
    
    @classmethod
    def ensure_reports_dir(cls):
        """Ensure the reports directory exists"""
        if not os.path.exists(cls.REPORTS_DIR):
            os.makedirs(cls.REPORTS_DIR)
            print(f"📁 Created reports directory: {cls.REPORTS_DIR}/")
        return cls.REPORTS_DIR