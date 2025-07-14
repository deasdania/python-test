import subprocess
import sys
import os
from datetime import datetime

def generate_quick_report():
    """Generate a quick, beautiful HTML report"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f"reports/html/quick_report_{timestamp}.html"
    
    # Ensure directory exists
    os.makedirs("reports/html", exist_ok=True)
    
    print("🚀 Generating Quick Test Report...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--html", report_path,
        "--self-contained-html",
        "--tb=short",
        f"--html-title=Quick API Test Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print(f"✅ Quick report generated: {report_path}")
        
        # Try to open in browser
        try:
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
            print(f"🌐 Opened in browser!")
        except:
            print(f"💡 Manually open: {os.path.abspath(report_path)}")
    else:
        print(f"❌ Report generation failed")
    
    return result.returncode

if __name__ == "__main__":
    generate_quick_report()