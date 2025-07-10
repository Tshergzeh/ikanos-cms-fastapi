from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import select

from app.models.category import Category
from app import db

router = APIRouter()

@router.get("/api/categories", tags=["categories"])
def list_all_categories(response: Response, session: db.SessionDep):
    categories = session.exec(select(Category)).all()
    if not categories:
        response.status_code = status.HTTP_204_NO_CONTENT
    return {
        "success": True,
        "message": "All project categories returned successfully",
        "data": categories
    }

@router.post("/api/admin/categories", tags=["categories"])
def add_category(category: Category, response: Response, session: db.SessionDep):
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
def delete_category(id: int, session: db.SessionDep, response: Response):
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    session.delete(category)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
