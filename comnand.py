import os

from utils.loading_spinner import loading_spinner


def create_folders(base_dir, folders):
    """
    Create folders and an __init__.py file to make them Python packages.
    """
    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)

        # Skip __init__.py in test folders
        if "/tests" not in folder:
            init_file = os.path.join(path, "__init__.py")
            with open(init_file, "w"):
                pass


def create_files(base_dir, files):
    """
    Create files with optional content.
    """
    for file_path, content in files.items():
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)


def main():
    base_folder = input("Enter the base folder name: ").strip()
    if not base_folder:
        print("❌ Base folder name cannot be empty.")
        return

    print(f"\n📦 Creating FastAPI project: {base_folder}")
    os.makedirs(base_folder, exist_ok=True)
    loading_spinner("Initializing project", duration=1.5)

    folders = [
        "app",
        "app/api/v1/routes",
        "app/api/v1/schemas",
        "app/core",
        "app/db/models",
        "app/db/crud",
        "app/services",
        "app/utils",
        "commands",
        "tests/integration",
        "tests/unit",
    ]

    print("\n📁 Creating folders...")
    create_folders(base_folder, folders)
    loading_spinner("Initializing project", duration=1.5)

    files = {
        "README.md": f"# {base_folder}\n\nGenerated FastAPI project scaffold.",
        "main.py": (
            "from fastapi import FastAPI\n\n"
            "app = FastAPI()\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {\"message\": \"Welcome to the FastAPI project!\"}\n"
        )
    }

    print("\n📝 Creating files...")
    create_files(base_folder, files)
    loading_spinner("Initializing project", duration=1.5)

    print("\n✅ FastAPI project structure created successfully!")


if __name__ == "__main__":
    main()
