from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ..models.user import User
from app import db
from ..utils.auth_utils import verify_password, create_access_token

router = APIRouter()

@router.post("/api/auth/login", tags=["auth"])
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(db.get_session)
):
    user = session.get(User, form_data.username)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, 
            "Invalid credentials"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer"
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

