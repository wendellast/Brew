from auth.auth import get_current_user, get_password_hash
from controller import controller as crud
from fastapi import APIRouter, Depends, HTTPException
from models import models
from schemas import schemas
from settings.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    return crud.create_user(db, user, hashed_password)


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
