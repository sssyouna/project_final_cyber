#!/bin/bash

# CORS Wildcard (Access-Control-Allow-Origin: *) Checker
# This script checks if a web application has a CORS wildcard vulnerability

# Check if URL argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <URL> [custom-origin]"
    echo "Example: $0 http://localhost:8000"
    echo "Example: $0 http://localhost:8000 https://evil.com"
    exit 1
fi

TARGET_URL="$1"
CUSTOM_ORIGIN="${2:-https://evil.com}"

echo "🔍 Checking CORS configuration for: $TARGET_URL"
echo "Using Origin header: $CUSTOM_ORIGIN"
echo "----------------------------------------"

# Send OPTIONS request to check CORS headers
echo "Sending OPTIONS request..."
OPTIONS_RESPONSE=$(curl -s -D - -X OPTIONS \
    -H "Origin: $CUSTOM_ORIGIN" \
    -H "Access-Control-Request-Method: GET" \
    -H "Access-Control-Request-Headers: X-Requested-With" \
    --max-time 10 \
    "$TARGET_URL" -o /dev/null)

# Extract CORS headers
ACAO_HEADER=$(echo "$OPTIONS_RESPONSE" | grep -i "Access-Control-Allow-Origin:" | head -n 1 | cut -d: -f2- | xargs)
ACAC_HEADER=$(echo "$OPTIONS_RESPONSE" | grep -i "Access-Control-Allow-Credentials:" | head -n 1 | cut -d: -f2- | xargs)

echo "OPTIONS Access-Control-Allow-Origin: $ACAO_HEADER"
echo "OPTIONS Access-Control-Allow-Credentials: $ACAC_HEADER"

# Check if ACAO is wildcard
if [ "$ACAO_HEADER" = "*" ]; then
    if [ "$ACAC_HEADER" = "true" ]; then
        echo ""
        echo "🚨 VULNERABLE: CORS Wildcard with Credentials Detected!"
        echo "   This allows any website to make authenticated requests to this API"
        exit 1
    else
        echo ""
        echo "⚠️  WARNING: CORS Wildcard Detected (Less Critical)"
        echo "   This allows any website to make requests to this API, but without credentials"
        exit 1
    fi
else
    echo ""
    echo "✅ SECURE: No CORS Wildcard Detected"
    echo "   The API properly restricts cross-origin requests"
    exit 0
fi