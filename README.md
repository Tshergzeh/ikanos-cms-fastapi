# ikanos-cms-fastapi

# Administrative Backend System (FastAPI)

This is a backend system built with **FastAPI**, designed to support real-time content updates for a website. It offers structured APIs for managing content and includes **role-based access control (RBAC)** for granular permissions across different user roles.

> This project is still a work in progress — contributions and feedback are welcome.

---

## Features

- RESTful APIs for content management (e.g. services, projects, and categories)
- Role-based access control:
  - **Admin**: Full control (auto-publish, approve editor submissions)
  - **Editor**: Create/update content (requires admin approval)
- PostgreSQL integration for data storage
- Clean and modular code structure using FastAPI best practices
- Pydantic models for request validation and response serialization

---

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **Auth**: JWT with role-based permissions
- **Environment**: Python 3.11+, Uvicorn

---

## Project Structure

app/
│
├── models/ # Pydantic models
├── routes/ # API routes
├── config.py # Define settings
├── db.py # Database connection logic
├── main.py # Entry point

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Tshergzeh/ikanos-cms-fastapi.git
cd ikanos-cms-fastapi
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to explore the auto-generated Swagger docs.

---

## Authentication & Roles

- Admin: Can create, update, delete, and auto-publish content.
- Editor: Can create or edit content, but changes require admin approval.

---

## License

MIT License. Feel free to fork, clone, and contribute.

---

## Author

Built by Oluwasegun Ige. I am open to remote and hybrid software engineering roles.

---