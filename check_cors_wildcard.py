#!/usr/bin/env python3
"""
CORS Wildcard (Access-Control-Allow-Origin: *) Checker
This script checks if a web application has a CORS wildcard vulnerability
"""
import requests
import sys
import argparse
from urllib.parse import urlparse

def check_cors_wildcard(target_url, custom_origin=None):
    """
    Check if the target URL has a CORS wildcard vulnerability
    
    Args:
        target_url (str): The URL to test
        custom_origin (str): Custom origin to test with (default: https://evil.com)
    
    Returns:
        dict: Results of the CORS check
    """
    if not custom_origin:
        custom_origin = "https://evil.com"
    
    try:
        # Make an OPTIONS request to check CORS headers
        headers = {
            "Origin": custom_origin,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Requested-With"
        }
        
        # Test the target URL with a simple endpoint
        response = requests.options(target_url, headers=headers, timeout=10)
        
        # Get the Access-Control-Allow-Origin header
        cors_origin = response.headers.get("Access-Control-Allow-Origin")
        cors_credentials = response.headers.get("Access-Control-Allow-Credentials")
        
        # Check for wildcard vulnerability
        is_wildcard = cors_origin == "*"
        is_wildcard_with_credentials = cors_origin == "*" and cors_credentials == "true"
        
        # Also test a regular GET request to see if the header is present
        get_response = requests.get(target_url, headers={"Origin": custom_origin}, timeout=10)
        get_cors_origin = get_response.headers.get("Access-Control-Allow-Origin")
        get_is_wildcard = get_cors_origin == "*"
        
        results = {
            "target_url": target_url,
            "options_cors_header": cors_origin,
            "options_credentials": cors_credentials,
            "get_cors_header": get_cors_origin,
            "has_wildcard": is_wildcard or get_is_wildcard,
            "has_wildcard_with_credentials": is_wildcard_with_credentials,
            "vulnerable": is_wildcard_with_credentials  # This is the most dangerous scenario
        }
        
        return results
        
    except requests.exceptions.RequestException as e:
        return {
            "target_url": target_url,
            "error": str(e),
            "has_wildcard": False,
            "vulnerable": False
        }

def print_results(results):
    """Print the CORS check results in a readable format"""
    print(f"\n🔍 CORS Analysis for: {results['target_url']}")
    print("-" * 50)
    
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return
    
    print(f"OPTIONS Access-Control-Allow-Origin: {results['options_cors_header']}")
    print(f"OPTIONS Access-Control-Allow-Credentials: {results['options_credentials']}")
    print(f"GET Access-Control-Allow-Origin: {results['get_cors_header']}")
    
    if results['vulnerable']:
        print("\n🚨 VULNERABLE: CORS Wildcard with Credentials Detected!")
        print("   This allows any website to make authenticated requests to this API")
    elif results['has_wildcard']:
        print("\n⚠️  WARNING: CORS Wildcard Detected (Less Critical)")
        print("   This allows any website to make requests to this API, but without credentials")
    else:
        print("\n✅ SECURE: No CORS Wildcard Detected")
        print("   The API properly restricts cross-origin requests")

def main():
    parser = argparse.ArgumentParser(description="Check for CORS wildcard vulnerability (Access-Control-Allow-Origin: *)")
    parser.add_argument("url", nargs="?", help="Target URL to test for CORS vulnerability")
    parser.add_argument("--origin", default="https://evil.com", 
                       help="Custom origin to test with (default: https://evil.com)")
    parser.add_argument("--file", help="File containing multiple URLs to test (one per line)")
    
    args = parser.parse_args()
    
    if not args.url and not args.file:
        print("Usage: python check_cors_wildcard.py <URL> [--origin CUSTOM_ORIGIN]")
        print("   Or: python check_cors_wildcard.py --file urls.txt")
        sys.exit(1)
    
    urls_to_test = []
    
    if args.file:
        try:
            with open(args.file, 'r') as f:
                urls_to_test = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print(f"Error: File {args.file} not found")
            sys.exit(1)
    else:
        urls_to_test = [args.url]
    
    vulnerable_count = 0
    
    for url in urls_to_test:
        # Ensure the URL has a scheme
        if not urlparse(url).scheme:
            url = "http://" + url
            
        results = check_cors_wildcard(url, args.origin)
        print_results(results)
        
        if results.get('vulnerable', False) or results.get('has_wildcard', False):
            vulnerable_count += 1
    
    if len(urls_to_test) > 1:
        print(f"\n📊 Summary: {vulnerable_count}/{len(urls_to_test)} URLs are vulnerable to CORS wildcard issues")

if __name__ == "__main__":
    main()