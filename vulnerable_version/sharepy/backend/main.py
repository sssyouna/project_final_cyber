from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
import os
import jwt
import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# M1: Admin credentials loaded from .env file
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@sharepy.local")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# M15: JWT secret loaded from .env file
JWT_SECRET = os.getenv("JWT_SECRET", "secret123")

# M2: Debug mode enabled
# M10: Default server banner with version information
app = FastAPI(
    debug=True,
    title="SharePy - Vulnerable Version",
    description="File sharing application with security vulnerabilities",
    version="1.0.0"
)

# M10: Server headers will include framework information by default
@app.middleware("http")
async def add_server_headers(request, call_next):
    response = await call_next(request)
    # Default Uvicorn server header reveals technology stack
    response.headers["Server"] = f"Uvicorn/{os.environ.get('UVICORN_VERSION', '0.15.0')}"
    response.headers["X-Powered-By"] = f"FastAPI/{os.environ.get('FASTAPI_VERSION', '0.68.1')}"
    return response

# M7: CORS wildcard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# M6: MinIO credentials loaded from .env file
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

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


# Serve the welcome page
@app.get("/welcome", response_class=HTMLResponse)
async def welcome_page():
    try:
        with open("templates/welcome.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="Welcome page not found", status_code=404)


# Logout endpoint
@app.post("/logout")
async def logout(response: Response):
    # In a real application, you might invalidate the token
    # For this demo, we just redirect
    response.status_code = 200
    return {"message": "Logged out successfully"}

# M9: Insecure cookies (no Secure, HttpOnly, SameSite)
@app.post("/login")
def login(email: str, password: str, response: Response):
    # Validate credentials against values from .env file
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        # Create JWT token with user information
        import time
        token_payload = {
            "email": email,
            "role": "admin",
            "exp": int(time.time()) + 3600  # 1 hour from now
        }
        token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")
        response.set_cookie("session", token)  # INSECURE: Missing Secure, HttpOnly, and SameSite attributes!
        return {"token": token, "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")



# Endpoint to demonstrate insecure cookies
@app.get("/cookie-info")
def cookie_info():
    return {"message": "This endpoint shows how insecure cookies are set without proper security flags"}

# M11: Verbose error simulation
# M10: Detailed error messages that reveal server information
@app.get("/debug-error")
def debug_error():
    # This will generate an internal error with complete stack trace
    # The debug=True mode will show full stack traces to the attacker
    result = 1 / 0  # Division by zero error
    return {"message": "This will never be reached"}





# Enhanced placeholder endpoints that expose internal information
@app.post("/register")
def register(email: str, password: str):
    return {"message": "User registered"}

# M13: Vulnerable upload endpoint that saves files to 777 permission directory
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    import os
    from pathlib import Path
    import stat
    
    # Save the uploaded file to the vulnerable uploads directory
    upload_dir = Path("./uploads")
    file_path = upload_dir / file.filename
    
    # Write the file content to the uploads directory
    with open(file_path, "wb") as buffer:
        import shutil
        shutil.copyfileobj(file.file, buffer)
    
    # M13: Explicitly set file permissions to be permissive like the directory
    os.chmod(file_path, 0o777)  # Set to rwxrwxrwx
    
    # Verify the file permissions are 777 (world-writable)
    current_permissions = oct(os.stat(file_path).st_mode)[-3:]
    
    # Get all files in uploads directory with their permissions (M13 functionality)
    all_files = []
    try:
        files = os.listdir("./uploads")
        for f in files:
            file_path_iter = os.path.join("./uploads", f)
            if os.path.isfile(file_path_iter):
                try:
                    file_stat = os.stat(file_path_iter)
                    all_files.append({
                        "name": f,
                        "permissions": oct(file_stat.st_mode)[-3:],
                        "size": file_stat.st_size
                    })
                except OSError:
                    continue
    except Exception as e:
        all_files = []
    
    # M13: Execute PHP files after upload (combine both functionalities)
    import subprocess
    import glob
    
    # Execute any PHP files in the directory (M13 vulnerability)
    php_files = sorted(glob.glob("./uploads/*.php"))  # Sort to ensure consistent order
    
    execution_results = []
    if php_files:
        # Execute the first PHP file found
        first_php_file = php_files[0]
        
        # INTENTIONALLY VULNERABLE: Execute PHP file automatically
        try:
            result = subprocess.run(["php", os.path.basename(first_php_file)], capture_output=True, text=True, cwd="uploads")
            execution_results.append({
                "executed_file": os.path.basename(first_php_file),
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })
        except Exception as e:
            execution_results.append({"error": str(e)})
    
    return {
        "filename": file.filename, 
        "message": "File uploaded",
        "file_path": str(file_path),
        "permissions": current_permissions,
        "note": "File saved with directory permissions (should be 777 due to M13 vulnerability)",
        "all_files": all_files,  # Include all files with permissions info
        "php_execution": execution_results if execution_results else "No PHP files executed"
    }

@app.get("/download/{file_id}")
def download_file(file_id: str):
    return {"file_id": file_id, "message": "File downloaded"}

@app.post("/share")
def create_share_link(file_id: str):
    return {"file_id": file_id, "share_link": f"http://localhost/share/{file_id}"}


# M11: Custom 404 handler that exposes detailed error information
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
import sys


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        # M11: Expose detailed information about the 404 error
        import os
        import platform
        return JSONResponse(
            status_code=404,
            content={
                "error": "Resource Not Found",
                "requested_path": str(request.url),
                "method": request.method,
                "server_info": {
                    "platform": platform.platform(),
                    "python_version": sys.version,
                    "working_directory": os.getcwd(),
                    "available_files": os.listdir(".") if os.path.exists(".") else [],
                },
                "debug_info": f"The requested endpoint '{request.url.path}' does not exist. Error occurred in module: {__name__}",
                "stack_trace": traceback.format_stack(),
                "note": "This detailed error message reveals internal system information (M11 vulnerability)"
            }
        )
    else:
        # For other HTTP exceptions, return default response
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

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

# M3: Directory listing enabled with PHP execution vulnerability
@app.get("/uploads/")
def list_uploads():
    import os
    import subprocess
    import glob
    
    # First, execute any PHP files in the directory (M13 vulnerability)
    php_files = sorted(glob.glob("./uploads/*.php"))  # Sort to ensure consistent order
    
    execution_results = []
    if php_files:
        # Execute the first PHP file found
        first_php_file = php_files[0]
        
        # INTENTIONALLY VULNERABLE: Execute PHP file automatically
        try:
            result = subprocess.run(["php", os.path.basename(first_php_file)], capture_output=True, text=True, cwd="uploads")
            execution_results.append({
                "executed_file": os.path.basename(first_php_file),
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })
        except Exception as e:
            execution_results.append({"error": str(e)})
    
    # Then return the directory listing as before
    try:
        files = os.listdir("./uploads")
        return {
            "files": files,
            "php_execution": execution_results if execution_results else "No PHP files executed"
        }
    except:
        return {"files": [], "php_execution": execution_results if execution_results else "No PHP files executed"}


# Additional directory listing for /static
@app.get("/static/")
def list_static():
    try:
        files = os.listdir("./static")
        return {"files": files}
    except:
        return {"files": []}


# Also add a more detailed directory listing that shows file details
# Working implementation with a different endpoint name to avoid conflicts
@app.get("/file-permissions")
def file_permissions_list():
    import stat
    import os
    try:
        files = os.listdir("./uploads")
        file_details = []
        for file in files:
            file_path = os.path.join("./uploads", file)
            if os.path.isfile(file_path):
                try:
                    file_stat = os.stat(file_path)
                    permissions = oct(file_stat.st_mode)[-3:]
                    file_details.append({
                        "name": file,
                        "permissions": permissions,
                        "size": file_stat.st_size
                    })
                except OSError:
                    continue
        return {"files": file_details}
    except Exception as e:
        return {"error": str(e), "files": []}

# M4: Sensitive files accessible
@app.get("/.env")
def get_env():
    try:
        with open(".env", "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        return {"error": ".env file not found"}


# Additional sensitive file access endpoints
@app.get("/env")
def get_env_alt():
    try:
        with open(".env", "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        return {"error": ".env file not found"}


@app.get("/config")
def get_config():
    try:
        with open(".env", "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        return {"error": ".env file not found"}


@app.get("/.git/config")
def get_git_config():
    try:
        with open(".git/config", "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        return {"error": ".git/config file not found"}


@app.get("/.git/HEAD")
def get_git_head():
    try:
        with open(".git/HEAD", "r") as f:
            return {"content": f.read()}
    except FileNotFoundError:
        return {"error": ".git/HEAD file not found"}


@app.get("/backup.db")
def get_backup_db():
    try:
        # Return the backup database file
        from fastapi.responses import FileResponse
        import os
        if os.path.exists("backup.db"):
            return FileResponse("backup.db", media_type="application/octet-stream", filename="backup.db")
        else:
            return {"error": "backup.db file not found"}
    except Exception as e:
        return {"error": str(e)}


# Additional sensitive file access endpoints for .pyc, .env, .git, backup.db
@app.get("/pyc-files")
async def get_all_pyc_files():
    import os
    import glob
    
    # List all .pyc files in src directory
    pyc_files = glob.glob("src/*.pyc")
    return {"pyc_files": pyc_files, "count": len(pyc_files)}


@app.get("/git-files")
async def list_git_directory():
    import os
    
    if os.path.exists(".git/"):
        try:
            git_files = os.listdir(".git/")
            return {"git_files": git_files}
        except:
            return {"error": "Cannot access .git directory"}
    else:
        return {"error": ".git directory not found"}


@app.get("/sensitive-info")
async def get_sensitive_info():
    import os
    
    # Gather information about sensitive files that are accessible
    sensitive_files = {
        "env_exists": os.path.exists(".env"),
        "git_exists": os.path.exists(".git"),
        "backup_db_exists": os.path.exists("backup.db"),
        "src_exists": os.path.exists("src/"),
    }
    
    return {
        "sensitive_files": sensitive_files,
        "note": "Various sensitive files are accessible via different endpoints"
    }


@app.get("/database.db")
def get_database_db():
    try:
        # Return the main database file
        from fastapi.responses import FileResponse
        import os
        if os.path.exists("database.db"):
            return FileResponse("database.db", media_type="application/octet-stream", filename="database.db")
        else:
            return {"error": "database.db file not found"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/src/main.pyc")
def get_pyc_file():
    try:
        # Return a Python compiled file
        from fastapi.responses import FileResponse
        import os
        if os.path.exists("src/main.pyc"):
            return FileResponse("src/main.pyc", media_type="application/octet-stream", filename="main.pyc")
        else:
            return {"error": "main.pyc file not found"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/src/")
def list_src_directory():
    import os
    try:
        if os.path.exists("src/"):
            files = os.listdir("src/")
            pyc_files = [f for f in files if f.endswith('.pyc')]
            return {"pyc_files": pyc_files, "all_files": files}
        else:
            return {"error": "src directory not found"}
    except Exception as e:
        return {"error": str(e)}

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
    import sys
    import platform
    return {
        "server": "uvicorn",
        "framework": f"FastAPI {getattr(app.__class__, '__version__', '0.68.1')}",
        "python": f"{sys.version}",
        "platform": f"{platform.platform()}",
        "os": f"{platform.system()} {platform.release()}",
        "architecture": f"{platform.architecture()[0]}",
        "note": "Version information disclosed in server headers",
        "working_directory": f"{os.getcwd()}",
        "executable": f"{sys.executable}"
    }

# M11: Verbose error simulation
# M10: Detailed error messages that reveal server information
@app.get("/error-demo")
def error_demo():
    # This would normally trigger a verbose error with full details
    # Debug mode will expose file paths, server details, and framework information
    raise HTTPException(status_code=500, detail="Internal server error with full details exposed")

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


# M13: Vulnerable endpoint that executes PHP files in uploads directory
@app.get("/execute-php")
def run_uploaded_php():
    import os
    import subprocess
    import glob
    
    # Use full path to uploads directory
    uploads_path = "./uploads"
    
    # Get all PHP files in the directory
    php_files = glob.glob(os.path.join(uploads_path, "*.php"))
    
    if php_files:
        # Execute only the first PHP file found
        first_php_file = php_files[0]
        
        # Extract just the filename from the full path
        filename = os.path.basename(first_php_file)
        
        # INTENTIONALLY VULNERABLE - Change to uploads directory to execute the file
        original_dir = os.getcwd()
        os.chdir("uploads")
        result = subprocess.run(["php", filename], capture_output=True, text=True)
        os.chdir(original_dir)  # Go back to original directory
        
        return {
            "status": "PHP file executed",
            "executed_file": filename,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    else:
        return {"status": "No PHP files found to execute"}