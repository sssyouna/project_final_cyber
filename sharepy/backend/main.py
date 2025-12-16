from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
import os
import jwt
import psycopg2

# M1: Admin password in clear text
ADMIN_PASSWORD = "admin123"
ADMIN_EMAIL = "admin@sharepy.local"

# M15: Weak JWT secret
JWT_SECRET = "secret123"

# M2: Debug mode enabled
app = FastAPI(debug=True)

# M7: CORS wildcard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# M6: MinIO credentials in code
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

# M14: Debug endpoint that dumps environment
@app.get("/debug/info")
def debug_info():
    return {
        "env": dict(os.environ),
        "cwd": os.getcwd(),
        "files": os.listdir(".")
    }

# M9: Insecure cookies (no Secure, HttpOnly, SameSite)
@app.post("/login")
def login(email: str, password: str, response: Response):
    # Login logic here
    token = jwt.encode({"email": email}, JWT_SECRET, algorithm="HS256")
    response.set_cookie("session", token)  # INSECURE!
    return {"token": token}

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
    return {"file_id": file_id, "share_link": f"http://localhost/share/{file_id}"}

@app.get("/admin")
def admin_panel():
    return {"message": "Admin panel"}

# Other endpoints: /register, /upload, /download, /share, /admin