import requests
import json
import datetime
import os
import platform
import sys
from typing import Dict, Any, List

class BeautifulAPITestReport:
    """Generate stunning HTML test reports with modern design"""
    
    def __init__(self):
        self.BASE_URL = "https://jsonplaceholder.typicode.com"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Python-API-Test/1.0'
        })
        self.test_results = []
        self.start_time = None
        self.end_time = None
        self.environment_info = self._get_environment_info()
    
    def _get_environment_info(self):
        """Collect environment information"""
        return {
            'python_version': sys.version.split()[0],
            'platform': platform.system(),
            'machine': platform.machine(),
            'requests_version': requests.__version__,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def run_test(self, test_name: str, test_func, description: str = "", *args, **kwargs):
        """Run a single test and record results"""
        start_time = datetime.datetime.now()
        
        try:
            result = test_func(*args, **kwargs)
            status = "PASSED"
            error_message = None
            details = result if isinstance(result, str) else "Test completed successfully"
        except Exception as e:
            status = "FAILED"
            error_message = str(e)
            details = f"Error: {error_message}"
        
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        self.test_results.append({
            'name': test_name,
            'description': description,
            'status': status,
            'duration': duration,
            'details': details,
            'error': error_message,
            'timestamp': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'endpoint': getattr(test_func, 'endpoint', 'N/A'),
            'method': getattr(test_func, 'method', 'N/A')
        })
        
        return status == "PASSED"
    
    def test_get_all_posts(self):
        """Test GET /posts - Retrieve all posts"""
        response = self.session.get(f"{self.BASE_URL}/posts")
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        posts = response.json()
        assert len(posts) == 100, f"Expected 100 posts, got {len(posts)}"
        
        # Validate first post structure
        first_post = posts[0]
        required_fields = ['userId', 'id', 'title', 'body']
        for field in required_fields:
            assert field in first_post, f"Missing field: {field}"
        
        return f"✅ Successfully retrieved {len(posts)} posts. Response time: {response.elapsed.total_seconds():.3f}s"
    
    def test_get_single_post(self):
        """Test GET /posts/1 - Retrieve single post"""
        response = self.session.get(f"{self.BASE_URL}/posts/1")
        assert response.status_code == 200
        
        post = response.json()
        assert post['id'] == 1
        assert len(post['title']) > 0
        assert len(post['body']) > 0
        
        return f"✅ Retrieved post: '{post['title'][:50]}...' (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_create_post(self):
        """Test POST /posts - Create new post"""
        new_post = {
            'title': 'Automated Test Post',
            'body': 'This post was created by our automated test suite to verify the API functionality.',
            'userId': 1
        }
        
        response = self.session.post(f"{self.BASE_URL}/posts", json=new_post)
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        
        created_post = response.json()
        assert created_post['title'] == new_post['title']
        assert created_post['body'] == new_post['body']
        assert 'id' in created_post
        
        return f"✅ Created post with ID: {created_post['id']} (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_update_post(self):
        """Test PUT /posts/1 - Update existing post"""
        updated_post = {
            'id': 1,
            'title': 'Updated Test Post',
            'body': 'This post has been updated by our test automation.',
            'userId': 1
        }
        
        response = self.session.put(f"{self.BASE_URL}/posts/1", json=updated_post)
        assert response.status_code == 200
        
        result = response.json()
        assert result['title'] == updated_post['title']
        
        return f"✅ Successfully updated post 1 (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_patch_post(self):
        """Test PATCH /posts/1 - Partially update post"""
        partial_update = {'title': 'Partially Updated via PATCH'}
        
        response = self.session.patch(f"{self.BASE_URL}/posts/1", json=partial_update)
        assert response.status_code == 200
        
        result = response.json()
        assert result['title'] == partial_update['title']
        
        return f"✅ Successfully patched post 1 (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_delete_post(self):
        """Test DELETE /posts/1 - Delete post"""
        response = self.session.delete(f"{self.BASE_URL}/posts/1")
        assert response.status_code == 200
        
        return f"✅ Successfully deleted post 1 (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_get_users(self):
        """Test GET /users - Retrieve all users"""
        response = self.session.get(f"{self.BASE_URL}/users")
        assert response.status_code == 200
        
        users = response.json()
        assert len(users) == 10, f"Expected 10 users, got {len(users)}"
        
        # Validate user structure
        first_user = users[0]
        required_fields = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
        for field in required_fields:
            assert field in first_user, f"Missing field: {field}"
        
        return f"✅ Retrieved {len(users)} users with complete profiles (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_get_comments(self):
        """Test GET /comments - Retrieve all comments"""
        response = self.session.get(f"{self.BASE_URL}/comments")
        assert response.status_code == 200
        
        comments = response.json()
        assert len(comments) == 500, f"Expected 500 comments, got {len(comments)}"
        
        return f"✅ Retrieved {len(comments)} comments (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_get_post_comments(self):
        """Test GET /posts/1/comments - Get comments for specific post"""
        response = self.session.get(f"{self.BASE_URL}/posts/1/comments")
        assert response.status_code == 200
        
        comments = response.json()
        assert len(comments) > 0, "No comments found for post 1"
        
        # Verify all comments belong to post 1
        for comment in comments:
            assert comment['postId'] == 1, f"Comment {comment['id']} doesn't belong to post 1"
        
        return f"✅ Retrieved {len(comments)} comments for post 1 (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_get_albums(self):
        """Test GET /albums - Retrieve all albums"""
        response = self.session.get(f"{self.BASE_URL}/albums")
        assert response.status_code == 200
        
        albums = response.json()
        assert len(albums) == 100, f"Expected 100 albums, got {len(albums)}"
        
        return f"✅ Retrieved {len(albums)} albums (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint - should return 404"""
        response = self.session.get(f"{self.BASE_URL}/nonexistent-endpoint")
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        
        return f"✅ Invalid endpoint correctly returned 404 (Response: {response.elapsed.total_seconds():.3f}s)"
    
    def run_all_tests(self):
        """Run all tests and collect results"""
        self.start_time = datetime.datetime.now()
        
        test_suite = [
            ("GET All Posts", self.test_get_all_posts, "Retrieve all posts from the API"),
            ("GET Single Post", self.test_get_single_post, "Retrieve a specific post by ID"),
            ("POST Create Post", self.test_create_post, "Create a new post via API"),
            ("PUT Update Post", self.test_update_post, "Update an existing post completely"),
            ("PATCH Post", self.test_patch_post, "Partially update a post"),
            ("DELETE Post", self.test_delete_post, "Delete a post from the API"),
            ("GET Users", self.test_get_users, "Retrieve all user profiles"),
            ("GET Comments", self.test_get_comments, "Retrieve all comments"),
            ("GET Post Comments", self.test_get_post_comments, "Get comments for a specific post"),
            ("GET Albums", self.test_get_albums, "Retrieve all photo albums"),
            ("Invalid Endpoint", self.test_invalid_endpoint, "Test error handling for invalid URLs"),
        ]
        
        print("🚀 Starting Enhanced JSONPlaceholder API Test Suite")
        print("=" * 60)
        
        for test_name, test_func, description in test_suite:
            print(f"🔄 Running: {test_name}...")
            self.run_test(test_name, test_func, description)
        
        self.end_time = datetime.datetime.now()
        
        # Generate the beautiful HTML report
        report_path = self.generate_beautiful_html_report()
        
        # Print summary
        passed = sum(1 for result in self.test_results if result['status'] == 'PASSED')
        failed = len(self.test_results) - passed
        total_duration = sum(result['duration'] for result in self.test_results)
        
        print("\n" + "=" * 60)
        print(f"📊 Test Execution Complete!")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️  Total Duration: {total_duration:.2f}s")
        print(f"🎯 Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        print(f"📄 Beautiful Report: {report_path}")
        
        return report_path
    
    def generate_beautiful_html_report(self):
        """Generate a stunning, modern HTML report in html directory"""
        
        # Create html directory if it doesn't exist
        html_dir = 'html'
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
            print(f"📁 Created directory: {html_dir}/")
        
        # Set the output file path
        output_file = os.path.join(html_dir, 'awesome_api_report.html')
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['status'] == 'PASSED')
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        total_duration = sum(result['duration'] for result in self.test_results)
        avg_response_time = total_duration / total_tests if total_tests > 0 else 0
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 API Test Report - JSONPlaceholder</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --success-color: #10b981;
            --danger-color: #ef4444;
            --warning-color: #f59e0b;
            --info-color: #3b82f6;
            --dark-color: #1f2937;
            --light-bg: #f8fafc;
            --white: #ffffff;
            --shadow: 0 10px 25px rgba(0,0,0,0.1);
            --border-radius: 12px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--primary-gradient);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            background: var(--white);
            border-radius: var(--border-radius);
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--primary-gradient);
        }}

        .header h1 {{
            font-size: 3em;
            font-weight: 700;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 1.2em;
            color: #6b7280;
            margin-bottom: 20px;
        }}

        .header .meta {{
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            font-size: 0.9em;
            color: #9ca3af;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: var(--white);
            border-radius: var(--border-radius);
            padding: 30px;
            box-shadow: var(--shadow);
            text-align: center;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}

        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
        }}

        .stat-card.success::before {{ background: var(--success-color); }}
        .stat-card.danger::before {{ background: var(--danger-color); }}
        .stat-card.info::before {{ background: var(--info-color); }}
        .stat-card.warning::before {{ background: var(--warning-color); }}

        .stat-icon {{
            font-size: 2.5em;
            margin-bottom: 15px;
        }}

        .stat-card.success .stat-icon {{ color: var(--success-color); }}
        .stat-card.danger .stat-icon {{ color: var(--danger-color); }}
        .stat-card.info .stat-icon {{ color: var(--info-color); }}
        .stat-card.warning .stat-icon {{ color: var(--warning-color); }}

        .stat-number {{
            font-size: 2.8em;
            font-weight: 700;
            margin-bottom: 5px;
        }}

        .stat-card.success .stat-number {{ color: var(--success-color); }}
        .stat-card.danger .stat-number {{ color: var(--danger-color); }}
        .stat-card.info .stat-number {{ color: var(--info-color); }}
        .stat-card.warning .stat-number {{ color: var(--warning-color); }}

        .stat-label {{
            color: #6b7280;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.85em;
        }}

        .progress-section {{
            background: var(--white);
            border-radius: var(--border-radius);
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: var(--shadow);
        }}

        .progress-header {{
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 20px;
        }}

        .progress-bar {{
            width: 100%;
            height: 12px;
            background: #e5e7eb;
            border-radius: 6px;
            overflow: hidden;
            position: relative;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--success-color), #34d399);
            width: {success_rate}%;
            border-radius: 6px;
            transition: width 2s ease;
            position: relative;
        }}

        .progress-fill::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }}

        @keyframes shimmer {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}

        .tests-section {{
            background: var(--white);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            overflow: hidden;
        }}

        .tests-header {{
            background: var(--light-bg);
            padding: 25px 30px;
            border-bottom: 1px solid #e5e7eb;
        }}

        .tests-header h2 {{
            font-size: 1.5em;
            color: var(--dark-color);
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .test-item {{
            border-bottom: 1px solid #f3f4f6;
            transition: background-color 0.2s ease;
        }}

        .test-item:hover {{
            background: #f9fafb;
        }}

        .test-header {{
            padding: 25px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }}

        .test-info {{
            flex: 1;
        }}

        .test-name {{
            font-size: 1.1em;
            font-weight: 600;
            color: var(--dark-color);
            margin-bottom: 5px;
        }}

        .test-description {{
            color: #6b7280;
            font-size: 0.9em;
        }}

        .test-meta {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}

        .test-duration {{
            color: #6b7280;
            font-size: 0.9em;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .test-status {{
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .status-passed {{
            background: #dcfce7;
            color: #166534;
        }}

        .status-failed {{
            background: #fef2f2;
            color: #991b1b;
        }}

        .test-details {{
            padding: 0 30px 25px;
            background: #f9fafb;
            display: none;
        }}

        .test-details.show {{
            display: block;
        }}

        .details-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .detail-item {{
            background: var(--white);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid var(--info-color);
        }}

        .detail-label {{
            font-size: 0.8em;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }}

        .detail-value {{
            font-weight: 600;
            color: var(--dark-color);
        }}

        .test-result {{
            background: var(--white);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid var(--success-color);
        }}

        .test-result.error {{
            border-left-color: var(--danger-color);
        }}

        .expand-icon {{
            transition: transform 0.3s ease;
            color: #9ca3af;
        }}

        .test-header.expanded .expand-icon {{
            transform: rotate(180deg);
        }}

        .footer {{
            background: var(--white);
            border-radius: var(--border-radius);
            padding: 30px;
            margin-top: 30px;
            text-align: center;
            box-shadow: var(--shadow);
            color: #6b7280;
        }}

        .footer-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}

        .footer-item {{
            text-align: center;
        }}

        .footer-label {{
            font-size: 0.8em;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }}

        .footer-value {{
            font-weight: 600;
            font-size: 1.1em;
        }}

        @media (max-width: 768px) {{
            .header {{
                padding: 25px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .test-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 15px;
            }}
            
            .test-meta {{
                width: 100%;
                justify-content: space-between;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-rocket"></i> API Test Report</h1>
            <div class="subtitle">JSONPlaceholder REST API Test Suite</div>
            <div class="meta">
                <div class="meta-item">
                    <i class="fas fa-calendar"></i>
                    <span>{datetime.datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</span>
                </div>
                <div class="meta-item">
                    <i class="fas fa-code"></i>
                    <span>Python {self.environment_info['python_version']}</span>
                </div>
                <div class="meta-item">
                    <i class="fas fa-server"></i>
                    <span>{self.environment_info['platform']}</span>
                </div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-card info">
                <div class="stat-icon"><i class="fas fa-list-check"></i></div>
                <div class="stat-number">{total_tests}</div>
                <div class="stat-label">Total Tests</div>
            </div>
            <div class="stat-card success">
                <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
                <div class="stat-number">{passed_tests}</div>
                <div class="stat-label">Passed</div>
            </div>
            <div class="stat-card danger">
                <div class="stat-icon"><i class="fas fa-times-circle"></i></div>
                <div class="stat-number">{failed_tests}</div>
                <div class="stat-label">Failed</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-icon"><i class="fas fa-percentage"></i></div>
                <div class="stat-number">{success_rate:.1f}%</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat-card info">
                <div class="stat-icon"><i class="fas fa-clock"></i></div>
                <div class="stat-number">{total_duration:.2f}s</div>
                <div class="stat-label">Total Duration</div>
            </div>
            <div class="stat-card warning">
                <div class="stat-icon"><i class="fas fa-tachometer-alt"></i></div>
                <div class="stat-number">{avg_response_time:.3f}s</div>
                <div class="stat-label">Avg Response</div>
            </div>
        </div>

        <div class="progress-section">
            <div class="progress-header">
                <h3><i class="fas fa-chart-line"></i> Test Progress</h3>
                <span>{success_rate:.1f}% Complete</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill"></div>
            </div>
        </div>

        <div class="tests-section">
            <div class="tests-header">
                <h2><i class="fas fa-flask"></i> Test Results</h2>
            </div>
"""

        for i, result in enumerate(self.test_results):
            status_class = f"status-{result['status'].lower()}"
            icon = "check-circle" if result['status'] == 'PASSED' else "times-circle"
            
            html_content += f"""
            <div class="test-item">
                <div class="test-header" onclick="toggleDetails({i})">
                    <div class="test-info">
                        <div class="test-name">
                            <i class="fas fa-{icon}"></i> {result['name']}
                        </div>
                        <div class="test-description">{result['description']}</div>
                    </div>
                    <div class="test-meta">
                        <div class="test-duration">
                            <i class="fas fa-clock"></i>
                            {result['duration']:.3f}s
                        </div>
                        <div class="test-status {status_class}">
                            {result['status']}
                        </div>
                        <i class="fas fa-chevron-down expand-icon"></i>
                    </div>
                </div>
                <div class="test-details" id="details-{i}">
                    <div class="details-grid">
                        <div class="detail-item">
                            <div class="detail-label">Timestamp</div>
                            <div class="detail-value">{result['timestamp']}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Duration</div>
                            <div class="detail-value">{result['duration']:.3f} seconds</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Status</div>
                            <div class="detail-value">{result['status']}</div>
                        </div>
                        <div class="detail-item">
                            <div class="detail-label">Method</div>
                            <div class="detail-value">{result.get('method', 'API Call')}</div>
                        </div>
                    </div>
                    <div class="test-result{'error' if result['error'] else ''}">
                        <strong>Result:</strong> {result['details']}
"""
            
            if result['error']:
                html_content += f"""
                        <div style="margin-top: 15px; padding: 15px; background: #fef2f2; border-radius: 8px; border-left: 4px solid var(--danger-color);">
                            <strong style="color: var(--danger-color);">Error Details:</strong>
                            <pre style="margin-top: 10px; font-family: monospace; color: #991b1b;">{result['error']}</pre>
                        </div>
"""
            
            html_content += """
                    </div>
                </div>
            </div>
"""

        execution_time = (self.end_time - self.start_time).total_seconds()
        
        html_content += f"""
        </div>

        <div class="footer">
            <div class="footer-grid">
                <div class="footer-item">
                    <div class="footer-label">Execution Time</div>
                    <div class="footer-value">{execution_time:.2f} seconds</div>
                </div>
                <div class="footer-item">
                    <div class="footer-label">API Endpoint</div>
                    <div class="footer-value">JSONPlaceholder</div>
                </div>
                <div class="footer-item">
                    <div class="footer-label">Test Framework</div>
                    <div class="footer-value">Python Requests</div>
                </div>
                <div class="footer-item">
                    <div class="footer-label">Generated By</div>
                    <div class="footer-value">API Test Suite v2.0</div>
                </div>
            </div>
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                <p><i class="fas fa-info-circle"></i> This report was automatically generated by our API testing framework</p>
            </div>
        </div>
    </div>

    <script>
        function toggleDetails(index) {{
            const details = document.getElementById('details-' + index);
            const header = details.previousElementSibling;
            
            if (details.classList.contains('show')) {{
                details.classList.remove('show');
                header.classList.remove('expanded');
            }} else {{
                details.classList.add('show');
                header.classList.add('expanded');
            }}
        }}

        // Auto-expand failed tests on load
        document.addEventListener('DOMContentLoaded', function() {{
            // Add smooth animations
            setTimeout(() => {{
                document.querySelectorAll('.stat-card').forEach((card, index) => {{
                    setTimeout(() => {{
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        card.style.transition = 'all 0.6s ease';
                        
                        setTimeout(() => {{
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }}, 100);
                    }}, index * 100);
                }});
            }}, 100);

            // Auto-expand failed tests
            const failedTests = document.querySelectorAll('.status-failed');
            failedTests.forEach((statusElement) => {{
                const testItem = statusElement.closest('.test-item');
                const header = testItem.querySelector('.test-header');
                const details = testItem.querySelector('.test-details');
                
                if (details && header) {{
                    details.classList.add('show');
                    header.classList.add('expanded');
                }}
            }});

            // Add click animations
            document.querySelectorAll('.test-header').forEach(header => {{
                header.addEventListener('click', function() {{
                    this.style.transform = 'scale(0.99)';
                    setTimeout(() => {{
                        this.style.transform = 'scale(1)';
                    }}, 100);
                }});
            }});
        }});

        // Add some interactive effects
        document.querySelectorAll('.stat-card').forEach(card => {{
            card.addEventListener('mouseenter', function() {{
                this.style.transform = 'translateY(-8px) scale(1.02)';
            }});
            
            card.addEventListener('mouseleave', function() {{
                this.style.transform = 'translateY(0) scale(1)';
            }});
        }});
    </script>
</body>
</html>
"""
        
        # Write the beautiful HTML file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✨ Beautiful HTML report saved to: {output_file}")
        return output_file

def main():
    """Main function to run tests and generate beautiful report"""
    print("🎨 Generating Beautiful API Test Report...")
    generator = BeautifulAPITestReport()
    report_path = generator.run_all_tests()
    
    print("\n🎉 Beautiful report generated successfully!")
    print(f"📂 Open '{report_path}' in your browser to view the stunning report!")
    print(f"💡 Quick open commands:")
    print(f"   Mac: open {report_path}")
    print(f"   Windows: start {report_path}")
    print(f"   Linux: xdg-open {report_path}")

if __name__ == "__main__":
    main()