# 🚀 API Test Suite

A comprehensive, organized test suite for the JSONPlaceholder API with modern structure and beautiful reporting.

## 📁 Project Structure

```
api-test-suite/
├── 📂 tests/                     # Main test directory
│   ├── 📂 test_cases/            # Individual test modules
│   ├── 📂 test_suites/           # Test suite collections  
│   ├── 📂 fixtures/              # Test data
│   └── 📂 utilities/             # Helper utilities
├── 📂 config/                    # Configuration
├── 📂 reports/                   # Generated reports
├── 📂 scripts/                   # Utility scripts
└── 📂 docs/                      # Documentation
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run smoke tests:**
   ```bash
   python quick_test.py
   ```

3. **Run all tests with report:**
   ```bash
   python scripts/run_tests.py all
   ```

## 🧪 Test Categories

- **Smoke Tests** - Quick API health checks
- **Regression Tests** - Full test coverage
- **Performance Tests** - Response time validation
- **Integration Tests** - Cross-resource testing

## 📊 Test Commands

```bash
# Quick smoke test
pytest tests/test_suites/smoke_tests.py -v

# Run specific test file
pytest tests/test_cases/test_posts.py -v

# Run all tests with markers
pytest -m smoke -v
```

## 📈 Reports

Reports are automatically generated in `reports/html/` directory with:
- ✅ Test results summary
- 📊 Execution metrics
- 🔍 Detailed failure information
- 📱 Mobile-friendly interface

## 🎯 Test Markers

Use pytest markers to run specific test types:
```bash
pytest -m smoke        # Smoke tests only
pytest -m regression   # Regression tests only
pytest -m performance  # Performance tests only
pytest -m negative     # Error handling tests
```

## 🔧 Configuration

Edit `config/test_config.py` to modify:
- API base URL
- Timeout settings
- Report configurations
- Environment settings
