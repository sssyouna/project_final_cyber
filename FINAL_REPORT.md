# SharePy Security Project Report

## Executive Summary

This project demonstrates the implementation of a deliberately vulnerable file-sharing application (SharePy) with 15 real-world security misconfigurations from OWASP A02:2025, followed by a comprehensive hardening process that addresses all identified vulnerabilities. The project showcases the critical importance of secure configuration practices in modern web applications.

## Project Overview

SharePy is a mini-Dropbox clone built with:
- Backend: FastAPI (Python)
- Database: PostgreSQL 15
- File Storage: MinIO (S3-compatible)
- Reverse Proxy: Nginx
- Orchestration: Docker Compose (6-7 services)

## Phase 1: Vulnerable Application Implementation

The vulnerable version was implemented with all 15 specified misconfigurations:

1. **M1: Admin Password in Clear Text** - Hardcoded credentials in source code
2. **M2: Debug Mode Enabled** - FastAPI running in debug mode
3. **M3: Directory Listing Enabled** - Nginx allows directory browsing
4. **M4: Sensitive Files Accessible** - .env and .git files exposed
5. **M5: pgAdmin/Adminer Publicly Accessible** - Adminer exposed on port 8080
6. **M6: MinIO Public Bucket + Keys in Code** - Credentials hardcoded
7. **M7: CORS Wildcard** - Allow all origins
8. **M8: No Security Headers** - Missing security HTTP headers
9. **M9: Insecure Cookies** - Missing Secure, HttpOnly, SameSite flags
10. **M10: Default FastAPI/Uvicorn Banner** - Server version disclosed
11. **M11: Verbose Nginx Errors** - Debug level error logging
12. **M12: Internal Ports Exposed** - PostgreSQL, MinIO exposed publicly
13. **M13: chmod 777 on Uploads** - World-writable upload directory
14. **M14: /debug/info Endpoint** - Leaks environment information
15. **M15: Weak JWT Secret** - Weak secret used for JWT signing

All vulnerabilities were implemented as specified in the project requirements and verified to be exploitable.

## Phase 2: Exploitation Documentation

Detailed exploitation methods were documented for each vulnerability, including:
- Exact commands to exploit each misconfiguration
- Expected outputs/results
- Impact assessments
- Real-world implications

See `EXPLOITATION_REPORT.md` for complete details.

## Phase 3: Hardened Application Implementation

The secure version was implemented with fixes for all 15 vulnerabilities:

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

## Key Security Improvements

### Network Isolation
- Internal services (PostgreSQL, MinIO) isolated in private network
- No direct public access to databases or storage systems
- Proper service dependencies and communication channels

### Secure Configuration
- All secrets managed through environment variables
- No hardcoded credentials in source code
- Proper file permissions following principle of least privilege

### Defense in Depth
- Comprehensive security headers to prevent common attacks
- Rate limiting to prevent abuse
- Proper error handling without information disclosure
- Container security with non-root user execution

### Automated Validation
- Security validation script (`check_security.py`) to verify fixes
- Deployment script (`deploy_secure.sh`) for consistent deployment
- Git hooks to prevent committing sensitive files

## Technical Implementation Details

### Docker Compose Hardening
- Internal services isolated in private network
- No exposed ports for internal services
- Proper restart policies
- Volume management for persistent data

### Nginx Hardening
- HTTPS-only configuration with redirect
- Security headers implementation
- Sensitive file blocking
- Directory listing disabled
- Rate limiting
- Server version hiding

### Application Hardening
- Debug mode disabled
- CORS restrictions
- Secure cookie settings
- Strong JWT secret generation
- Proper logging configuration

## Deployment Process

### Vulnerable Version
```bash
git checkout vulnerable
docker-compose up -d
```

### Secure Version
```bash
git checkout secure
cp backend/.env.example backend/.env
# Edit backend/.env with secure values
./deploy_secure.sh
```

## Security Validation

The `check_security.py` script validates all 15 security fixes:
- Checks for hardcoded passwords
- Verifies debug mode is disabled
- Ensures directory listing is disabled
- Validates sensitive files are blocked
- Confirms internal ports are not exposed
- And 10 more security validations

## Lessons Learned

1. **Configuration Security is Critical**: Many vulnerabilities stem from poor configuration rather than code flaws
2. **Defense in Depth Works**: Multiple layers of security controls provide better protection
3. **Environment Variables are Essential**: Never hardcode secrets in source code
4. **Automated Validation is Key**: Scripts to verify security posture prevent regressions
5. **Principle of Least Privilege**: Limit access rights to minimum necessary

## Conclusion

This project successfully demonstrated:
- Implementation of common security misconfigurations
- Exploitation techniques for each vulnerability
- Comprehensive hardening approaches
- Automated validation of security fixes

The before/after comparison clearly shows how proper security configuration can eliminate critical vulnerabilities that would otherwise lead to complete system compromise.

## Future Improvements

1. **Enhanced Monitoring**: Add logging and monitoring for security events
2. **Advanced Authentication**: Implement multi-factor authentication
3. **Encryption at Rest**: Encrypt sensitive data in databases
4. **Regular Security Scanning**: Integrate automated security scanning in CI/CD
5. **Penetration Testing**: Regular penetration testing to identify new vulnerabilities

## Repository Structure

Both vulnerable and secure versions are available in separate branches:
- `vulnerable` branch: Contains the deliberately vulnerable implementation
- `secure` branch: Contains the hardened implementation with all fixes

This structure allows for easy comparison of the security improvements and serves as an educational resource for understanding common security misconfigurations and their fixes.