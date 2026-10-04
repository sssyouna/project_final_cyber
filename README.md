# SharePy

SharePy is a file-sharing application prototype with a FastAPI backend, static dashboard, and deployment configuration for local or containerized use. This branch reflects the vulnerable version of the project and is intended for security assessment, testing, and learning about common application weaknesses.

## Overview

The project includes:

- A Python backend built with FastAPI
- Static HTML/CSS/JS frontend assets
- Docker-based deployment for app services
- PostgreSQL and MinIO integration configuration
- Nginx proxy setup
- Security validation scripts and deployment automation

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
The FastAPI app in `sharepy/backend/main.py` serves the dashboard and exposes endpoints for login, upload, sharing, and admin-related actions.

### Frontend
Static assets live under `sharepy/backend/static` and templates under `sharepy/backend/templates`.

### Infrastructure
The project uses Docker Compose to bring up PostgreSQL, MinIO, the backend, and Nginx, with configuration stored in environment files and deployment scripts.

## Getting Started

1. Open the project directory:

```bash
cd sharepy
```

2. Copy the sample environment file:

```bash
cp backend/.env.example backend/.env
```

3. Fill in the required environment values before running the stack.

4. Deploy with Docker Compose or run the helper script:

```bash
./deploy_secure.sh
```

## Prerequisites

- Docker
- Docker Compose
- Python 3
- A configured environment file for secrets and deployment variables

## Security Note

This branch represents a deliberately insecure or weakly hardened implementation and should be used only in controlled environments for security testing, review, and educational analysis. Do not deploy this version in production without remediation.

## Documentation

- `sharepy/backend/README.md` – backend setup and API notes
- `sharepy/backend/.env.example` – environment variable template
- `sharepy/check_security.py` – security validation helper

