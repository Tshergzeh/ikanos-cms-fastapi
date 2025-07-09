from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.concurrency import asynccontextmanager
from fastapi.params import Body
import sqlalchemy
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.config import settings

DB_URL = settings.database_url

engine = create_engine(DB_URL)

class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    password: str = Field()
    is_admin: bool | None = Field(default=False)

class Service(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field()
    description: str = Field()
    image: str = Field()
    created_by: str = Field()
    last_modified_by: str = Field()
    is_published: bool = Field(default=False)
    approved_by: str | None = Field()
    approved_at: datetime | None = Field()

class ServiceUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    image: str | None = None
    last_modified_by: str 
    is_published: bool = False

class ServiceApproveInput(SQLModel):
    approved_by: str 

class ServiceApproveFinal(ServiceUpdate):
    last_modified_by: str
    is_published: bool = True
    approved_by: str
    approved_at: datetime = datetime.now()

class Category(SQLModel, table=True):
    category_id: int | None = Field(default=None, primary_key=True)
    category_name: str = Field(index=True)

class Project(SQLModel, table=True):
    project_id: int | None = Field(default=None, primary_key=True)
    project_image: str = Field()
    category_id: int = Field(index=True)
    created_by: str = Field()
    last_modified_by: str = Field()
    is_published: bool = Field(index=True, default=False)
    approved_by: str | None = Field()
    approved_at: datetime | None = Field()

class ProjectUpdate(SQLModel):
    project_image: str | None = None
    category_id: str | None = None
    last_modified_by: str | None = None
    is_published: bool | None = None
    approved_by: str | None = None
    approved_at: datetime | None = None

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# @app.get("/test")
# async def test_endpoint():
#     return {"status": "ok"}

@app.get("/health/db")
def test_db(session: Session = Depends(get_session)):
    print("✅ Running DB health check...")
    with session.get_bind().connect() as conn:
        db_name = conn.execute(sqlalchemy.text("SELECT current_database();")).scalar()
        print("🎯 Connected to DB:", db_name)
    try:
        statement = select(Service).where(Service.is_published == True)
        results = session.exec(statement).all()
        return {
            "success": True,
            "record_count": len(results)
        }
    except Exception as e:
        print("❌ DB Error:", e)
        return {
            "success": False,
            "error": str(e)
        }

# Authentication and Authorization

@app.post("/auth/login")
def login_user(user: User, session: SessionDep):
    query = select(User).where(
        User.username == user.username, 
        User.password == user.password
    )
    valid_user = session.exec(query).first()
    if not valid_user:
        raise HTTPException(
            403, 
            "Login failed. Invalid authentication details."
        )
    return {
        "success": True,
        "message": "You have been successfully logged in",
        "data": "jwt_token"
    }
    
@app.post("/auth/logout")
def logout_user():
    # token str
    return {
        "success": True,
        "message": "User logged out successfully"
    }

@app.get("/auth/me")
def get_current_user():
    return {
        "success": True,
        "message": "User details returned successfully",
        "data": {
            "username": "username",
            "is_admin": "is_admin"
        }
    }

# User Management

@app.get("/users")
def get_all_users(session: SessionDep):
    users = session.exec(select(User)).all()
    secure_users = []
    for user in users:
        secure_users.append({
            "username": user.username,
            "is_admin": user.is_admin
        })
    return {
        "success": True,
        "message": "All user details returned successfully",
        "data": secure_users
    }

@app.get("/users/{username}")
def get_user_by_username(username: str, session: SessionDep):
    user = session.get(User, username)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"User {username} does not exist"
        )
    return {
        "success": True,
        "message": "user details returned successfully",
        "data": {
            "username": f"{username}",
            "is_admin": user.is_admin
        }
    }

@app.post("/users")
def create_user(user:User, session: SessionDep, response: Response):
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(
            status.HTTP_409_CONFLICT, 
            f"User {user.username} already exists"
        )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, 
            f"User creation failed with error: {e}"
        )
    response.status_code = status.HTTP_201_CREATED
    return {
        "success": True,
        "message": "User created successfully"
    }

@app.delete("/users/{username}")
def delete_user(username: str, session: SessionDep, response: Response):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    session.delete(user)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
        
# Services

@app.get("/services")
def list_all_published_services(response: Response, session: SessionDep):
    services = session.exec(
        select(Service).where(Service.is_published == True)
    ).all()
    if not services:
        response.status_code = status.HTTP_204_NO_CONTENT
    return {
        "success": True,
        "message": "All published services returned successfully",
        "data": services
    }

@app.get("/admin/services")
def list_all_services(session: SessionDep, response: Response):
    services = session.exec(select(Service)).all()
    if not services:
        response.status_code = status.HTTP_204_NO_CONTENT
    return {
        "success": True,
        "message": "All services returned successfully",
        "data": services
    }

@app.post("/admin/services")
def create_new_service(
    service: Service, 
    response: Response, 
    session: SessionDep
    ):
    try:
        session.add(service)
        session.commit()
        session.refresh(service)
        response.status_code = status.HTTP_201_CREATED
        return {
            "success": True,
            "message": "Service created successfully",
            "data": service
        }
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, 
            f"Service creation failed with error {e}"
        )

@app.patch("/admin/services/{id}/approve")
def approve_service(
    id: int, 
    service_input: ServiceApproveInput, 
    session: SessionDep
):
    service_db = session.get(Service, id)
    if not service_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")

    user = session.get(User, service_input.approved_by)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User does not exist")
    if user.is_admin == 0:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, 
            "User not permitted to approve"
        )
    service_db.is_published = True
    service_db.approved_by = service_input.approved_by
    service_db.last_modified_by = service_input.approved_by
    service_db.approved_at = datetime.now()
    
    session.add(service_db)
    session.commit()
    session.refresh(service_db)
    return {
        "success": True,
        "message": f"Service {id} approved successfully"
    }

@app.patch("/admin/services/{id}")
def update_service(id: int, service: ServiceUpdate, session: SessionDep):
    service_db = session.get(Service, id)
    user = session.get(User, service.last_modified_by)
    if not (user):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User does not exist")
    if not service_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")
    service.is_published = False
    service_data = service.model_dump(exclude_unset=True)
    service_db.sqlmodel_update(service_data)
    session.add(service_db)
    print(service_db)
    if user.is_admin == True:
        print("Admin code starts here")
        approver = ServiceApproveInput(approved_by=user.username)
        if approve_service(id, approver, session):
            return {
                "success": True,
                "message": f"Service {id} with name '{service.title}' updated and approved successfully"
            }
    session.commit()
    session.refresh(service_db)
    return {
        "success": True,
        "message": f"Service {id} with name '{service.title}' updated successfully"
    }

@app.delete("/admin/services/{id}")
def delete_service(id: int, session: SessionDep, response: Response):
    service = session.get(Service, id)
    if not service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")
    session.delete(service)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT

# Project categories

@app.get("/categories")
def list_all_categories(response: Response, session: SessionDep):
    categories = session.exec(select(Category)).all()
    if not categories:
        response.status_code = status.HTTP_204_NO_CONTENT
    return {
        "success": True,
        "message": "All project categories returned successfully",
        "data": categories
    }

@app.post("/admin/categories")
def add_category(category: Category, response: Response, session: SessionDep):
    try:
        session.add(category)
        session.commit()
        session.refresh(category)
        response.status_code = status.HTTP_201_CREATED
        return {
            "success": True,
            "message": "Category added successfully",
            "data": category
        }
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, 
            f"Category addition failed with error {e}"
        )

@app.delete("/admin/categories/{id}")
def delete_category(id: int, session: SessionDep, response: Response):
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    session.delete(category)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT

# Projects

@app.get("/projects")
def list_all_published_projects(response: Response, session: SessionDep):
    projects = session.exec(
        select(Project).where(Project.is_published == True)
    ).all()
    if not projects:
        response.status_code = 204
    return projects

@app.get("/admin/projects")
def list_all_projects(session: SessionDep, response: Response):
    projects = session.exec(select(Project)).all()
    if not projects:
        response.status_code = status.HTTP_204_NO_CONTENT
    return {
        "success": True,
        "message": "All projects returned successfully",
        "data": projects
    }

@app.post("/admin/projects")
def add_project(project: Project, response: Response, session: SessionDep):
    try:
        session.add(project)
        session.commit()
        session.refresh(project)
        response.status_code = status.HTTP_201_CREATED
        return {
            "success": True,
            "message": "Project created successfully",
            "data": project
        }
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, 
            f"Project addition failed with error {e}"
        )

@app.patch("/admin/projects/{id}")
def edit_project_category(id: int, payload: dict = Body(...)):
    return {
        "success": True,
        "message": f"Project {id} edited successfully"
    }

@app.delete("/admin/projects/{id}")
def delete_project(id: int, response: Response, session: SessionDep):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    session.delete(project)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT

@app.patch("/admin/projects/{id}/approve")
def approve_project(id: int):
    return {
        "success": True,
        "message": f"Project {id} approved successfully"
    }
