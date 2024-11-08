
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema.user import User, UserCreate
from app.models.models import User as UserModel
from app.db.database import SessionLocal
import bcrypt
from typing import List
user_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    new_user = UserModel(name=user.name, email=user.email, password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user_router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/users/", response_model=list[User])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users
