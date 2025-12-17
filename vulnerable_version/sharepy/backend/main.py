from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
import os
import jwt

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

# Serve the subtle vulnerable dashboard
@app.get("/", response_class=HTMLResponse)
async def vulnerable_dashboard():
    try:
        with open("templates/subtle_vulnerable_dashboard.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        try:
            # Fallback to original dashboard
            with open("templates/vulnerable_dashboard.html", "r") as f:
                html_content = f.read()
            return HTMLResponse(content=html_content, status_code=200)
        except FileNotFoundError:
            return HTMLResponse(content="Dashboard not found", status_code=404)

# M9: Insecure cookies (no Secure, HttpOnly, SameSite)
@app.post("/login")
def login(email: str, password: str, response: Response):
    # Login logic here
    token = jwt.encode({"email": email}, JWT_SECRET, algorithm="HS256")
    response.set_cookie("session", token)  # INSECURE!
    return {"token": token}

# Endpoint to demonstrate insecure cookies
@app.get("/cookie-info")
def cookie_info():
    return {"message": "This endpoint shows how insecure cookies are set without proper security flags"}

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

# Endpoint to demonstrate JWT weakness
@app.get("/jwt-test")
def jwt_test():
    # M15: Weak JWT secret demonstration
    token = jwt.encode({"role": "user"}, JWT_SECRET, algorithm="HS256")
    return {"token": token, "secret_used": JWT_SECRET}

@app.get("/admin")
def admin_panel():
    return {"message": "Admin panel"}

# M1: Admin password in clear text
@app.get("/credentials")
def get_credentials():
    return {
        "ADMIN_EMAIL": ADMIN_EMAIL,
        "ADMIN_PASSWORD": ADMIN_PASSWORD,
        "JWT_SECRET": JWT_SECRET,
        "MINIO_ACCESS_KEY": MINIO_ACCESS_KEY,
        "MINIO_SECRET_KEY": MINIO_SECRET_KEY
    }

# Additional endpoints for vulnerability demonstration

# M3: Directory listing enabled
@app.get("/uploads/")
def list_uploads():
    try:
        files = os.listdir("./uploads")
        return {"files": files}
    except:
        return {"files": []}

# M4: Sensitive files accessible
@app.get("/.env")
def get_env():
    try:
        with open(".env", "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        return {"error": ".env file not found"}

# M5: Demonstrate Adminer accessibility (simulated)
@app.get("/adminer-check")
def adminer_check():
    return {"message": "Adminer would be accessible at http://localhost:8080 in the vulnerable version"}

# M6: Demonstrate MinIO exposure
@app.get("/minio-info")
def minio_info():
    return {
        "endpoint": "http://localhost:9000",
        "console": "http://localhost:9001",
        "credentials": f"{MINIO_ACCESS_KEY}:{MINIO_SECRET_KEY}",
        "note": "These credentials are hardcoded and the service is publicly exposed"
    }

# M7: CORS demonstration endpoint
@app.get("/cors-test")
def cors_test():
    return {"message": "This endpoint allows all origins due to wildcard CORS configuration"}

# M8: Missing security headers demonstration
@app.get("/headers-info")
def headers_info():
    return {"message": "This response is missing security headers like CSP, HSTS, etc."}

# M10: Server banner disclosure
@app.get("/server-info")
def server_info():
    return {
        "server": "uvicorn",
        "framework": "FastAPI 0.68.1",
        "python": "3.9.7",
        "note": "Version information disclosed in server headers"
    }

# M11: Verbose error simulation
@app.get("/error-demo")
def error_demo():
    # This would normally trigger a verbose error
    return {"message": "In vulnerable mode, errors would show full stack traces and file paths"}

# M12: Port exposure simulation
@app.get("/ports-info")
def ports_info():
    return {
        "exposed_services": [
            {"service": "PostgreSQL", "port": 5432, "note": "Direct database access possible"},
            {"service": "MinIO", "port": 9000, "note": "Object storage publicly accessible"}
        ]
    }

# M13: Permission check
@app.get("/permissions-check")
def permissions_check():
    import stat
    try:
        uploads_stat = os.stat("./uploads")
        permissions = oct(uploads_stat.st_mode)[-3:]
        return {
            "directory": "./uploads",
            "permissions": permissions,
            "note": "777 permissions allow anyone to modify files" if permissions == "777" else "Secure permissions"
        }
    except:
        return {"error": "Could not check permissions"}