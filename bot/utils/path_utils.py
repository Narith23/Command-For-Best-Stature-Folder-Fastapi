"""Folder selection helpers."""

from pathlib import Path


def select_folder_with_tkinter() -> Path | None:
    """Open a native folder picker and return the selected folder."""

    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return None

    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        selected_folder = filedialog.askdirectory(
            initialdir=Path.cwd(),
            title="Select project parent folder",
        )
        root.destroy()
    except Exception:
        return None

    if not selected_folder:
        return None

    return Path(selected_folder).resolve()


def ask_parent_folder() -> Path:
    """Ask the user to select the parent folder for the generated project."""

    print("Select project parent folder:")

    selected_folder = select_folder_with_tkinter()
    if selected_folder is not None and selected_folder.is_dir():
        print(f"Selected: {selected_folder}")
        return selected_folder

    print("Folder dialog was not available or no folder was selected.")

    while True:
        folder = input(f"Enter parent folder path [{Path.cwd()}]: ").strip()
        parent_folder = Path(folder).expanduser() if folder else Path.cwd()

        if parent_folder.is_dir():
            return parent_folder.resolve()

        print("Please enter an existing folder path.")
