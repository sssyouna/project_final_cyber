# SharePy - Vulnerable Version (Local)

This is the vulnerable version of SharePy that you can run locally to see the security misconfigurations in action.

## How to Run

1. Navigate to the sharepy directory:
   ```bash
   cd sharepy
   ```

2. Start the application:
   ```bash
   docker-compose up -d
   ```

3. Access the application at: http://localhost

## What You'll See

This version contains all 15 security misconfigurations:
- Hardcoded credentials in source code
- Debug mode enabled
- Directory listing enabled
- Sensitive files exposed
- Adminer publicly accessible
- CORS wildcard
- Missing security headers
- Insecure cookies
- Verbose error logging
- Internal ports exposed
- World-writable directories
- Debug endpoints
- Weak JWT secrets

## Warning

⚠️ This version is intentionally insecure and should only be used for educational purposes in a controlled environment.