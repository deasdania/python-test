import subprocess
import sys
import os
import json
from datetime import datetime

def generate_ci_reports():
    """Generate reports suitable for CI/CD pipelines"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Ensure directories exist
    for directory in ["reports/html", "reports/xml", "reports/json"]:
        os.makedirs(directory, exist_ok=True)
    
    reports = {}
    
    print("🔧 Generating CI/CD Reports...")
    
    # Generate JUnit XML for CI systems
    xml_path = f"reports/xml/junit_results_{timestamp}.xml"
    cmd_xml = [
        sys.executable, "-m", "pytest",
        "tests/",
        f"--junitxml={xml_path}",
        "--tb=short"
    ]
    
    print("📊 Generating JUnit XML...")
    result_xml = subprocess.run(cmd_xml)
    reports['junit_xml'] = xml_path if result_xml.returncode == 0 else None
    
    # Generate HTML report
    html_path = f"reports/html/ci_report_{timestamp}.html"
    cmd_html = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--html", html_path,
        "--self-contained-html",
        "--tb=short"
    ]
    
    print("📊 Generating HTML report...")
    result_html = subprocess.run(cmd_html)
    reports['html'] = html_path if result_html.returncode == 0 else None
    
    # Generate JSON report (if pytest-json-report is available)
    json_path = f"reports/json/test_results_{timestamp}.json"
    cmd_json = [
        sys.executable, "-m", "pytest",
        "tests/",
        "--json-report",
        f"--json-report-file={json_path}",
        "--tb=short"
    ]
    
    print("📊 Generating JSON report...")
    try:
        result_json = subprocess.run(cmd_json)
        reports['json'] = json_path if result_json.returncode == 0 else None
    except:
        print("⚠️  JSON report skipped (pytest-json-report not installed)")
        reports['json'] = None
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 CI/CD Report Generation Summary:")
    
    for report_type, path in reports.items():
        if path and os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {report_type.upper()}: {path} ({size:,} bytes)")
        else:
            print(f"❌ {report_type.upper()}: Failed to generate")
    
    # Return overall exit code
    exit_codes = [result_xml.returncode, result_html.returncode]
    return max(exit_codes)

if __name__ == "__main__":
    exit_code = generate_ci_reports()
    sys.exit(exit_code)