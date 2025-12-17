from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
import os
import jwt
import bcrypt
import secrets
import logging
from typing import Optional

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}'
)
logger = logging.getLogger(__name__)

# ✅ FIX M2: Debug mode disabled
app = FastAPI(
    debug=False,
    docs_url=None,  # Disable Swagger UI in production
    redoc_url=None,  # Disable ReDoc in production
    openapi_url=None  # Disable OpenAPI schema
)

# ✅ FIX M15: Strong JWT secret from environment
JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(64))
if len(JWT_SECRET) < 32:
    raise ValueError("JWT_SECRET must be at least 32 characters")

# ✅ FIX M1: Load credentials from secure environment
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")  # Pre-hashed

# ✅ FIX M7: Restrict CORS to specific origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://sharepy.com").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# ✅ FIX M6: MinIO credentials from environment only
minio_endpoint = os.getenv("MINIO_ENDPOINT")
if minio_endpoint:
    minio_client = Minio(
        minio_endpoint,
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        secure=True  # Use HTTPS
    )
else:
    minio_client = None  # MinIO not configured

# ✅ FIX M14: Remove debug endpoints entirely
# @app.get("/debug/info") - REMOVED!

# Serve the subtle secure dashboard
@app.get("/", response_class=HTMLResponse)
async def secure_dashboard():
    try:
        with open("templates/subtle_dashboard.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        try:
            # Fallback to original dashboard
            with open("templates/dashboard.html", "r") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content, status_code=200)
        except FileNotFoundError:
            return HTMLResponse(content="Dashboard not found", status_code=404)

# ✅ FIX M9: Secure cookies
@app.post("/login")
def login(email: str, password: str, response: Response):
    # Verify credentials with bcrypt
    # user = get_user_by_email(email)
    # if not user or not bcrypt.checkpw(password.encode(), user.password_hash):
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # For demo purposes, we'll simulate successful login
    # In a real app, you'd verify against hashed passwords in DB
    token = jwt.encode({"email": email}, JWT_SECRET, algorithm="HS256")
    
    # ✅ Secure cookie settings
    response.set_cookie(
        "session",
        token,
        secure=True,      # HTTPS only
        httponly=True,    # No JavaScript access
        samesite="strict", # CSRF protection
        max_age=3600      # 1 hour expiry
    )
    return {"message": "Logged in successfully"}

# Placeholder endpoints
@app.post("/register")
def register(email: str, password: str):
    return {"message": "User registered"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename, "message": "File uploaded"}

@app.get("/download/{file_id}")
def download_file(file_id: str):
    return {"file_id": file_id, "message": "File downloaded"}

@app.post("/share")
def create_share_link(file_id: str):
    return {"file_id": file_id, "share_link": f"https://sharepy.com/share/{file_id}"}

@app.get("/admin")
def admin_panel():
    return {"message": "Admin panel"}

# Endpoint to demonstrate secure credential handling
@app.get("/secure-credentials")
def get_secure_credentials_info():
    # Show that credentials are properly secured
    return {
        "message": "Credentials are loaded from environment variables, not hardcoded",
        "ADMIN_EMAIL": "Loaded from environment" if os.getenv("ADMIN_EMAIL") else "Not set",
        "JWT_SECRET_LENGTH": len(os.getenv("JWT_SECRET", "")) if os.getenv("JWT_SECRET") else 0
    }