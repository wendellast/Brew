from datetime import datetime, timezone
from typing import List

from models.models import Alternativa, Fase, Pergunta, Tema, User, UserProgress
from schemas.schemas import (
    FaseCreate,
    PerguntaCreate,
    PerguntaSimpleCreate,
    TemaCreate,
    UserCreate,
    UserProgressCreate,
)
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    """Retrieve a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """Retrieve a user by their username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Retrieve a user by their email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate, hashed_password: str):
    """Create a new user with a hashed password."""
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_temas_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Retrieve themes by user ID with optional pagination."""
    return (
        db.query(Tema).filter(Tema.owner_id == user_id).offset(skip).limit(limit).all()
    )


def get_tema(db: Session, tema_id: int, user_id: int):
    """Retrieve a theme by its ID and user ID."""
    return db.query(Tema).filter(Tema.id == tema_id, Tema.owner_id == user_id).first()


def create_tema(db: Session, tema: TemaCreate, user_id: int):
    """Create a new theme for a user."""
    db_tema = Tema(nome=tema.nome, descricao=tema.descricao, owner_id=user_id)
    db.add(db_tema)
    db.commit()
    db.refresh(db_tema)
    return db_tema


def update_tema(db: Session, tema_id: int, tema: TemaCreate, user_id: int):
    """Update an existing theme."""
    db_tema = get_tema(db, tema_id, user_id)
    if not db_tema:
        return None
    db_tema.nome = tema.nome
    db_tema.descricao = tema.descricao
    db.commit()
    db.refresh(db_tema)
    return db_tema


def delete_tema(db: Session, tema_id: int, user_id: int):
    """Delete a theme by its ID and user ID."""
    db_tema = get_tema(db, tema_id, user_id)
    if db_tema:
        db.delete(db_tema)
        db.commit()
        return True
    return False


def get_fases_by_tema(
    db: Session, tema_id: int, user_id: int, skip: int = 0, limit: int = 100
):
    """Retrieve phases by theme ID and user ID with optional pagination."""
    tema = get_tema(db, tema_id, user_id)
    if not tema:
        return []
    return (
        db.query(Fase).filter(Fase.tema_id == tema_id).offset(skip).limit(limit).all()
    )


def get_fase(db: Session, fase_id: int, user_id: int):
    """Retrieve a phase by its ID and user ID."""
    return (
        db.query(Fase)
        .join(Tema)
        .filter(Fase.id == fase_id, Tema.owner_id == user_id)
        .first()
    )


def create_fase(db: Session, fase: FaseCreate, tema_id: int, user_id: int):
    """Create a new phase for a theme."""
    tema = get_tema(db, tema_id, user_id)
    if not tema:
        return None
    db_fase = Fase(nome=fase.nome, descricao=fase.descricao, tema_id=tema_id)
    db.add(db_fase)
    db.commit()
    db.refresh(db_fase)
    return db_fase


def update_fase(db: Session, fase_id: int, fase: FaseCreate, user_id: int):
    """Update an existing phase."""
    db_fase = get_fase(db, fase_id, user_id)
    if not db_fase:
        return None
    db_fase.nome = fase.nome
    db_fase.descricao = fase.descricao
    db.commit()
    db.refresh(db_fase)
    return db_fase


def delete_fase(db: Session, fase_id: int, user_id: int):
    """Delete a phase by its ID and user ID."""
    db_fase = get_fase(db, fase_id, user_id)
    if db_fase:
        db.delete(db_fase)
        db.commit()
        return True
    return False


def get_perguntas_by_fase(
    db: Session, fase_id: int, user_id: int, skip: int = 0, limit: int = 100
):
    """Retrieve questions by phase ID and user ID with optional pagination."""
    fase = get_fase(db, fase_id, user_id)
    if not fase:
        return []
    return (
        db.query(Pergunta)
        .filter(Pergunta.fase_id == fase_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_pergunta(db: Session, pergunta_id: int, user_id: int):
    """Retrieve a question by its ID and user ID."""
    return (
        db.query(Pergunta)
        .join(Fase)
        .join(Tema)
        .filter(Pergunta.id == pergunta_id, Tema.owner_id == user_id)
        .first()
    )


def create_pergunta(db: Session, pergunta: PerguntaCreate, fase_id: int, user_id: int):
    """Create a new question for a phase."""
    fase = get_fase(db, fase_id, user_id)
    if not fase:
        return None
    if len(pergunta.alternativas) != 4:
        return None
    if sum(1 for alt in pergunta.alternativas if alt.correta) != 1:
        return None
    db_pergunta = Pergunta(texto=pergunta.texto, fase_id=fase_id)
    db.add(db_pergunta)
    db.commit()
    db.refresh(db_pergunta)
    for alt in pergunta.alternativas:
        db_alternativa = Alternativa(
            texto=alt.texto, correta=alt.correta, pergunta_id=db_pergunta.id
        )
        db.add(db_alternativa)
    db.commit()
    db.refresh(db_pergunta)
    return db_pergunta


def update_pergunta(
    db: Session, pergunta_id: int, pergunta: PerguntaCreate, user_id: int
):
    """Update an existing question."""
    db_pergunta = get_pergunta(db, pergunta_id, user_id)
    if not db_pergunta:
        return None
    if len(pergunta.alternativas) != 4:
        return None
    if sum(1 for alt in pergunta.alternativas if alt.correta) != 1:
        return None
    db_pergunta.texto = pergunta.texto
    db.query(Alternativa).filter(Alternativa.pergunta_id == pergunta_id).delete()
    for alt in pergunta.alternativas:
        db_alternativa = Alternativa(
            texto=alt.texto, correta=alt.correta, pergunta_id=db_pergunta.id
        )
        db.add(db_alternativa)
    db.commit()
    db.refresh(db_pergunta)
    return db_pergunta


def delete_pergunta(db: Session, pergunta_id: int, user_id: int):
    """Delete a question by its ID and user ID."""
    db_pergunta = get_pergunta(db, pergunta_id, user_id)
    if db_pergunta:
        db.delete(db_pergunta)
        db.commit()
        return True
    return False


def check_resposta(db: Session, pergunta_id: int, alternativa_id: int, user_id: int):
    """Check if an answer is correct."""
    pergunta = get_pergunta(db, pergunta_id, user_id)
    if not pergunta:
        return {"correta": False, "resposta_correta": None}
    alternativa = (
        db.query(Alternativa)
        .filter(
            Alternativa.pergunta_id == pergunta_id, Alternativa.id == alternativa_id
        )
        .first()
    )
    if not alternativa:
        return {"correta": False, "resposta_correta": None}
    if alternativa.correta:
        return {"correta": True}
    alternativa_correta = (
        db.query(Alternativa)
        .filter(Alternativa.pergunta_id == pergunta_id, Alternativa.correta.is_(True))
        .first()
    )
    return {
        "correta": False,
        "resposta_correta": alternativa_correta.id if alternativa_correta else None,
    }


def get_progress_by_user(db: Session, user_id: int):
    """Retrieve user progress by user ID."""
    return db.query(UserProgress).filter(UserProgress.user_id == user_id).all()


def create_progress(db: Session, progress: UserProgressCreate, user_id: int):
    """Create a new progress record for a user."""
    tema = get_tema(db, progress.tema_id, user_id)
    fase = get_fase(db, progress.fase_id, user_id)
    if not tema or not fase:
        return None
    db_progress = UserProgress(
        user_id=user_id,
        tema_id=progress.tema_id,
        fase_id=progress.fase_id,
        completed=progress.completed,
        score=progress.score,
        date_completed=datetime.now(timezone.utc) if progress.completed else None,
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


def create_multiple_perguntas(
    db: Session, perguntas_list: List[dict], fase_id: int, user_id: int
):
    """Create multiple questions associated with a phase."""
    perguntas_objs = []
    for pergunta_data in perguntas_list:
        pergunta_schema = PerguntaSimpleCreate(**pergunta_data)
        db_pergunta = Pergunta(texto=pergunta_schema.texto, fase_id=fase_id)
        db.add(db_pergunta)
        db.commit()
        db.refresh(db_pergunta)
        for alternativa_data in pergunta_schema.alternativas:
            db_alternativa = Alternativa(
                texto=alternativa_data.texto,
                correta=alternativa_data.correta,
                pergunta_id=db_pergunta.id,
            )
            db.add(db_alternativa)
        db.commit()
        db.refresh(db_pergunta)
        perguntas_objs.append(db_pergunta)
    return perguntas_objs
