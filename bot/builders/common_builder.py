"""Common generated files for every project type."""

from pathlib import Path

from bot.utils.file_writer import write_file


REQUIREMENTS = """fastapi[standard]
uvicorn[standard]
pydantic-settings
jinja2
python-multipart
pytest
httpx
"""


GITIGNORE = """__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
venv/
env/
.env.local
.pytest_cache/
.mypy_cache/
.ruff_cache/
build/
dist/
*.egg-info/
storage/logs/*.log
"""


def create_common_files(
    project_path: Path,
    project_title: str,
    project_type: str,
) -> None:
    """Create common root, config, and bootstrap files."""

    write_file(
        project_path / ".env",
        f"FASTAPI_LARAVEL_APP_NAME={project_title}\n",
        overwrite=True,
    )
    write_file(project_path / ".gitignore", GITIGNORE, overwrite=True)
    write_file(project_path / "requirements.txt", REQUIREMENTS, overwrite=True)
    write_file(project_path / "run.bat", "python main.py\n", overwrite=True)
    write_file(
        project_path / "main.py",
        """import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
""",
        overwrite=True,
    )
    write_file(
        project_path / "config" / "app.py",
        f'''"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FASTAPI_LARAVEL_",
        extra="ignore",
    )

    app_name: str = "{project_title}"
    project_type: str = "{project_type}"
    debug: bool = True


settings = Settings()
''',
        overwrite=True,
    )
    write_file(
        project_path / "bootstrap" / "app.py",
        f'''"""Application bootstrap."""

from fastapi import FastAPI

from config.app import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(title=settings.app_name)
    project_type = "{project_type}"

    if project_type == "api":
        @app.get("/")
        def root():
            return {{"message": f"Welcome to {{settings.app_name}}"}}

    if project_type in ("api", "hybrid"):
        from routes.api import router as api_router

        app.include_router(api_router)

    if project_type in ("web", "hybrid"):
        from fastapi.staticfiles import StaticFiles
        from routes.web import router as web_router

        app.mount("/static", StaticFiles(directory="public"), name="static")
        app.include_router(web_router)

    return app
''',
        overwrite=True,
    )


def create_vendor_files(project_path: Path) -> None:
    """Create shared vendor helper files."""

    write_file(
        project_path / "vendor" / "helpers" / "datetime_helper.py",
        '''"""Date and time helpers."""

from datetime import datetime, timezone


def utc_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="milliseconds")
        .replace("+00:00", "Z")
    )
''',
        overwrite=True,
    )
    write_file(
        project_path / "vendor" / "helpers" / "string_helper.py",
        '''"""String helpers."""

import re


def to_slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip("-")
''',
        overwrite=True,
    )
    write_file(
        project_path / "vendor" / "helpers" / "response.py",
        '''"""Standard API response helpers."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from vendor.helpers.datetime_helper import utc_timestamp


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = Field(json_schema_extra={"example": True})
    message: str = Field(json_schema_extra={"example": "Success"})
    data: T | None = None
    timestamp: str = Field(
        default_factory=utc_timestamp,
        json_schema_extra={"example": "2026-06-24T04:06:47.964Z"},
    )
    errors: dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={"example": {}},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Success",
                "data": {},
                "timestamp": "2026-06-24T04:06:47.964Z",
                "errors": {},
            }
        }
    )


class PaginationMeta(BaseModel):
    page: int = Field(json_schema_extra={"example": 1})
    per_page: int = Field(json_schema_extra={"example": 10})
    total: int = Field(json_schema_extra={"example": 100})
    total_pages: int = Field(json_schema_extra={"example": 10})


class PaginatedApiResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True, json_schema_extra={"example": True})
    message: str = Field(json_schema_extra={"example": "Success"})
    data: list[T]
    meta: PaginationMeta
    timestamp: str = Field(
        default_factory=utc_timestamp,
        json_schema_extra={"example": "2026-06-24T04:06:47.964Z"},
    )
    errors: dict[str, Any] = Field(
        default_factory=dict,
        json_schema_extra={"example": {}},
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Items fetched successfully",
                "data": [],
                "meta": {
                    "page": 1,
                    "per_page": 10,
                    "total": 100,
                    "total_pages": 10,
                },
                "timestamp": "2026-06-24T04:06:47.964Z",
                "errors": {},
            }
        }
    )


def success_response(
    message: str = "Success",
    data: T | None = None,
) -> ApiResponse[T]:
    return ApiResponse[T](
        success=True,
        message=message,
        data=data,
        errors={},
    )


def error_response(
    message: str = "Error",
    errors: dict[str, Any] | None = None,
    data: T | None = None,
) -> ApiResponse[T]:
    return ApiResponse[T](
        success=False,
        message=message,
        data=data,
        errors=errors or {},
    )


def validation_error_response(
    errors: dict[str, Any],
    message: str = "Validation failed",
) -> ApiResponse[None]:
    return ApiResponse[None](
        success=False,
        message=message,
        data=None,
        errors=errors,
    )


def paginated_response(
    message: str,
    data: list[T],
    page: int,
    per_page: int,
    total: int,
) -> PaginatedApiResponse[T]:
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    return PaginatedApiResponse[T](
        success=True,
        message=message,
        data=data,
        meta=PaginationMeta(
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages,
        ),
        errors={},
    )
''',
        overwrite=True,
    )
    write_file(
        project_path / "vendor" / "helpers" / "__init__.py",
        '''"""Shared helper exports."""

from vendor.helpers.response import (
    ApiResponse,
    PaginatedApiResponse,
    PaginationMeta,
    success_response,
    error_response,
    validation_error_response,
    paginated_response,
)
from vendor.helpers.datetime_helper import utc_timestamp
from vendor.helpers.string_helper import to_slug


__all__ = [
    "ApiResponse",
    "PaginatedApiResponse",
    "PaginationMeta",
    "success_response",
    "error_response",
    "validation_error_response",
    "paginated_response",
    "utc_timestamp",
    "to_slug",
]
''',
        overwrite=True,
    )


def create_app_main(
    project_path: Path,
    project_title: str,
    project_type: str,
) -> None:
    """Create app/main.py."""

    write_file(
        project_path / "app" / "main.py",
        f'''"""FastAPI application instance for {project_title}."""

from bootstrap.app import create_app


app = create_app()
''',
        overwrite=True,
    )


def create_readme(
    project_path: Path,
    project_title: str,
    project_type: str,
) -> None:
    """Create generated project README."""

    project_type_label = {
        "api": "API only",
        "web": "Web only",
        "hybrid": "API + Web",
    }[project_type]

    write_file(
        project_path / "README.md",
        f"""# {project_title}

Generated FastAPI project using a Laravel-style folder structure.

## Project Type

{project_type_label}

## Run

```powershell
py -3.13 -m venv .venv
.\\.venv\\Scripts\\activate
pip install -r requirements.txt
python main.py
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

API projects also include:

- http://127.0.0.1:8000/api/v1/health
- http://127.0.0.1:8000/api/v1/items

Web projects also include:

- http://127.0.0.1:8000/about

## Structure

- `app/Http/Controllers` contains API and web controllers.
- `app/Http/Requests` contains request schemas.
- `app/Http/Resources` contains response serializers.
- `app/Models` contains domain models.
- `app/Services` contains business logic.
- `routes` contains FastAPI routers.
- `bootstrap/app.py` creates and wires the FastAPI app.
- `config/app.py` contains application settings.
- `resources/views` contains Jinja templates.
- `public` contains static assets.
- `vendor/helpers` contains shared response, date, and string helpers.

## API Response Standard

This project uses generic response models from `vendor.helpers`.

For one object:

```python
response_model=ApiResponse[ItemResource]
```

For list data:

```python
response_model=ApiResponse[list[ItemResource]]
```

Example response:

```json
{{
  "success": true,
  "message": "Items fetched successfully",
  "data": [
    {{
      "id": 1,
      "name": "Sample Item",
      "description": "Laravel-style FastAPI item"
    }}
  ],
  "timestamp": "2026-06-24T04:06:47.964Z",
  "errors": {{}}
}}
```

For paginated list data:

```python
response_model=PaginatedApiResponse[ItemResource]
```

Example pagination response:

```json
{{
  "success": true,
  "message": "Items fetched successfully",
  "data": [
    {{
      "id": 1,
      "name": "Sample Item",
      "description": "Laravel-style FastAPI item"
    }}
  ],
  "meta": {{
    "page": 1,
    "per_page": 10,
    "total": 100,
    "total_pages": 10
  }},
  "timestamp": "2026-06-24T04:06:47.964Z",
  "errors": {{}}
}}
```
""",
        overwrite=True,
    )
