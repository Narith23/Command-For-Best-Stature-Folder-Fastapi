import os
import tkinter as tk
from tkinter import filedialog
from utils.loading_spinner import loading_spinner


def create_folders(base_dir: str, folders: list[str]) -> None:
    """
    Create folders inside base_dir.
    Adds __init__.py to each folder except those related to tests,
    so they are treated as Python packages.
    """
    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)

        if "tests" not in folder.split(os.sep):
            init_file = os.path.join(path, "__init__.py")
            try:
                with open(init_file, "w", encoding="utf-8") as f:
                    pass
            except OSError as e:
                print(f"⚠️ Warning: Failed to create {init_file}: {e}")


def create_files(base_dir: str, files: dict[str, str]) -> None:
    """
    Create files with given content inside base_dir.
    Creates parent folders if needed.
    """
    for relative_path, content in files.items():
        full_path = os.path.join(base_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            print(f"⚠️ Warning: Failed to create file {full_path}: {e}")


def select_base_folder() -> str | None:
    """
    Opens a folder selection dialog and returns the selected folder path.
    Returns None if no folder selected.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title="Select Base Folder")
    root.destroy()
    return folder_selected if folder_selected else None


def main() -> None:
    print("Please select the base folder for the FastAPI project.")
    base_folder = select_base_folder()
    if not base_folder:
        print("❌ No folder selected. Exiting.")
        return

    print(f"\n📦 Creating FastAPI project inside: {base_folder}")
    os.makedirs(base_folder, exist_ok=True)
    loading_spinner("Initializing project", duration=1.5)

    folders = [
        "app",
        "app/api/form",
        "app/api/router",
        "app/api/schema",
        "app/core",
        "app/db",
        "app/dependencies",
        "app/services",
        "app/utils",
        "tests",
    ]

    print("\n📁 Creating folders...")
    create_folders(base_folder, folders)
    loading_spinner("Creating folders", duration=1.5)

    # Define starter files
    files = {
        "README.md": f"""
# FastAPI Project Setup Guide

## 📌 Overview
This project is built with **FastAPI** — a modern, fast (high-performance) Python web framework for building APIs.  
It includes environment configuration, dependency management, and a recommended project structure.

---

## 🛠 Requirements
- Python **3.10+**
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (optional but recommended)
- (Optional) [Docker](https://www.docker.com/) for containerized deployment

---

## 📂 Project Structure
```
project_name/
│── app/
│   ├── main.py             # Entry point
│   ├── api/                # API
|   |   ├── form            # Form request
|   |   ├── router          # Router
|   |   ├── schema          # Schemas
│   ├── core/               # Configurations & settings & databases
│   ├── db/                 # Database models
│   ├── dependencies/       # Dependencies
│   ├── services/           # Business logic
│   ├── utils               # DB connection
│── tests/                  # Unit tests
│── requirements.txt        # Python dependencies
│── README.md               # Documentation
│── .env                    # Environment variables
```

---

## 🚀 Setup & Installation

### 1️⃣ Create Virtual Environment
```bash
python -m venv .venv
```
Activate it:
- **Windows (PowerShell)**  
  ```bash
  .\.venv\Scripts\activate
  ```
- **Mac/Linux**  
  ```bash
  source .venv/bin/activate
  ```

### 2️⃣ Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables
Create a `.env` file in the project root:
```env
cp .\.env.example .\.env
```

---

## ▶️ Run the Application
```bash
uvicorn app.main:app --reload
```
- Open URL: [http://localhost:8000]
- Open API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Alternative docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Run Tests
```bash
pytest
```
        """,
        "requirements.txt": "fastapi[all]\nSQLAlchemy",
        "main.py": (
"import logging\n"
"from fastapi import FastAPI, HTTPException, Request, status\n"
"from fastapi.exceptions import RequestValidationError\n"
"from fastapi.responses import JSONResponse\n"
"from starlette.middleware.cors import CORSMiddleware\n\n"
"from app.utils.base_response import BaseResponse\n"
"from app.core.config import settings\n\n"
"# Setup logger to print to terminal\n"
"logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')\n"
"logger = logging.getLogger(__name__)\n\n"
"# Configure API documentation URLs based on environment\n"
"api_docs = {\n"
"    'openapi_url': (\n"
"        f'/{settings.ROUTER_PREFIX}/docs/openapi.json' if settings.APP_ENV == 'development' else None\n"
"    ),\n"
"    'docs_url': (\n"
"        f'/{settings.ROUTER_PREFIX}/docs' if settings.APP_ENV == 'development' else None\n"
"    ),\n"
"    'redoc_url': (\n"
"        f'/{settings.ROUTER_PREFIX}/redoc' if settings.APP_ENV == 'development' else None\n"
"    ),\n"
"}\n\n"
"# Initialize FastAPI application\n"
"app = FastAPI(\n"
"    title=settings.APP_NAME,\n"
"    description=settings.APP_DESCRIPTION,\n"
"    version=settings.APP_VERSION,\n"
"    **api_docs,\n"
")\n\n"
"app.add_middleware(\n"
"    CORSMiddleware,\n"
"    allow_origins=['http://localhost:3000'],  # React/Vue/etc.\n"
"    allow_credentials=True,\n"
"    allow_methods=['*'],\n"
"    allow_headers=['*'],\n"
")\n\n"
"@app.exception_handler(HTTPException)\n"
"async def custom_http_exception_handler(request: Request, exc: HTTPException):\n"
"    detail = exc.detail\n\n"
"    # Check if detail is a dict and contains 'message'\n"
"    if isinstance(detail, dict) and 'message' in detail:\n"
"        message = detail['message']\n"
"    else:\n"
"        message = detail  # Assume it's a string\n\n"
"    return JSONResponse(\n"
"        status_code=exc.status_code,\n"
"        content={\n"
"            'status_code': exc.status_code,\n"
"            'message': message,\n"
"            'result': None,\n"
"        },\n"
"    )\n\n"
"@app.exception_handler(RequestValidationError)\n"
"async def validation_exception_handler(request: Request, exc: RequestValidationError):\n"
"    errors = exc.errors()\n"
"    formatted_errors = [\n"
"        {\n"
"            'field': '.'.join(str(loc) for loc in err['loc'][1:]),  # skip 'body' or 'query'\n"
"            'message': err['msg'],\n"
"        }\n"
"        for err in errors\n"
"    ]\n\n"
"    return JSONResponse(\n"
"        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,\n"
"        content={\n"
"            'status_code': status.HTTP_422_UNPROCESSABLE_ENTITY,\n"
"            'message': 'Validation failed',\n"
"            'result': formatted_errors,\n"
"        },\n"
"    )\n\n"
"@app.get('/', status_code=200, response_model=BaseResponse[None], tags=['Default'])\n"
"def read_root():\n"
"    return BaseResponse[None].success(\n"
"        message=f\"{settings.APP_NAME} is running v{settings.APP_VERSION}. \"\n"
"                f\"Go to {api_docs['docs_url']} for API documentation.\",\n"
"    )\n"
),
        "app/core/config.py": """
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # General app info
    APP_NAME: str
    APP_ENV: str
    APP_DEBUG: bool
    APP_DESCRIPTION: str
    APP_VERSION: str

    # Router settings
    ROUTER_PREFIX: str
    
    # JWT settings
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES: int
    JWT_REFRESH_TOKEN_EXPIRES: int

    # Database settings
    DB_CONNECTION: str
    DB_HOST: str
    DB_PORT: int
    DB_DATABASE: str
    DB_USERNAME: str
    DB_PASSWORD: str
    
    # Other
    BROADCAST_DRIVER: str
    CACHE_DRIVER: str
    QUEUE_CONNECTION: str
    SESSION_DRIVER: str
    SESSION_LIFETIME: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
            
""",
        "app/utils/base_response.py": """
from typing import TypeVar, Generic, Optional, List
from pydantic import Field
from pydantic.generics import GenericModel

T = TypeVar("T")


# --- Base response model ---
class BaseResponse(GenericModel, Generic[T]):
    status_code: int = Field(200, description="HTTP status code")
    message: str = Field("OK", description="Description or message")
    result: Optional[T] = Field(None, description="Returned data (if any)")

    @classmethod
    def success(
        cls, status_code: int = 200, message: str = "OK", result: Optional[T] = None
    ) -> "BaseResponse[T]":
        return cls(status_code=status_code, message=message, result=result)

    @classmethod
    def error(
        cls,
        status_code: int = 400,
        message: str = "Bad request",
        result: Optional[T] = None,
    ) -> "BaseResponse[T]":
        return cls(status_code=status_code, message=message, result=result)


# --- Pagination structure ---
class PaginationItems(GenericModel, Generic[T]):
    data: List[T] = Field(default_factory=list, description="Paginated list of items")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, description="Items per page")
    total: int = Field(..., ge=0, description="Total number of items")
    pages: int = Field(..., ge=0, description="Total number of pages")

    @classmethod
    def create(
        cls, data: List[T], total: int, page: int, size: int
    ) -> "PaginationItems[T]":
        pages = (total + size - 1) // size if size else 0
        return cls(data=data, page=page, size=size, total=total, pages=pages)


# --- Response wrapper for paginated items ---
class PaginatedResponse(GenericModel, Generic[T]):
    status_code: int = Field(200, description="HTTP status code")
    message: str = Field("OK", description="Description or message")
    result: Optional[PaginationItems[T]] = Field(
        None, description="Paginated result data"
    )

    @classmethod
    def success(
        cls, items: List[T], total: int, page: int, size: int, message: str = "OK"
    ) -> "PaginatedResponse[T]":
        pagination = PaginationItems.create(
            data=items, total=total, page=page, size=size
        )
        return cls(status_code=200, message=message, result=pagination)

        
""",
        ".env.example": f"""
# -----------------------------
# General Application Settings
# -----------------------------
APP_NAME=FastAPI
APP_ENV=development
APP_DEBUG=true
APP_DESCRIPTION=This is a FastAPI application.
APP_VERSION=1.0.0

# -----------------------------
# Routing Config
# -----------------------------
ROUTER_PREFIX=api/v1

# -----------------------------
# JWT Auth Settings
# -----------------------------
JWT_SECRET_KEY=a85412f4a6b5247dd2dbcefe8063a12fb047ba0c4b381e9ed074e8cafa556623
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRES=15
JWT_REFRESH_TOKEN_EXPIRES=30

# -----------------------------
# Database Connections
# -----------------------------
DB_CONNECTION=mysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=your_database
DB_USERNAME=root
DB_PASSWORD=your_password

# -----------------------------
# Queue/Session/Cache Settings
# -----------------------------
BROADCAST_DRIVER=log
CACHE_DRIVER=file
QUEUE_CONNECTION=sync
SESSION_DRIVER=file
SESSION_LIFETIME=120

""",
    }

    print("\n📝 Creating files...")
    create_files(base_folder, files)
    loading_spinner("Creating files", duration=1.5)

    print("\n✅ FastAPI project structure created successfully!")


if __name__ == "__main__":
    main()
