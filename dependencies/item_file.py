# Generate .env.example file
import os


def generate_env_file(
    request_jwt: bool = False,
    request_db: bool = False,
    jwt_secret_key: str = None,
    db_type: str = "mysql",  # default to mysql
) -> str:
    """
    Generate .env file content for FastAPI project.
    Args:
        request_jwt: Include JWT configuration
        request_db: Include DB configuration
        jwt_secret_key: Optional secret key for JWT
        db_type: 'mysql', 'postgresql', or 'oracle'
    Returns:
        str: .env file content
    """
    base_txt = (
        "APP_NAME=FastAPI\n"
        "APP_ENV=development\n"
        "APP_DEBUG=true\n"
        "APP_DESCRIPTION=This is a FastAPI application.\n"
        "APP_VERSION=1.0.0\n\n"
        "ROUTER_PREFIX=api/v1\n\n"
    )

    # JWT configuration
    if request_jwt:
        base_txt += (
            f"JWT_SECRET_KEY={jwt_secret_key or 'your_secret_key'}\n"
            "JWT_ALGORITHM=HS256\n"
            "JWT_ACCESS_TOKEN_EXPIRES=15\n"
            "JWT_REFRESH_TOKEN_EXPIRES=30\n\n"
        )

    # Database configuration
    if request_db:
        db_type = db_type.lower()
        if db_type == "mysql":
            base_txt += (
                "DB_CONNECTION=mysql\n"
                "DB_HOST=localhost\n"
                "DB_PORT=3306\n"
                "DB_DATABASE=your_database\n"
                "DB_USERNAME=root\n"
                "DB_PASSWORD=your_password\n\n"
            )
        elif db_type == "postgresql":
            base_txt += (
                "DB_CONNECTION=postgresql\n"
                "DB_HOST=localhost\n"
                "DB_PORT=5432\n"
                "DB_DATABASE=your_database\n"
                "DB_USERNAME=postgres\n"
                "DB_PASSWORD=your_password\n\n"
            )
        elif db_type == "oracle":
            base_txt += (
                "DB_CONNECTION=oracle\n"
                "DB_HOST=localhost\n"
                "DB_PORT=1521\n"
                "DB_SERVICE_NAME=XE\n"
                "DB_USERNAME=system\n"
                "DB_PASSWORD=your_password\n\n"
            )
        else:
            raise ValueError(f"Invalid db_type: {db_type}")

    # Other Laravel-style configurations
    base_txt += (
        "BROADCAST_DRIVER=log\n"
        "CACHE_DRIVER=file\n"
        "QUEUE_CONNECTION=sync\n"
        "SESSION_DRIVER=file\n"
        "SESSION_LIFETIME=120\n\n"
        "LOG_FILE=storage/logs/app.log\n"
    )

    return base_txt


# Generate base response file
def generate_base_response_file() -> str:
    """
    Generate the base_response.py file content.

    Returns:
        str: Content of the base_response.py file.
    """
    src_path = os.path.join("dependencies", "example_txt", "base_response.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()


# Generate Config file
def generate_config_file(request_jwt: bool = False, request_db: bool = False) -> str:
    """
    Generate the config.py file content based on the selected features.

    Args:
        request_jwt: Include JWT configuration
        request_db: Include DB configuration
    Returns:
        str: Content of the config.py file.
    """
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
        "\tLOG_FILE: str = 'storage/logs/app.log'\n\n"
        "\tclass Config:\n"
        "\t\tenv_file = '.env'\n"
        "\t\tenv_file_encoding = 'utf-8'\n"
        "\t\tcase_sensitive = True\n\n"
        "settings = Settings()"
    )

    return base_txt


# Generate main.py file
def generate_main_file() -> str:
    """
    Generate the main.py file content.

    Returns:
        str: Content of the main.py file.
    """
    src_path = os.path.join("dependencies", "example_txt", "main.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()


# Generate requirements.txt file
def generate_requirements_file(
    request_jwt: bool = False, request_db: bool = False, db_type: str = "mysql"
) -> str:
    """
    Generate requirements.txt content based on project features.

    Args:
        request_jwt: Include JWT dependencies
        request_db: Include database dependencies
        db_type: 'mysql', 'postgresql', or 'oracle'

    Returns:
        str: requirements.txt content
    """
    base_txt = "fastapi[all]\nSQLAlchemy\nclick\n"

    # JWT dependencies
    if request_jwt:
        base_txt += "python-jose[cryptography]\n"

    # Database dependencies mapping
    db_packages = {
        "mysql": "mysql-connector-python",
        "postgresql": "psycopg2-binary",
        "oracle": "cx_Oracle",
    }

    if request_db:
        db_pkg = db_packages.get(db_type.lower())
        if db_pkg:
            base_txt += f"{db_pkg}\n"
        else:
            raise ValueError(
                f"Invalid db_type: {db_type}. Choose from {list(db_packages.keys())}"
            )

    return base_txt


# Generate Readme file
def generate_readme_file() -> str:
    """
    Generate Readme file content.

    Returns:
        str: Content of the Readme file.
    """
    src_path = os.path.join("dependencies", "example_txt", "readme.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()


# Generate .gitignore file
def generate_gitignore_file() -> str:
    """
    Generate .gitignore file content.

    Returns:
        str: Content of the .gitignore file.
    """
    src_path = os.path.join("dependencies", "example_txt", "gitignore.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()


# Generate database.py file
def generate_database_file(db_type: str = "mysql") -> str:
    """
    Generate the database.py file content based on the selected DB type.

    Args:
        db_type: 'mysql', 'postgresql', or 'oracle'.

    Returns:
        str: Content of the database.py file.
    """
    db_type = db_type.lower()
    valid_types = ["mysql", "postgresql", "oracle"]

    if db_type not in valid_types:
        raise ValueError(f"Invalid db_type: {db_type}. Choose from {valid_types}")

    # Map db_type to template file
    template_map = {
        "mysql": "database_mysql.txt",
        "postgresql": "database_postgresql.txt",
        "oracle": "database_oracle.txt",
    }

    src_path = os.path.join("dependencies", "example_txt", template_map[db_type])

    try:
        with open(src_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {src_path}")


# Generate logging.py file
def generate_logging_file() -> str:
    """
    Generate the logging.py file content.

    Returns:
        str: Content of the logging.py file.
    """
    src_path = os.path.join("dependencies", "example_txt", "logging.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()
    
# Generate manage.py file
def generate_manage_file() -> str:
    """
    Generate the manage.py file content.

    Returns:
        str: Content of the manage.py file.
    """
    src_path = os.path.join("dependencies", "example_txt", "manage.txt")
    with open(src_path, "r", encoding="utf-8") as f:
        return f.read()
