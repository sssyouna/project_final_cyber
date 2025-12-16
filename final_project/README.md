# SharePy Security Project

This project demonstrates the implementation of a deliberately vulnerable file-sharing application (SharePy) with 15 real-world security misconfigurations from OWASP A02:2025, followed by a comprehensive hardening process that addresses all identified vulnerabilities.

## Project Structure

```
final_project/
├── vulnerable/          # Vulnerable version with all 15 security misconfigurations
│   ├── sharepy/         # Main application files
│   ├── README.md        # Instructions for running vulnerable version
│   ├── VULNERABILITY_REPORT.md
│   ├── EXPLOITATION_REPORT.md
│   └── REMEDIATION_REPORT.md
└── secure/             # Hardened version with all vulnerabilities fixed
    ├── sharepy/         # Main application files
    ├── README.md        # Instructions for running secure version
    ├── VULNERABILITY_REPORT.md
    ├── EXPLOITATION_REPORT.md
    └── REMEDIATION_REPORT.md
```

## Overview

SharePy is a mini-Dropbox clone built with:
- Backend: FastAPI (Python)
- Database: PostgreSQL 15
- File Storage: MinIO (S3-compatible)
- Reverse Proxy: Nginx
- Admin Tool: Adminer
- Orchestration: Docker Compose (6-7 services)

## 15 Security Misconfigurations (M1-M15)

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

## Getting Started

### Vulnerable Version
```bash
cd vulnerable/sharepy
docker-compose up -d
# Access at: http://localhost
```

### Secure Version
```bash
cd secure/sharepy
cp .env.example .env
# Edit .env with secure values
./deploy_secure.sh
# Access at: https://localhost
```

## Documentation

Each version contains detailed reports:
- **VULNERABILITY_REPORT.md**: Location of each security misconfiguration
- **EXPLOITATION_REPORT.md**: Step-by-step instructions to exploit each vulnerability
- **REMEDIATION_REPORT.md**: How each vulnerability was fixed in the secure version

## Repository Structure

Both vulnerable and secure versions are available in separate branches on GitHub:
- `vulnerable` branch: Contains the deliberately vulnerable implementation
- `secure` branch: Contains the hardened implementation with all fixes

This structure allows for easy comparison of the security improvements and serves as an educational resource for understanding common security misconfigurations and their fixes.