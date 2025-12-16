# SharePy - Secure Version (Local)

This is the secure version of SharePy with all 15 security misconfigurations fixed.

## How to Run

1. Navigate to the sharepy directory:
   ```bash
   cd sharepy
   ```

2. Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   # Edit .env with secure values
   ```

3. Start the application:
   ```bash
   ./deploy_secure.sh
   ```

   Or manually:
   ```bash
   docker-compose up -d
   ```

4. Access the application at: https://localhost

## What You'll See

This version has all security fixes implemented:
- Credentials from environment variables
- Debug mode disabled
- Directory listing disabled
- Sensitive files blocked
- Adminer removed
- CORS restrictions
- Comprehensive security headers
- Secure cookies
- Minimal error logging
- Internal services isolated
- Proper file permissions
- Debug endpoints removed
- Strong JWT secrets

## Security Validation

Run the automated security checker:
```bash
python3 check_security.py
```

This will validate that all 15 security fixes have been properly implemented.