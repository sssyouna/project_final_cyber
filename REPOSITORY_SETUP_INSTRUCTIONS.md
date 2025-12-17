# Repository Setup Instructions

This document provides instructions for setting up the three GitHub repositories for the SharePy project.

## Repository Structure

1. **Main Repository** (`project_final_cyber`)
   - Contains the complete project folder structure including both secure_version and vulnerable_version directories
   - Includes all documentation files, reports, and supporting materials
   - Represents the full project deliverable

2. **Secure-Only Repository** (`sharepy-secure`)
   - Contains only the contents of the secure_version/sharepy directory
   - Includes all files necessary to run the secure version independently
   - Maintains proper directory structure and dependencies

3. **Vulnerable-Only Repository** (`sharepy-vulnerable`)
   - Contains only the contents of the vulnerable_version/sharepy directory
   - Includes all files necessary to run the vulnerable version independently
   - Maintains proper directory structure and dependencies

## Setup Instructions

### Prerequisites
- Git installed on your system
- GitHub account
- Internet connection

### Step 1: Create Repositories on GitHub

1. Log in to your GitHub account
2. Create three new repositories:
   - `project_final_cyber` (public or private as desired)
   - `sharepy-secure` (public or private as desired)
   - `sharepy-vulnerable` (public or private as desired)

### Step 2: Push Main Repository

The main repository (`project_final_cyber`) has already been prepared with all content. To push it:

```bash
cd /home/kali/Desktop/project_final_cyber
git remote set-url origin https://github.com/YOUR_USERNAME/project_final_cyber.git
git push origin secure
```

### Step 3: Push Secure-Only Repository

The secure-only repository has been prepared in `/home/kali/Desktop/sharepy-secure`. To push it:

```bash
cd /home/kali/Desktop/sharepy-secure
git remote set-url origin https://github.com/YOUR_USERNAME/sharepy-secure.git
git push -u origin master
```

### Step 4: Push Vulnerable-Only Repository

The vulnerable-only repository has been prepared in `/home/kali/Desktop/sharepy-vulnerable`. To push it:

```bash
cd /home/kali/Desktop/sharepy-vulnerable
git remote set-url origin https://github.com/YOUR_USERNAME/sharepy-vulnerable.git
git push -u origin master
```

## Repository Contents

### Main Repository (`project_final_cyber`)
- Complete project structure with both versions
- All documentation files
- Reports and supporting materials
- Test scripts and verification tools

### Secure-Only Repository (`sharepy-secure`)
- `/backend/` - Application backend with security fixes
- `/nginx/` - Secure Nginx configuration
- `docker-compose.yml` - Docker orchestration file
- `check_security.py` - Security validation script
- `deploy_secure.sh` - Deployment script
- Environment files and requirements
- Dashboard templates

### Vulnerable-Only Repository (`sharepy-vulnerable`)
- `/backend/` - Vulnerable application backend
- `/nginx/` - Vulnerable Nginx configuration
- `docker-compose.yml` - Docker orchestration file
- `check_security.py` - Security validation script
- Environment files and requirements
- Dashboard templates
- Sample vulnerable files in uploads directory

## Educational Use

These repositories are designed for educational purposes:
- Students can study the vulnerable version to learn about security misconfigurations
- Students can study the secure version to learn about proper security practices
- Instructors can use the main repository as a complete course material package
- Security professionals can use these for training and demonstration purposes

## Notes

- All repositories include Docker configurations for easy deployment
- Both secure and vulnerable versions can be run independently
- The main repository contains comprehensive documentation about all vulnerabilities
- Each repository includes a README file with specific instructions for that version