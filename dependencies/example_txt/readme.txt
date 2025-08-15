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
project_name/
│── app/
│   ├── main.py             # Entry point
│   ├── api/                # API
|   |   ├── form            # Form request
|   |   ├── router          # Router
|   |   ├── schema          # Schemas
│   ├── core/               # Configurations & settings & databases
│   ├── db/                 # Database models
│   ├── dependencies/       # Dependencies
│   ├── services/           # Business logic
│   ├── utils               # DB connection
│── tests/                  # Unit tests
│── requirements.txt        # Python dependencies
│── README.md               # Documentation
│── .env                    # Environment variables
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