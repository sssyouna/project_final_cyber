# SharePy

SharePy is a secure file-sharing application designed as a cybersecurity-focused project. The repository contains a hardened, containerized deployment for a FastAPI backend, MinIO object storage, PostgreSQL, and an Nginx reverse proxy.

## Overview

This project focuses on secure application design and deployment patterns, including:

- Environment-based secret management
- JWT-based authentication with secure cookie configuration
- Restricted CORS and network isolation
- HTTPS-only access via Nginx
- Dockerized services with internal-only networking
- Security checks and deployment validation

## Repository Structure

```text
project_final_cyber/
├── README.md
├── sharepy/
│   ├── .env
│   ├── check_security.py
│   ├── deploy_secure.sh
│   ├── docker-compose.yml
│   ├── backend/
│   │   ├── .env.example
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   ├── static/
│   │   └── templates/
│   └── nginx/
│       ├── Dockerfile.secure
│       └── nginx.conf.secure
└──
```

## Main Components

### Backend
The FastAPI application provides dashboard and API endpoints for file sharing, login, upload, and secure credential handling. See `sharepy/backend/README.md` for detailed backend documentation.

### Nginx
The Nginx service is configured for HTTPS-only access and is intended to sit in front of the FastAPI backend.

### PostgreSQL + MinIO
The app uses PostgreSQL for app data and MinIO for object storage, both deployed behind internal-only Docker networking.

### Security Validation
The repository includes a deployment script and security check script to validate configuration before starting the stack.

## Quick Start

1. Navigate to the project directory:

```bash
cd sharepy
```

2. Create a secure environment file from the example:

```bash
cp backend/.env.example backend/.env
```

3. Fill in the required values in `backend/.env` with strong credentials.

4. Deploy the stack:

```bash
./deploy_secure.sh
```

5. Access the service via HTTPS on the configured domain or local host.

## Prerequisites

- Docker
- Docker Compose
- Python 3 (for local backend development and checks)

## Notes

This project is structured around secure-by-default deployment practices. Before production use, review the environment values, secret storage, certificate setup, and any placeholder authentication or storage logic.

## Related Documentation

- `sharepy/backend/README.md` — backend-specific setup and API details
- `sharepy/backend/.env.example` — example environment configuration
- `sharepy/check_security.py` — deployment validation checks

