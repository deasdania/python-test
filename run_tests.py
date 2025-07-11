
import subprocess
import sys
import os
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def run_beautiful_report():
    """Run the beautiful API test report generator"""
    if not check_dependencies():
        return False
    
    try:
        print("🚀 Starting API Test Suite...")
        print("=" * 50)
        
        # Import and run the test generator
        from beautiful_api_report import BeautifulAPITestReport
        
        generator = BeautifulAPITestReport()
        report_path = generator.run_all_tests()
        
        print("\n" + "=" * 50)
        print("🎉 Test execution completed successfully!")
        print(f"📊 Report saved to: {report_path}")
        
        # Ask if user wants to open the report
        if input("\n🌐 Open report in browser? (y/n): ").lower().startswith('y'):
            try:
                webbrowser.open(f"file://{os.path.abspath(report_path)}")
                print("🔗 Report opened in your default browser!")
            except Exception as e:
                print(f"❌ Could not open browser automatically: {e}")
                print(f"💡 Manually open: {os.path.abspath(report_path)}")
        
        return True
        
    except ImportError:
        print("❌ Could not import test generator.")
        print("💡 Make sure 'beautiful_api_report.py' is in the same directory.")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main function"""
    print("🎨 API Test Report Generator")
    print("=" * 30)
    
    # Check current directory
    current_files = [f for f in os.listdir('.') if f.endswith('.py')]
    print(f"📂 Found Python files: {', '.join(current_files)}")
    
    if 'beautiful_api_report.py' not in current_files:
        print("\n❌ 'beautiful_api_report.py' not found in current directory!")
        print("💡 Make sure you have saved the beautiful report generator script.")
        return
    
    # Run the tests
    success = run_beautiful_report()
    
    if success:
        print("\n✨ All done! Check your html/ directory for the report.")
    else:
        print("\n❌ Test execution failed. Please check the errors above.")

if __name__ == "__main__":
    main()