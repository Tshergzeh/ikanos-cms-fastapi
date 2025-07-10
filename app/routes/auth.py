from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.models.user import User
from app import db

router = APIRouter()

@router.post("/api/auth/login", tags=["auth"])
def login_user(user: User, session: db.SessionDep):
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
    
@router.post("/api/auth/logout", tags=["auth"])
def logout_user():
    # token str
    return {
        "success": True,
        "message": "User logged out successfully"
    }

@router.get("/api/auth/me", tags=["auth"])
def get_current_user():
    return {
        "success": True,
        "message": "User details returned successfully",
        "data": {
            "username": "username",
            "is_admin": "is_admin"
        }
    }

