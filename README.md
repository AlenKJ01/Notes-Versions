# 📝 Notes App – Versioned Notes with History

A full-stack notes application built with **FastAPI**, **PostgreSQL**, and **vanilla HTML/CSS/JS**, featuring **authentication**, **note versioning**, **restore & delete history**, **search**, and **activity tracking**.

This project focuses on **clean backend architecture**, **API design**, and a **mobile-style UI** with a smooth user experience.

---

## 🚀 Features

- User authentication (Register / Login)
- JWT-based protected routes
- Create, edit, delete notes
- Automatic **version history** on every update
- Preview previous versions without overwriting
- Restore any version (creates a new version)
- Delete older versions safely
- Search notes by title
- Mobile-style centered UI
- Alembic migrations
- Ready for Docker & production deployment

---

## 📸 Screenshots
### Login Page
![Notes Page](screenshots/notes.png)
### Notes Page
![Login Page](screenshots/login.png)
### Version Preview
![Version Preview](screenshots/note_versions.png)

---

## 🌐 Live Application

- **Frontend (Live UI):**  
  https://notes-versions.onrender.com/static/index.html

- **Backend API Base URL:**  
  https://notes-versions.onrender.com/docs

---

## 🧠 Application Workflow

1. User registers or logs in

2. JWT token is stored in browser localStorage

3. User creates a note

4. Every update:

- Saves current state

- Creates a new version entry

5. User can:

- Preview versions (no DB write)

- Restore versions (creates a new version)

- Delete old versions

6. All routes are protected via auth dependency

--- 

## 📁 Project Folder Structure
```bash
project-notes/
│
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # DB session & engine
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication & JWT logic
│   ├── notes.py             # Notes CRUD + search
│   ├── versions.py          # Version history logic
│   └── static/
│       ├── css/style.css
│       ├── js/
│       │   ├── auth.js
│       │   ├── notes.js
│       │   └── note.js
│       ├── index.html
│       ├── notes.html
│       └── note.html
│
├── alembic/
│   ├── versions/            # Migration scripts
│   ├── env.py
│   └── script.py.mako
│
├── tests/                   # Pytest test suite
├── requirements.txt
├── alembic.ini
├── render.yaml              # Deployment config
├── .env.example
├── README.md
└── .gitignore
```

---

## ⚙️ Key Backend Files Explained

### main.py

- Creates FastAPI app

- Registers routers

- Mounts static files

- Enables CORS

### auth.py

- User registration & login

- Password hashing

- JWT token creation

- get_current_user dependency

### notes.py

- Create / read / update / delete notes

- Search notes by title

- Ownership validation

### versions.py

- List note versions

- Preview versions

- Restore versions (creates new version)

- Delete versions safely

### models.py

- User, Note, NoteVersion models

- Relationships and constraints

### schemas.py

- Request/response validation

- Clean API contracts

---

## 🛠 Setup & Run (Local)
### 1️⃣ Clone the repo
```
git clone https://github.com/AlenKJ01/Notes-Versions.git
cd project-notes
```
### 2️⃣ Create virtual environment
```
python -m venv venv
venv\Scripts\activate
```
### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```
### 4️⃣ Configure environment variables

Create .env using .env.example:
```
DATABASE_URL=postgresql://user:password@localhost:5432/notes_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
### 5️⃣ Run migrations
```
alembic upgrade head
```
### 6️⃣ Start the app
```
uvicorn app.main:app --reload
```

Open:

- API docs: http://127.0.0.1:8000/docs

- UI: http://127.0.0.1:8000/static/index.html

## 🚀 Deployment

The application is deployed using **Render (Backend)** and **Neon (PostgreSQL)**.

- **Frontend:**  
  Served as static files via FastAPI  
  https://notes-versions.onrender.com/static/index.html

- **Backend API:**  
  https://notes-versions.onrender.com/docs

- **Database:**  
  PostgreSQL hosted on Neon

### Production command:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📚 API Documentation Summary

### Base URL:
```bash
/auth
/notes
/notes/{id}/versions
```
### Auth

- POST /auth/register

- POST /auth/login

### Notes

- GET /notes

- POST /notes

- GET /notes/{id}

- PUT /notes/{id}

- DELETE /notes/{id}

- GET /notes?title=<search>

### Versions

- GET /notes/{id}/versions

- POST /notes/{id}/versions/{version}/restore

- DELETE /notes/{id}/versions/{version}

All protected routes require:
```
Authorization: Bearer <token>
```


