import pytest
import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# Try to import config, fall back to defaults if not available
try:
    from config.test_config import APITestConfig
    REPORTS_DIR = APITestConfig.HTML_REPORTS_DIR
except ImportError:
    REPORTS_DIR = "reports/html"


def run_test_suite(test_type='all'):
    """Run organized test suite"""
    
    # Ensure directories exist
    APITestConfig.ensure_directories()
    
    # Generate timestamp for reports
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Configure pytest arguments based on test type
    pytest_args = ['-v']
    
    if test_type == 'smoke':
        pytest_args.extend(['tests/test_suites/smoke_tests.py'])
        report_name = f'smoke_test_report_{timestamp}.html'
    elif test_type == 'performance':
        pytest_args.extend(['tests/test_suites/performance_tests.py'])
        report_name = f'performance_test_report_{timestamp}.html'
    elif test_type == 'posts':
        pytest_args.extend(['tests/test_cases/test_posts.py'])
        report_name = f'posts_test_report_{timestamp}.html'
    elif test_type == 'users':
        pytest_args.extend(['tests/test_cases/test_users.py'])
        report_name = f'users_test_report_{timestamp}.html'
    else:  # all tests
        pytest_args.extend(['tests/'])
        report_name = f'full_test_report_{timestamp}.html'
    
    # Add HTML report generation
    html_report_path = os.path.join(APITestConfig.HTML_REPORTS_DIR, report_name)
    pytest_args.extend([
        '--html', html_report_path,
        '--self-contained-html'
    ])
    
    print(f"🚀 Running {test_type} tests...")
    print(f"📊 Report will be saved to: {html_report_path}")
    
    # Run pytest
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    print(f"📄 View report: {html_report_path}")
    return exit_code

if __name__ == "__main__":
    test_type = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    valid_types = ['all', 'smoke', 'performance', 'posts', 'users', 'comments']
    
    if test_type not in valid_types:
        print(f"❌ Invalid test type: {test_type}")
        print(f"✅ Valid types: {', '.join(valid_types)}")
        sys.exit(1)
    
    exit_code = run_test_suite(test_type)
    sys.exit(exit_code)