import os


def create_folders(base_dir, folders):
    """
    Create folders based on the provided folder structure.
    """
    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)
        init_file = os.path.join(path, "__init__.py")
        # Create __init__.py for Python package directories
        if not os.path.exists(init_file) and "/tests" not in path:
            with open(init_file, "w") as f:
                pass


def create_files(base_dir, files):
    """
    Create files in the base directory.
    """
    for file, content in files.items():
        file_path = os.path.join(base_dir, file)
        with open(file_path, "w") as f:
            f.write(content)


# Define the folder structure
base_folder = "my_fastapi_project"

folders = [
    "app",
    "app/api/v1/routes",
    "app/api/v1/schemas",
    "app/core",
    "app/db/models",
    "app/db/crud",
    "app/services",
    "app/utils",
    "tests/integration",
    "tests/unit",
]

# Generate the folder structure
if __name__ == "__main__":
    base_folder = input("Enter the base folder name: ")
    print(f"====== Creating base folder: {base_folder} ======")
    print("")
    os.makedirs(base_folder, exist_ok=True)
    print("")
    print("====== Creating folders... ======")
    print("")
    create_folders(base_folder, folders)
    print("")
    print("====== Creating main file... ======")
    print("")
    create_files(base_folder, {"main.py": ""})
    print("")
    print("FastAPI project structure created successfully!")
