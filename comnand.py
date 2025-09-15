import os
import logging
import tkinter as tk
from tkinter import filedialog
from typing import Dict, List, Optional

from dependencies.item_file import (
    generate_auth_dependency_file,
    generate_base_response_file,
    generate_config_file,
    generate_database_file,
    generate_env_file,
    generate_gitignore_file,
    generate_logging_file,
    generate_main_file,
    generate_rbac_dependency_file,
    generate_readme_file,
    generate_requirements_file,
    generate_storage_file,
)
from utils.jwt_secret_key import generate_secret_key
from utils.loading_spinner import loading_spinner

logging.basicConfig(level=logging.INFO, format="%(message)s")


# ---------------------------
# Helpers
# ---------------------------
def create_folders(base_dir: str, folders: List[str]) -> None:
    """Create folders with __init__.py (except tests)."""
    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)

        if "tests" not in folder.split(os.sep):
            init_file = os.path.join(path, "__init__.py")
            try:
                with open(init_file, "w", encoding="utf-8"):
                    pass
            except OSError as e:
                logging.warning(f"⚠️ Failed to create {init_file}: {e}")


def create_files(base_dir: str, files: Dict[str, str]) -> None:
    """Create files with given content inside base_dir."""
    for relative_path, content in files.items():
        full_path = os.path.join(base_dir, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as e:
            logging.warning(f"⚠️ Failed to create file {full_path}: {e}")


def ask_yes_no(question: str, default: bool = False) -> bool:
    """Ask yes/no question with default option."""
    choice = input(f"\n{question} (y/n): ").strip().lower()
    if choice in ("y", "yes"):
        return True
    if choice in ("n", "no"):
        return False
    return default


def select_base_folder() -> Optional[str]:
    """Open a folder dialog for selecting project root."""
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Base Folder")
    root.destroy()
    return folder or None


def select_db_type() -> Optional[str]:
    """Let the user select a database type."""
    db_options = ["mysql", "postgresql", "oracle"]
    print("\n🗄️  Select a database type:")
    for idx, db in enumerate(db_options, start=1):
        print(f"{idx}. {db.capitalize()}")

    choice = input("Enter number (1-3): ").strip()
    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(db_options):
            return db_options[idx - 1]

    logging.error("❌ Invalid choice. Exiting.")
    return None


# ---------------------------
# Main generator
# ---------------------------
def main() -> None:
    print("📂 Select base folder for FastAPI project")
    base_folder = select_base_folder()
    if not base_folder:
        logging.error("❌ No folder selected. Exiting.")
        return

    # Feature options
    request_jwt = ask_yes_no("🔑 Use JWT authentication?", default=True)
    request_db = ask_yes_no("🗄️  Use a database?", default=True)

    db_type = None
    if request_db:
        db_type = select_db_type()
        if not db_type:
            return
        logging.info(f"✅ Selected database: {db_type}")

    logging.info(f"\n📦 Creating Laravel-style FastAPI project in: {base_folder}")
    os.makedirs(base_folder, exist_ok=True)
    loading_spinner("Initializing project", duration=1.2)

    # Folder structure
    folders = [
        "app",
        "app/api/controllers",
        "app/api/routers",
        "app/api/schemas",
        "app/core",
        "app/db",
        "app/dependencies",
        "app/services",
        "app/utils",
        "tests",
    ]
    logging.info("\n📁 Creating folders...")
    create_folders(base_folder, folders)
    loading_spinner("Creating folders", duration=1.2)

    # File structure
    files = {
        "README.md": generate_readme_file(),
        "requirements.txt": generate_requirements_file(
            request_db=request_db, request_jwt=request_jwt, db_type=db_type
        ),
        "main.py": generate_main_file(),
        "app/core/config.py": generate_config_file(
            request_jwt=request_jwt, request_db=request_db
        ),
        "app/core/logging.py": generate_logging_file(),
        "app/dependencies/auth_dependency.py": generate_auth_dependency_file(),
        "app/dependencies/rbac_dependency.py": generate_rbac_dependency_file(),
        "app/utils/base_response.py": generate_base_response_file(),
        "app/utils/storage.py": generate_storage_file(),
        ".env": generate_env_file(
            request_jwt=request_jwt,
            request_db=request_db,
            jwt_secret_key=generate_secret_key(),
            db_type=db_type,
        ),
        ".env.example": generate_env_file(
            request_jwt=request_jwt, request_db=request_db, db_type=db_type
        ),
        ".gitignore": generate_gitignore_file(),
    }

    if request_db:
        files["app/core/database.py"] = generate_database_file(db_type=db_type)

    logging.info("\n📝 Creating files...")
    create_files(base_folder, files)
    loading_spinner("Creating files", duration=1.2)

    logging.info("\n✅ FastAPI project (Laravel-style) created successfully!")
    print(f"👉 Next step:\n   cd {base_folder} && uvicorn main:app --reload")


if __name__ == "__main__":
    main()
