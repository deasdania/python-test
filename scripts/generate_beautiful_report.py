import sys
import os
from pathlib import Path
import subprocess
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Try to import the existing beautiful report generator
try:
    from beautiful_api_report import BeautifulAPITestReport
    HAS_BEAUTIFUL_GENERATOR = True
except ImportError:
    HAS_BEAUTIFUL_GENERATOR = False

def ensure_directories():
    """Ensure report directories exist"""
    directories = [
        "reports",
        "reports/html",
        "reports/json", 
        "reports/xml",
        "reports/coverage"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def generate_pytest_html_report(test_path="tests/", report_name=None):
    """Generate HTML report using pytest-html"""
    
    if report_name is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_name = f"pytest_report_{timestamp}.html"
    
    report_path = f"reports/html/{report_name}"
    
    print(f"📊 Generating pytest HTML report...")
    print(f"🎯 Test path: {test_path}")
    print(f"📄 Report: {report_path}")
    
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v",
        "--html", report_path,
        "--self-contained-html",
        "--tb=short",
        f"--html-title=API Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"✅ HTML report generated: {report_path}")
    else:
        print(f"❌ Report generation failed (exit code: {result.returncode})")
    
    return result.returncode, report_path

def generate_json_report(test_path="tests/", report_name=None):
    """Generate JSON report for programmatic access"""
    
    if report_name is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_name = f"test_results_{timestamp}.json"
    
    report_path = f"reports/json/{report_name}"
    
    print(f"📊 Generating JSON report...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v",
        "--json-report",
        f"--json-report-file={report_path}",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"✅ JSON report generated: {report_path}")
    else:
        print(f"❌ JSON report generation failed")
    
    return result.returncode, report_path

def generate_junit_xml_report(test_path="tests/", report_name=None):
    """Generate JUnit XML report for CI/CD integration"""
    
    if report_name is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_name = f"junit_results_{timestamp}.xml"
    
    report_path = f"reports/xml/{report_name}"
    
    print(f"📊 Generating JUnit XML report...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v",
        f"--junitxml={report_path}",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"✅ JUnit XML report generated: {report_path}")
    else:
        print(f"❌ JUnit XML report generation failed")
    
    return result.returncode, report_path

def generate_coverage_report(test_path="tests/"):
    """Generate coverage report"""
    
    print(f"📊 Generating coverage report...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        test_path,
        "-v",
        "--cov=tests",
        "--cov-report=html:reports/coverage",
        "--cov-report=term",
        "--cov-report=xml:reports/coverage/coverage.xml",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"✅ Coverage report generated: reports/coverage/index.html")
    else:
        print(f"❌ Coverage report generation failed")
    
    return result.returncode, "reports/coverage/index.html"

def generate_beautiful_custom_report():
    """Generate beautiful custom report using existing generator"""
    
    if not HAS_BEAUTIFUL_GENERATOR:
        print("❌ Beautiful report generator not found!")
        print("💡 Make sure beautiful_api_report.py exists in the project root")
        return 1, None
    
    print(f"🎨 Generating beautiful custom report...")
    
    try:
        generator = BeautifulAPITestReport()
        generator.run_all_tests()
        
        # The report should be in html/awesome_api_report.html
        report_path = "html/awesome_api_report.html"
        if os.path.exists(report_path):
            print(f"✅ Beautiful custom report generated: {report_path}")
            return 0, report_path
        else:
            print(f"❌ Report file not found after generation")
            return 1, None
            
    except Exception as e:
        print(f"❌ Error generating beautiful report: {e}")
        return 1, None

def generate_comprehensive_report_suite(test_path="tests/"):
    """Generate all types of reports"""
    
    print("🚀 Generating Comprehensive Report Suite")
    print("=" * 50)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    reports = {}
    
    # Generate HTML report
    exit_code, html_report = generate_pytest_html_report(test_path, f"comprehensive_html_{timestamp}.html")
    reports['html'] = html_report if exit_code == 0 else None
    
    # Generate JSON report  
    exit_code, json_report = generate_json_report(test_path, f"comprehensive_json_{timestamp}.json")
    reports['json'] = json_report if exit_code == 0 else None
    
    # Generate JUnit XML
    exit_code, xml_report = generate_junit_xml_report(test_path, f"comprehensive_junit_{timestamp}.xml")
    reports['xml'] = xml_report if exit_code == 0 else None
    
    # Generate coverage report
    exit_code, coverage_report = generate_coverage_report(test_path)
    reports['coverage'] = coverage_report if exit_code == 0 else None
    
    # Generate beautiful custom report
    exit_code, beautiful_report = generate_beautiful_custom_report()
    reports['beautiful'] = beautiful_report if exit_code == 0 else None
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Report Generation Summary:")
    
    for report_type, path in reports.items():
        if path:
            print(f"✅ {report_type.upper()}: {path}")
        else:
            print(f"❌ {report_type.upper()}: Failed to generate")
    
    return reports

def open_reports_in_browser(reports):
    """Open generated reports in browser"""
    import webbrowser
    
    html_reports = []
    
    if reports.get('html'):
        html_reports.append(('HTML Report', reports['html']))
    
    if reports.get('coverage'):
        html_reports.append(('Coverage Report', reports['coverage']))
    
    if reports.get('beautiful'):
        html_reports.append(('Beautiful Report', reports['beautiful']))
    
    if not html_reports:
        print("❌ No HTML reports available to open")
        return
    
    print(f"\n🌐 Opening {len(html_reports)} reports in browser...")
    
    for name, path in html_reports:
        try:
            full_path = os.path.abspath(path)
            webbrowser.open(f"file://{full_path}")
            print(f"✅ Opened {name}: {path}")
        except Exception as e:
            print(f"❌ Could not open {name}: {e}")

def interactive_report_generator():
    """Interactive report generation"""
    
    print("🎨 Interactive Report Generator")
    print("=" * 35)
    
    while True:
        print("\nChoose report type:")
        print("1. 📊 HTML Report (pytest-html)")
        print("2. 📋 JSON Report (machine readable)")
        print("3. 🔧 JUnit XML Report (CI/CD)")
        print("4. 📈 Coverage Report")
        print("5. 🎨 Beautiful Custom Report")
        print("6. 🚀 All Reports (comprehensive)")
        print("7. 🌐 Open existing reports")
        print("8. ❌ Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            test_path = input("Test path (default: tests/): ").strip() or "tests/"
            generate_pytest_html_report(test_path)
            
        elif choice == '2':
            test_path = input("Test path (default: tests/): ").strip() or "tests/"
            generate_json_report(test_path)
            
        elif choice == '3':
            test_path = input("Test path (default: tests/): ").strip() or "tests/"
            generate_junit_xml_report(test_path)
            
        elif choice == '4':
            test_path = input("Test path (default: tests/): ").strip() or "tests/"
            generate_coverage_report(test_path)
            
        elif choice == '5':
            generate_beautiful_custom_report()
            
        elif choice == '6':
            test_path = input("Test path (default: tests/): ").strip() or "tests/"
            reports = generate_comprehensive_report_suite(test_path)
            
            open_browser = input("\n🌐 Open reports in browser? (y/n): ").lower().startswith('y')
            if open_browser:
                open_reports_in_browser(reports)
                
        elif choice == '7':
            list_existing_reports()
            
        elif choice == '8':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

def list_existing_reports():
    """List all existing reports"""
    
    print("\n📋 Existing Reports:")
    
    report_dirs = [
        ("HTML Reports", "reports/html"),
        ("JSON Reports", "reports/json"),
        ("XML Reports", "reports/xml"),
        ("Coverage Reports", "reports/coverage"),
        ("Beautiful Reports", "html")
    ]
    
    for category, directory in report_dirs:
        print(f"\n🔹 {category}:")
        if os.path.exists(directory):
            files = [f for f in os.listdir(directory) if f.endswith(('.html', '.json', '.xml'))]
            if files:
                for file in sorted(files, reverse=True)[:5]:  # Show last 5
                    file_path = os.path.join(directory, file)
                    size = os.path.getsize(file_path)
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    print(f"   📄 {file} ({size:,} bytes, {mtime.strftime('%Y-%m-%d %H:%M')})")
            else:
                print("   (no reports found)")
        else:
            print("   (directory not found)")

def main():
    """Main function"""
    
    print("🎨 API Test Report Generator")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('tests'):
        print("❌ Error: 'tests' directory not found!")
        print("💡 Make sure you're running this script from the project root directory")
        sys.exit(1)
    
    # Ensure directories exist
    ensure_directories()
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        # No arguments provided, run in interactive mode
        interactive_report_generator()
        return
    
    report_type = sys.argv[1].lower()
    test_path = sys.argv[2] if len(sys.argv) > 2 else "tests/"
    
    if report_type == 'html':
        generate_pytest_html_report(test_path)
    elif report_type == 'json':
        generate_json_report(test_path)
    elif report_type == 'xml':
        generate_junit_xml_report(test_path)
    elif report_type == 'coverage':
        generate_coverage_report(test_path)
    elif report_type == 'beautiful':
        generate_beautiful_custom_report()
    elif report_type == 'all':
        reports = generate_comprehensive_report_suite(test_path)
        open_reports_in_browser(reports)
    elif report_type == 'list':
        list_existing_reports()
    elif report_type == 'interactive':
        interactive_report_generator()
    else:
        print(f"❌ Unknown report type: {report_type}")
        print("✅ Valid types: html, json, xml, coverage, beautiful, all, list, interactive")
        print("\n💡 Usage examples:")
        print(f"   python {sys.argv[0]} html")
        print(f"   python {sys.argv[0]} all")
        print(f"   python {sys.argv[0]} beautiful")
        print(f"   python {sys.argv[0]} interactive")
        sys.exit(1)

if __name__ == "__main__":
    main()