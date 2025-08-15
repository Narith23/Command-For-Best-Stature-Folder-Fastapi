# Generate .env.example file
import os
import shutil


def generate_env_file(request_jwt: bool = False, request_db: bool = False) -> str:
    base_txt = (
        "APP_NAME=FastAPI\n"
        "APP_ENV=development\n"
        "APP_DEBUG=true\n"
        "APP_DESCRIPTION=This is a FastAPI application.\n"
        "APP_VERSION=1.0.0\n\n"
        "ROUTER_PREFIX=api/v1\n\n"
    )

    if request_jwt:
        base_txt = (
            base_txt + "JWT_SECRET_KEY=your_secret_key\n"
            "JWT_ALGORITHM=HS256\n"
            "JWT_ACCESS_TOKEN_EXPIRES=15\n"
            "JWT_REFRESH_TOKEN_EXPIRES=30\n\n"
        )

    if request_db:
        base_txt = (
            base_txt + "DB_CONNECTION=mysql\n"
            "DB_HOST=localhost\n"
            "DB_PORT=3306\n"
            "DB_DATABASE=your_database\n"
            "DB_USERNAME=root\n"
            "DB_PASSWORD=your_password\n\n"
        )

    base_txt = (
        base_txt + "BROADCAST_DRIVER=log\n"
        "CACHE_DRIVER=file\n"
        "QUEUE_CONNECTION=sync\n"
        "SESSION_DRIVER=file\n"
        "SESSION_LIFETIME=120\n\n"
    )

    return base_txt


# Generate base response file
def generate_base_response_file() -> str:
    src_path = os.path.join("dependencies", "example_txt", "base_response.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()


# Generate Config file
def generate_config_file(request_jwt: bool = False, request_db: bool = False) -> str:
    base_txt = (
        "from pydantic_settings import BaseSettings\n\n"
        "class Settings(BaseSettings):\n"
        "\tAPP_NAME: str = 'FastAPI'\n"
        "\tAPP_ENV: str = 'development'\n"
        "\tAPP_DEBUG: bool = True\n"
        "\tAPP_DESCRIPTION: str = 'This is a FastAPI application.'\n"
        "\tAPP_VERSION: str = '1.0.0'\n\n"
        "\tROUTER_PREFIX: str = 'api/v1'\n\n"
    )

    if request_jwt:
        base_txt = (
            base_txt + "\tJWT_SECRET_KEY: str = 'your_secret_key'\n"
            "\tJWT_ALGORITHM: str = 'HS256'\n"
            "\tJWT_ACCESS_TOKEN_EXPIRES: int = 15\n"
            "\tJWT_REFRESH_TOKEN_EXPIRES: int = 30\n\n"
        )

    if request_db:
        base_txt = (
            base_txt + "\tDB_CONNECTION: str = 'mysql'\n"
            "\tDB_HOST: str = 'localhost'\n"
            "\tDB_PORT: int = 3306\n"
            "\tDB_DATABASE: str = 'your_database'\n"
            "\tDB_USERNAME: str = 'root'\n"
            "\tDB_PASSWORD: str = 'your_password'\n\n"
        )

    base_txt = (
        base_txt + "\tBROADCAST_DRIVER: str = 'log'\n"
        "\tCACHE_DRIVER: str = 'file'\n"
        "\tQUEUE_CONNECTION: str = 'sync'\n"
        "\tSESSION_DRIVER: str = 'file'\n"
        "\tSESSION_LIFETIME: int = 120\n\n"
        "settings = Settings()"
    )

    return base_txt


# Generate main.py file
def generate_main_file() -> str:
    src_path = os.path.join("dependencies", "example_txt", "main.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()


# Generate requirements.txt file
def generate_requirements_file() -> str:
    base_txt = "fastapi[all]\nSQLAlchemy\n"

    return base_txt


# Generate Readme file
def generate_readme_file() -> str:
    src_path = os.path.join("dependencies", "example_txt", "readme.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()
