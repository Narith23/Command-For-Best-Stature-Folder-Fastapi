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
│   ├── api/
│   │   ├── controllers/
│   │   │   ├── dashboard_controller.py
│   │   │   └── auth_controller.py
│   │   ├── middleware/
│   │   │   └── auth_middleware.py
│   │   ├── requests/
│   │   │   └── login_request.py
│   │   └── routes/
│   │       ├── web.py
│   │       └── api.py
│   │
│   ├── __init__.py
│   └── core/
│       ├── templates.py
│       └── staticfiles.py
│
├── config/
│   ├── settings.py
│   └── database.py
│
├── database/
│   ├── models/
│   │   └── user_model.py
│   └── schemas/
│       └── user_schema.py
│
├── services/
│   └── auth_service.py
│
├── static/
│   ├── css/
│   └── js/
│
├── resources/
│   ├── views/
│   │   ├── layouts/
│   │   │   └── base.html
│   │   ├── dashboard.html
│   │   └── login.html
│   └── lang/
│       └── en.json
│
├── storage/
│   ├── logs/
│   └── uploads/
│
├── main.py
├── .env
├── requirements.txt
└── tests/

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