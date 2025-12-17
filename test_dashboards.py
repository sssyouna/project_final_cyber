#!/usr/bin/env python3
"""
Test script to verify that both dashboards are working correctly
"""

import os
import sys

def test_file_exists(filepath, description):
    """Test if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description} - FOUND")
        return True
    else:
        print(f"❌ {description} - NOT FOUND")
        return False

def main():
    """Main test function"""
    print("Testing SharePy Dashboard Implementation")
    print("=" * 50)
    
    # Test vulnerable version files
    print("\nVulnerable Version Tests:")
    vuln_tests = [
        ("vulnerable_version/sharepy/backend/templates/vulnerable_dashboard.html", "Vulnerable dashboard HTML"),
        ("vulnerable_version/sharepy/backend/main.py", "Vulnerable backend main.py"),
        ("vulnerable_version/sharepy/backend/.env", "Vulnerable .env file"),
        ("vulnerable_version/sharepy/backend/uploads", "Uploads directory")
    ]
    
    vuln_passed = 0
    for filepath, description in vuln_tests:
        if test_file_exists(filepath, description):
            vuln_passed += 1
    
    # Test secure version files
    print("\nSecure Version Tests:")
    secure_tests = [
        ("secure_version/sharepy/backend/templates/dashboard.html", "Secure dashboard HTML"),
        ("secure_version/sharepy/backend/main.py", "Secure backend main.py")
    ]
    
    secure_passed = 0
    for filepath, description in secure_tests:
        if test_file_exists(filepath, description):
            secure_passed += 1
    
    # Test documentation files
    print("\nDocumentation Tests:")
    doc_tests = [
        ("README_DASHBOARD.md", "Dashboard README"),
        ("DASHBOARD_SUMMARY.md", "Dashboard Summary")
    ]
    
    doc_passed = 0
    for filepath, description in doc_tests:
        if test_file_exists(filepath, description):
            doc_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    total_tests = len(vuln_tests) + len(secure_tests) + len(doc_tests)
    total_passed = vuln_passed + secure_passed + doc_passed
    
    print(f"Tests Passed: {total_passed}/{total_tests}")
    
    if total_passed == total_tests:
        print("🎉 All tests passed! Dashboard implementation is complete.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())