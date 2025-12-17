# SharePy - Vulnerable Version

This is the vulnerable version of SharePy, a file-sharing application with 15 intentional security misconfigurations.

## Misconfigurations Implemented

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

## Exploitation Methods

See the project documentation for detailed exploitation methods for each vulnerability.