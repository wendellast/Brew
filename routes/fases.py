from typing import List

from auth.auth import get_current_user
from controller import controller as crud
from fastapi import APIRouter, Depends, HTTPException
from models import models
from schemas import schemas
from settings.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/temas/{tema_id}/fases/", response_model=schemas.Fase)
def create_fase(
    tema_id: int,
    fase: schemas.FaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_fase = crud.create_fase(db, fase, tema_id, current_user.id)
    if db_fase is None:
        raise HTTPException(
            status_code=404, detail="Tema not found or not owned by user"
        )
    return db_fase


@router.get("/temas/{tema_id}/fases/", response_model=List[schemas.Fase])
def read_fases(
    tema_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_fases_by_tema(db, tema_id, current_user.id, skip, limit)


@router.get("/fases/{fase_id}", response_model=schemas.Fase)
def read_fase(
    fase_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_fase = crud.get_fase(db, fase_id, current_user.id)
    if db_fase is None:
        raise HTTPException(status_code=404, detail="Fase not found")
    return db_fase


@router.put("/fases/{fase_id}", response_model=schemas.Fase)
def update_fase(
    fase_id: int,
    fase: schemas.FaseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_fase = crud.update_fase(db, fase_id, fase, current_user.id)
    if db_fase is None:
        raise HTTPException(status_code=404, detail="Fase not found")
    return db_fase


@router.delete("/fases/{fase_id}")
def delete_fase(
    fase_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    success = crud.delete_fase(db, fase_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Fase not found")
    return {"detail": "Fase deleted successfully"}
