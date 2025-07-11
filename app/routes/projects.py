from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.models.project import Project
from app import db
from app.models.user import User
from app.utils.auth_utils import admin_check

router = APIRouter()

@router.get("/api/projects", tags=["projects"])
def list_all_published_projects(
    response: Response, 
    session: Session = Depends(db.get_session)
):
    projects = session.exec(
        select(Project).where(Project.is_published == True)
    ).all()
    if not projects:
        response.status_code = 204
    return projects

@router.get("/api/admin/projects", tags=["projects"])
def list_all_projects(
    response: Response, 
    session: Session = Depends(db.get_session)
):  
    projects = session.exec(select(Project)).all()
    if not projects:
        response.status_code = status.HTTP_204_NO_CONTENT
    return {
        "success": True,
        "message": "All projects returned successfully",
        "data": projects
    }

@router.post("/api/admin/projects", tags=["projects"])
def add_project(
    project: Project, response: Response, 
    session: Session = Depends(db.get_session)
):  
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

@router.patch("/api/admin/projects/{id}", tags=["projects"])
def edit_project_category(id: int):  
    return {
        "success": True,
        "message": f"Project {id} edited successfully"
    }

@router.delete("/api/admin/projects/{id}", tags=["projects"])
def delete_project(
    id: int, 
    response: Response, 
    session: Session = Depends(db.get_session)
):
    project = session.get(Project, id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")
    session.delete(project)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT

@router.patch("/api/admin/projects/{id}/approve", tags=["projects"])
def approve_project(id: int, current_user: User = Depends(admin_check)):
    return {
        "success": True,
        "message": f"Project {id} approved successfully"
    }
