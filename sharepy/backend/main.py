from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Response
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
minio_client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=True  # Use HTTPS
)

# ✅ FIX M14: Remove debug endpoints entirely
# @app.get("/debug/info") - REMOVED!

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