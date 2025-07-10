from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select
from datetime import datetime

from app.models.user import User
from app.models.service import Service, ServiceUpdate, ServiceApproveInput
from app import db

router = APIRouter()

@router.get("/api/services", tags=["services"])
def list_all_published_services(response: Response, session: db.SessionDep):
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

@router.get("/api/admin/services", tags=["services"])
def list_all_services(session: db.SessionDep, response: Response):
    services = session.exec(select(Service)).all()
    if not services:
        response.status_code = status.HTTP_204_NO_CONTENT
    return {
        "success": True,
        "message": "All services returned successfully",
        "data": services
    }

@router.post("/api/admin/services", tags=["services"])
def create_new_service(
    service: Service, 
    response: Response, 
    session: db.SessionDep
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

@router.patch("/api/admin/services/{id}/approve", tags=["services"])
def approve_service(
    id: int, 
    service_input: ServiceApproveInput, 
    session: db.SessionDep
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

@router.patch("/api/admin/services/{id}", tags=["services"])
def update_service(id: int, service: ServiceUpdate, session: db.SessionDep):
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

@router.delete("/api/admin/services/{id}", tags=["services"])
def delete_service(id: int, session: db.SessionDep, response: Response):
    service = session.get(Service, id)
    if not service:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Service not found")
    session.delete(service)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
