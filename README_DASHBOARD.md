# SharePy Vulnerability Dashboard

This repository contains two versions of the SharePy application with a unified web interface that demonstrates all 15 security vulnerabilities:

1. **Vulnerable Version**: Contains all 15 security misconfigurations for educational purposes
2. **Secure Version**: Shows how each vulnerability was properly fixed

## Dashboard Features

The dashboard provides an attacker-friendly interface that clearly presents and allows exploitation of all 15 identified security misconfigurations (M1-M15):

### M1: Admin Password in Clear Text
Hardcoded administrative credentials in configuration files and source code.

### M2: Debug Mode Enabled
FastAPI running in debug mode, exposing detailed error messages and stack traces.

### M3: Directory Listing Enabled
Nginx configuration allows browsing of the uploads directory.

### M4: Sensitive Files Accessible
Configuration files and version control data are exposed through the web server.

### M5: pgAdmin/Adminer Publicly Accessible
Database administration tool exposed without authentication.

### M6: MinIO Public Bucket + Keys in Code
Object storage credentials hardcoded and service exposed publicly.

### M7: CORS Wildcard
Cross-Origin Resource Sharing configured with wildcards.

### M8: No Security Headers
Missing essential HTTP security headers.

### M9: Insecure Cookies
Session cookies missing security attributes.

### M10: Default FastAPI/Uvicorn Banner
Server headers reveal technology stack versions.

### M11: Verbose Nginx Errors
Nginx configured with debug-level error logging.

### M12: Internal Ports Exposed
Internal services exposed on public ports.

### M13: chmod 777 on Uploads
Uploads directory set with world-writable permissions.

### M14: /debug/info Endpoint
Debug endpoint that leaks environment information.

### M15: Weak JWT Secret
Weak secret used for JWT token signing.

## How to Use the Dashboard

1. Navigate to the vulnerable or secure version directory
2. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```
3. Access the dashboard at `http://localhost`

## Educational Purpose

This dashboard is designed for cybersecurity education and research. It allows students and security professionals to:
- Understand common web application vulnerabilities
- Learn how to identify security misconfigurations
- See the difference between vulnerable and secure implementations
- Practice penetration testing techniques in a controlled environment

**Warning**: Do not deploy the vulnerable version in production environments.