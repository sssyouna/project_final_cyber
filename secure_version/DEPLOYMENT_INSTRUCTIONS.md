# SharePy Deployment Instructions

## Repository Setup

1. Create a new GitHub repository named `final_project_cyber`
2. Do not initialize with README, .gitignore, or license

## Push Both Branches to GitHub

### Push the vulnerable branch:
```bash
cd /home/kali/Desktop/project_final_cyber
git remote add origin https://github.com/YOUR_USERNAME/final_project_cyber.git
git push -u origin vulnerable
```

### Push the secure branch:
```bash
git checkout secure
git push -u origin secure
```

## Branch Contents

### Vulnerable Branch
Contains the deliberately vulnerable implementation with all 15 security misconfigurations:
- Hardcoded credentials
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

### Secure Branch
Contains the hardened implementation with all 15 vulnerabilities fixed:
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

## Running the Applications

### Vulnerable Version
```bash
git checkout vulnerable
cd sharepy
docker-compose up -d
```

Accessible at: http://localhost

### Secure Version
```bash
git checkout secure
cd sharepy
cp backend/.env.example backend/.env
# Edit backend/.env with secure values
./deploy_secure.sh
```

Accessible at: https://localhost

## Security Validation

Run the automated security checker:
```bash
cd sharepy
python3 check_security.py
```

This will validate that all 15 security fixes have been properly implemented.