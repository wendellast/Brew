from typing import List

from auth.auth import get_current_user
from controller import controller as crud
from fastapi import APIRouter, Depends, HTTPException
from models import models
from schemas import schemas
from settings.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/progress/", response_model=schemas.UserProgress)
def create_user_progress(
    progress: schemas.UserProgressCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_progress = crud.create_progress(db, progress, current_user.id)
    if db_progress is None:
        raise HTTPException(status_code=404, detail="Tema or Fase not found")
    return db_progress


@router.get("/progress/", response_model=List[schemas.UserProgress])
def read_user_progress(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return crud.get_progress_by_user(db, current_user.id)
