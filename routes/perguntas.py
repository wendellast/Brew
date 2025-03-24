import tempfile
from typing import List

from auth.auth import get_current_user
from controller import controller as crud
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from models import models
from schemas import schemas
from services.json_llm import generate_json_pdf
from settings.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/fases/{fase_id}/perguntas/", response_model=schemas.Pergunta)
def create_pergunta(
    fase_id: int,
    pergunta: schemas.PerguntaCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_pergunta = crud.create_pergunta(db, pergunta, fase_id, current_user.id)
    if db_pergunta is None:
        raise HTTPException(
            status_code=404, detail="Fase not found or validation error"
        )
    return db_pergunta


@router.get("/fases/{fase_id}/perguntas/", response_model=List[schemas.Pergunta])
def read_perguntas(
    fase_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_perguntas_by_fase(db, fase_id, current_user.id, skip, limit)


@router.get("/perguntas/{pergunta_id}", response_model=schemas.Pergunta)
def read_pergunta(
    pergunta_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_pergunta = crud.get_pergunta(db, pergunta_id, current_user.id)
    if db_pergunta is None:
        raise HTTPException(status_code=404, detail="Pergunta not found")
    return db_pergunta


@router.put("/perguntas/{pergunta_id}", response_model=schemas.Pergunta)
def update_pergunta(
    pergunta_id: int,
    pergunta: schemas.PerguntaCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    db_pergunta = crud.update_pergunta(db, pergunta_id, pergunta, current_user.id)
    if db_pergunta is None:
        raise HTTPException(
            status_code=404, detail="Pergunta not found or validation error"
        )
    return db_pergunta


@router.delete("/perguntas/{pergunta_id}")
def delete_pergunta(
    pergunta_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    success = crud.delete_pergunta(db, pergunta_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Pergunta not found")
    return {"detail": "Pergunta deleted successfully"}


@router.post("/perguntas/{pergunta_id}/check")
def check_answer(
    pergunta_id: int,
    alternativa_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = crud.check_resposta(db, pergunta_id, alternativa_id, current_user.id)
    return result


@router.post(
    "/fases/{fase_id}/perguntas/multiple", response_model=List[schemas.Pergunta]
)
async def create_multiple_perguntas_for_fase(
    fase_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_path = temp_file.name

    questions_data = await generate_json_pdf(temp_path)

    perguntas_list: List[schemas.PerguntaSimpleCreate] = questions_data

    """Create multiple questions for a phase at once"""
    result = crud.create_multiple_perguntas(
        db, perguntas_list, fase_id, current_user.id
    )
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Fase not found or validation error in questions data",
        )
    return result
