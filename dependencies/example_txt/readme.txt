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
fastapi-project/
├── app/
│   ├── api/                  # (like Http/Controllers in Laravel)
│   │   ├── controllers/      # route logic
│   │   ├── middleware/       # request middleware
│   │   ├── requests/         # request validation (Pydantic)
│   │   └── routes/           # route definitions
│   │
│   ├── models/               # SQLAlchemy models (like Laravel Models)
│   ├── schemas/              # Pydantic schemas (like Laravel FormRequests/DTOs)
│   ├── services/             # business logic (like Laravel Services)
│   ├── repositories/         # database queries (like Laravel Repositories)
│   ├── exceptions/           # custom exceptions
│   └── providers/            # dependency injection, events (like Laravel Providers)
│
├── bootstrap/                # startup files (DB init, logging)
├── config/                   # config files (db, auth, cache…)
├── database/                 
│   ├── migrations/           # alembic migrations
│   ├── seeders/              # seeding data
│   └── factories/            # faker factories
│
├── public/                   # static files (CSS, JS, uploads) 
├── resources/                
│   ├── views/                # Jinja2 templates (like Laravel Blade)
│   └── lang/                 # translations
│
├── routes/                   # main route entry (like Laravel routes/web.php, api.php)
├── storage/                  # cache, logs, uploads
├── tests/                    # pytest tests
├── .env                      # environment variables
├── main.py                   # app entry (like Laravel artisan serve)
├── requirements.txt           # (like composer.json)
└── alembic.ini                # migration config
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