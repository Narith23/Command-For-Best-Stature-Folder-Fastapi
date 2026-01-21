# Project Overview

This project is a Python script that generates a complete FastAPI project structure, inspired by the organization of a Laravel project. It is a command-line tool that interactively asks for project specifications and sets up a ready-to-use FastAPI application with a modular and scalable architecture.

The script creates a directory structure with distinct folders for application logic (`app`), configuration (`app/core`), database models (`app/db`), and other common components. It also generates essential files like `main.py`, `requirements.txt`, `.env` for environment variables, and a `.gitignore` file.

The key technologies used are Python and FastAPI. The generator also supports optional integrations for:

*   **Authentication:** JWT-based authentication can be included.
*   **Databases:** It can be configured to use MySQL, PostgreSQL, or Oracle, generating the necessary database connection and configuration files.

# Building and Running

This is a Python script and does not require a build step.

To run the project generator:

1.  Make sure you have Python installed.
2.  Install the required `tkinter` library if it's not already part of your Python installation (it's included in most standard installations).
3.  Execute the script from your terminal:

    ```bash
    python comnand.py
    ```

4.  The script will open a graphical folder selection dialog. Choose the directory where you want to create your new FastAPI project.
5.  Answer the prompts in the terminal to configure your project (e.g., whether to include JWT authentication and a database).

After the script finishes, a new FastAPI project will be created in the selected directory. The script will output the command to run the newly created application (e.g., `uvicorn main:app --reload`).

# Development Conventions

The project is structured as a single Python script (`comnand.py`) that orchestrates the generation of the FastAPI project.

*   **Dependencies:** The script's own dependencies are minimal (`tkinter`). The dependencies for the *generated* FastAPI project are determined by the user's choices and written to the `requirements.txt` file.
*   **File Generation:** The content of the generated files is sourced from template files located in the `dependencies/example_txt` directory. The `dependencies/item_file.py` script contains the logic for reading these templates and customizing them based on user input.
*   **Project Structure:** The generated FastAPI project follows a consistent structure:
    *   `app/`: Main application directory.
    *   `app/api/`: API-related files (controllers, routes, schemas).
    *   `app/core/`: Configuration and core settings.
    *   `app/db/`: Database models.
    *   `app/dependencies/`: Project-specific dependencies.
    *   `app/resources/`: Frontend assets (views, CSS, JS).
    *   `app/static/`: Compiled static assets.
    *   `tests/`: Test files.
    *   `main.py`: Application entry point.
    *   `requirements.txt`: Project dependencies.
    *   `.env`: Environment variables.
