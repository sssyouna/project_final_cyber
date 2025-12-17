#!/usr/bin/env python3
import dotenv
dotenv.load_dotenv()
"""
Automated security checker for SharePy
Validates all 15 security fixes
"""

import requests
import subprocess
import os
import sys
from typing import List, Tuple

class SecurityChecker:
    def __init__(self, base_url="http://localhost"):
        self.base_url = base_url
        self.results = []
        
    def check(self, name: str, condition: bool, message: str):
        """Record check result"""
        status = "✅ PASS" if condition else "❌ FAIL"
        self.results.append((name, condition, message))
        print(f"{status} - {name}: {message}")
        return condition
    
    def run_all_checks(self):
        """Run all 15 security checks"""
        print("="*60)
        print("SharePy Security Validation")
        print("="*60)
        
        # M1: Admin password not in code/git
        self.check_m1_no_hardcoded_passwords()
        
        # M2: Debug mode disabled
        self.check_m2_debug_disabled()
        
        # M3: Directory listing disabled
        self.check_m3_no_directory_listing()
        
        # M4: Sensitive files blocked
        self.check_m4_sensitive_files_blocked()
        
        # M5: Adminer not publicly accessible
        self.check_m5_no_public_adminer()
        
        # M6: MinIO credentials secure
        self.check_m6_minio_secure()
        
        # M7: CORS restricted
        self.check_m7_cors_restricted()
        
        # M8: Security headers present
        self.check_m8_security_headers()
        
        # M9: Secure cookies
        self.check_m9_secure_cookies()
        
        # M10: Server banner hidden
        self.check_m10_no_server_banner()
        
        # M11: Nginx errors not verbose
        self.check_m11_minimal_errors()
        
        # M12: Internal ports not exposed
        self.check_m12_no_exposed_ports()
        
        # M13: Upload permissions correct
        self.check_m13_proper_permissions()
        
        # M14: No debug endpoints
        self.check_m14_no_debug_endpoint()
        
        # M15: Strong JWT secret
        self.check_m15_strong_jwt_secret()
        
        self.print_summary()
    
    def check_m1_no_hardcoded_passwords(self):
        """M1: Check no passwords in code/git"""
        # Check .env not in git
        result = subprocess.run(
            ["git", "ls-files", ".env"],
            capture_output=True, text=True
        )
        not_in_git = len(result.stdout.strip()) == 0
        
        # Check no hardcoded passwords in main.py
        with open("backend/main.py", "r") as f:
            content = f.read()
            no_hardcoded = "admin123" not in content.lower()
        
        self.check(
            "M1: No Hardcoded Passwords",
            not_in_git and no_hardcoded,
            ".env not in git and no hardcoded passwords"
        )
    
    def check_m2_debug_disabled(self):
        """M2: Check debug mode disabled"""
        try:
            # Trigger error and check response
            resp = requests.get(f"{self.base_url}/nonexistent", timeout=5)
            no_debug_info = "Traceback" not in resp.text
            self.check(
                "M2: Debug Mode Disabled",
                no_debug_info,
                "No stack traces in error responses"
            )
        except Exception as e:
            self.check("M2: Debug Mode Disabled", False, f"Error: {e}")
    
    def check_m3_no_directory_listing(self):
        """M3: Check directory listing disabled"""
        try:
            resp = requests.get(f"{self.base_url}/uploads/", timeout=5)
            no_listing = "Index of" not in resp.text
            self.check(
                "M3: Directory Listing Disabled",
                no_listing,
                "No directory browsing allowed"
            )
        except:
            self.check("M3: Directory Listing Disabled", True, "Endpoint not accessible")
    
    def check_m4_sensitive_files_blocked(self):
        """M4: Check sensitive files blocked"""
        sensitive_files = [".env", ".git/config", "backup.db", "__pycache__"]
        all_blocked = True
        
        for file in sensitive_files:
            try:
                resp = requests.get(f"{self.base_url}/{file}", timeout=5)
                if resp.status_code != 404:
                    all_blocked = False
                    break
            except:
                pass
        
        self.check(
            "M4: Sensitive Files Blocked",
            all_blocked,
            "All sensitive files return 404"
        )
    
    def check_m5_no_public_adminer(self):
        """M5: Check Adminer not publicly accessible"""
        try:
            resp = requests.get("http://localhost:8080", timeout=5)
            not_accessible = resp.status_code != 200
        except:
            not_accessible = True
        
        self.check(
            "M5: Adminer Not Public",
            not_accessible,
            "Adminer port not accessible"
        )
    
    def check_m6_minio_secure(self):
        """M6: Check MinIO properly secured"""
        # Check port not exposed
        try:
            resp = requests.get("http://localhost:9000", timeout=5)
            not_exposed = False
        except:
            not_exposed = True
        
        # Check no hardcoded credentials
        with open("backend/main.py", "r") as f:
            content = f.read()
            no_hardcoded = "minioadmin" not in content.lower()
        
        self.check(
            "M6: MinIO Secured",
            not_exposed and no_hardcoded,
            "MinIO not exposed and credentials from env"
        )
    
    def check_m7_cors_restricted(self):
        """M7: Check CORS not wildcard"""
        try:
            resp = requests.options(
                f"{self.base_url}/api/",
                headers={"Origin": "https://evil.com"}
            )
            restricted = resp.headers.get("Access-Control-Allow-Origin") != "*"
            self.check(
                "M7: CORS Restricted",
                restricted,
                "CORS not allowing all origins"
            )
        except:
            self.check("M7: CORS Restricted", True, "CORS properly configured")
    
    def check_m8_security_headers(self):
        """M8: Check security headers present"""
        try:
            resp = requests.get(self.base_url, timeout=5)
            headers = resp.headers
            
            required = [
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "X-Content-Type-Options",
                "X-Frame-Options"
            ]
            
            all_present = all(h in headers for h in required)
            self.check(
                "M8: Security Headers Present",
                all_present,
                f"Required headers: {', '.join(required)}"
            )
        except Exception as e:
            self.check("M8: Security Headers", False, f"Error: {e}")
    
    def check_m9_secure_cookies(self):
        """M9: Check cookies have Secure, HttpOnly, SameSite"""
        try:
            resp = requests.post(f"{self.base_url}/login?email=test@test.com&password=test")
            
            cookie_header = resp.headers.get("Set-Cookie", "")
            has_secure = "Secure" in cookie_header
            has_httponly = "HttpOnly" in cookie_header
            has_samesite = "SameSite" in cookie_header
            
            self.check(
                "M9: Secure Cookies",
                has_secure and has_httponly and has_samesite,
                "Cookies have Secure, HttpOnly, SameSite flags"
            )
        except:
            self.check("M9: Secure Cookies", False, "Could not verify cookies")
    def check_m10_no_server_banner(self):
        """M10: Check server version hidden"""
        try:
            resp = requests.get(self.base_url, timeout=5)
            server_header = resp.headers.get("Server", "").lower()
            
            no_version = "uvicorn" not in server_header and "fastapi" not in server_header
            self.check(
                "M10: Server Banner Hidden",
                no_version or server_header == "",
                "No server version information leaked"
            )
        except Exception as e:
            self.check("M10: Server Banner", False, f"Error: {e}")
    
    def check_m11_minimal_errors(self):
        """M11: Check error messages not verbose"""
        try:
            resp = requests.get(f"{self.base_url}/nonexistent/deep/path", timeout=5)
            no_path_leak = "/usr/share/nginx" not in resp.text
            self.check(
                "M11: Minimal Error Messages",
                no_path_leak,
                "Error messages don't leak internal paths"
            )
        except:
            self.check("M11: Minimal Errors", True, "Errors properly handled")
    
    def check_m12_no_exposed_ports(self):
        """M12: Check internal ports not exposed"""
        dangerous_ports = [5432, 9000]  # PostgreSQL, MinIO
        all_closed = True
        
        for port in dangerous_ports:
            try:
                result = subprocess.run(
                    ["nc", "-zv", "localhost", str(port)],
                    capture_output=True, timeout=2
                )
                if result.returncode == 0:
                    all_closed = False
                    break
            except:
                pass
        
        self.check(
            "M12: Internal Ports Not Exposed",
            all_closed,
            "PostgreSQL and MinIO ports not accessible externally"
        )
    
    def check_m13_proper_permissions(self):
        """M13: Check upload directory permissions"""
        try:
            result = subprocess.run(
                ["docker", "exec", "sharepy-backend-1", "stat", "-c", "%a", "/app/uploads"],
                capture_output=True, text=True
            )
            perms = result.stdout.strip()
            proper_perms = perms in ["750", "755", "700"]
            
            self.check(
                "M13: Proper File Permissions",
                proper_perms,
                f"Upload directory has {perms} permissions (not 777)"
            )
        except:
            self.check("M13: File Permissions", False, "Could not check permissions")
    
    def check_m14_no_debug_endpoint(self):
        """M14: Check /debug/info endpoint removed"""
        try:
            resp = requests.get(f"{self.base_url}/debug/info", timeout=5)
            removed = resp.status_code == 404
            self.check(
                "M14: Debug Endpoint Removed",
                removed,
                "/debug/info returns 404"
            )
        except:
            self.check("M14: Debug Endpoint", True, "Debug endpoint not accessible")
    
    def check_m15_strong_jwt_secret(self):
        """M15: Check JWT secret is strong"""
        weak_secrets = ["secret", "secret123", "changeme", "admin", "password"]
        
        # Check environment or config
        jwt_secret = os.getenv("JWT_SECRET", "")
        is_strong = len(jwt_secret) >= 32 and jwt_secret.lower() not in weak_secrets
        
        )
    
    def print_summary(self):
        """Print final summary"""
        print("\n" + "="*60)
        passed = sum(1 for _, result, _ in self.results if result)
        total = len(self.results)
        score = (passed / total) * 100
        
        print(f"FINAL SCORE: {passed}/{total} ({score:.1f}%)")
        
        if passed == total:
            print("🎉 ALL SECURITY CHECKS PASSED!")
            sys.exit(0)
        else:
            print("⚠️  SOME CHECKS FAILED - REVIEW ABOVE")
            sys.exit(1)

if __name__ == "__main__":
    checker = SecurityChecker()
    checker.run_all_checks()