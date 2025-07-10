from fastapi import HTTPException, status
from sqlmodel import Session

from ..models.user import User

def get_user(username: str, session: Session):
    user = session.get(User, username)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"User {username} does not exist"
        )
    return user
    