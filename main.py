
from fastapi import FastAPI
from app.routers.user import user_router
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/api", tags=["users"])