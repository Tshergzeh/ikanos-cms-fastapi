from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel
from typing import Annotated

from app.config import settings

DB_URL = settings.database_url

engine = create_engine(DB_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
