# SharePy Backend

FastAPI backend for SharePy, a secure file-sharing application.

## Features

- Serves the SharePy dashboard and static assets.
- Provides authentication endpoints using JWT cookies.
- Supports file upload, download, and share-link endpoints.
- Integrates with MinIO for object storage configuration.
- Uses environment variables for secrets and deployment settings.
- Runs in Docker as a non-root user.

## Project Structure

```text
backend/
├── main.py              # FastAPI application and API routes
├── requirements.txt     # Python dependencies
├── Dockerfile           # Production container configuration
├── .env.example         # Environment variable template
├── static/              # Static frontend assets
└── templates/           # HTML dashboard templates
```

## Configuration

Copy the example environment file and replace all placeholder values:

```bash
cp .env.example .env
```

Important variables include:

- `JWT_SECRET` — a random secret of at least 32 characters.
- `ADMIN_EMAIL` — administrator email address.
- `ADMIN_PASSWORD_HASH` — bcrypt-hashed administrator password.
- `MINIO_ENDPOINT` — MinIO server endpoint. Leave it unset to disable MinIO initialization.
- `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` — MinIO credentials.
- `ALLOWED_ORIGINS` — comma-separated list of permitted frontend origins.

Do not commit `.env` or real credentials to the repository.

## Local Development

From this directory, create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`.

## Docker

Build and run the backend container:

```bash
docker build -t sharepy-backend .
docker run --env-file .env -p 8000:8000 sharepy-backend
```

The production container starts Uvicorn with four workers and listens on port `8000`.

## API Routes

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/` | Serves the dashboard. |
| `POST` | `/login` | Creates a secure session cookie. |
| `POST` | `/register` | Registration placeholder endpoint. |
| `POST` | `/upload` | Uploads a file. |
| `GET` | `/download/{file_id}` | Downloads a file by ID. |
| `POST` | `/share` | Creates a share link for a file. |
| `GET` | `/admin` | Admin panel placeholder endpoint. |
| `GET` | `/secure-credentials` | Reports credential-loading status without exposing secrets. |

## Security Notes

- Use HTTPS in deployed environments.
- Set a strong, randomly generated `JWT_SECRET`.
- Store passwords as bcrypt hashes rather than plaintext.
- Restrict `ALLOWED_ORIGINS` to trusted frontend domains.
- Keep `.env` files and cloud credentials out of version control.
- Review placeholder authentication and file-storage endpoints before production use.
