from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select

from app.models.category import Category
from app import db
from app.models.user import User
from app.utils.auth_utils import get_current_user

router = APIRouter()

@router.get("/api/categories", tags=["categories"])
def list_all_categories(
    response: Response, 
    session: Session = Depends(db.get_session)
):
    categories = session.exec(select(Category)).all()
    if not categories:
        response.status_code = status.HTTP_204_NO_CONTENT
    return {
        "success": True,
        "message": "All project categories returned successfully",
        "data": categories
    }

@router.post("/api/admin/categories", tags=["categories"])
def add_category(
    category: Category, 
    response: Response, 
    session: Session = Depends(db.get_session),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorised")
    
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

@router.delete("/api/admin/categories/{id}", tags=["categories"])
def delete_category(
    id: int, 
    response: Response,
    session: Session = Depends(db.get_session),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not authorised")
    
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    session.delete(category)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
