from fastapi import FastAPI, Depends
from fastapi.concurrency import asynccontextmanager
import sqlalchemy
from sqlmodel import Session, select

from app.models.service import Service

from .routes import auth, users, services, categories, projects

from app import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# @app.get("/test")
# async def test_endpoint():
#     return {"status": "ok"}

@app.get("/health/db")
def test_db(session: Session = Depends(db.get_session)):
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

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(services.router)
app.include_router(categories.router)
app.include_router(projects.router)
