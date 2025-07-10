from fastapi import APIRouter, HTTPException, Response, status
import sqlalchemy
from sqlmodel import select

from app.models.user import User
from app import db

router = APIRouter()

@router.get("/api/users", tags=["users"])
def get_all_users(session: db.SessionDep):
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

@router.get("/api/users/{username}", tags=["users"])
def get_user_by_username(username: str, session: db.SessionDep):
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

@router.post("/api/users", tags=["users"])
def create_user(user:User, session: db.SessionDep, response: Response):
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

@router.delete("/api/users/{username}", tags=["users"])
def delete_user(username: str, session: db.SessionDep, response: Response):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    session.delete(user)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
        