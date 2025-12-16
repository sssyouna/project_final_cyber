# SharePy - Secure Version

This is the secure version of SharePy, a file-sharing application with all 15 security misconfigurations fixed.

## Security Fixes Implemented

1. **✅ M1: Admin Password in Clear Text** - Credentials loaded from environment variables
2. **✅ M2: Debug Mode Enabled** - Debug mode disabled in production
3. **✅ M3: Directory Listing Enabled** - Directory listing disabled
4. **✅ M4: Sensitive Files Accessible** - Sensitive files blocked via Nginx rules
5. **✅ M5: pgAdmin/Adminer Publicly Accessible** - Adminer removed from production
6. **✅ M6: MinIO Public Bucket + Keys in Code** - Credentials from environment variables
7. **✅ M7: CORS Wildcard** - Restricted to specific origins
8. **✅ M8: No Security Headers** - Comprehensive security headers implemented
9. **✅ M9: Insecure Cookies** - Secure, HttpOnly, SameSite flags set
10. **✅ M10: Default FastAPI/Uvicorn Banner** - Server version hidden
11. **✅ M11: Verbose Nginx Errors** - Minimal error logging
12. **✅ M12: Internal Ports Exposed** - Services isolated in internal network
13. **✅ M13: chmod 777 on Uploads** - Proper file permissions (750)
14. **✅ M14: /debug/info Endpoint** - Debug endpoint removed
15. **✅ M15: Weak JWT Secret** - Strong JWT secret from environment

## Deployment

1. Copy `.env.example` to `.env` and configure with secure values:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with secure values
   ```

2. Run the deployment script:
   ```bash
   ./deploy_secure.sh
   ```

3. Access the application at: https://localhost

## Security Validation

Run the automated security checker to verify all fixes:
```bash
python3 check_security.py
```

## Key Security Improvements

- **Network Isolation**: Internal services (PostgreSQL, MinIO) not exposed publicly
- **Proper Authentication**: Credentials stored securely, not hardcoded
- **Secure Headers**: Comprehensive security headers to prevent common attacks
- **Input Validation**: Rate limiting and proper error handling
- **File Permissions**: Secure file permissions following principle of least privilege
- **Secrets Management**: All secrets loaded from environment variables
- **Container Security**: Non-root user, minimal attack surface