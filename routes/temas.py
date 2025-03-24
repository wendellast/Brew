from typing import List

from auth.auth import get_current_user
from controller import controller as crud
from fastapi import APIRouter, Depends, HTTPException
from models import models
from schemas import schemas
from settings.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/temas/", response_model=schemas.Tema)
def create_tema(
    tema: schemas.TemaCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_tema(db, tema, current_user.id)


@router.get("/temas/", response_model=List[schemas.Tema])
def read_temas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_temas_by_user(db, current_user.id, skip, limit)


@router.get("/temas/{tema_id}", response_model=schemas.Tema)
def read_tema(
    tema_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_tema = crud.get_tema(db, tema_id, current_user.id)
    if db_tema is None:
        raise HTTPException(status_code=404, detail="Tema not found")
    return db_tema


@router.put("/temas/{tema_id}", response_model=schemas.Tema)
def update_tema(
    tema_id: int,
    tema: schemas.TemaCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_tema = crud.update_tema(db, tema_id, tema, current_user.id)
    if db_tema is None:
        raise HTTPException(status_code=404, detail="Tema not found")
    return db_tema


@router.delete("/temas/{tema_id}")
def delete_tema(
    tema_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    success = crud.delete_tema(db, tema_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Tema not found")
    return {"detail": "Tema deleted successfully"}
