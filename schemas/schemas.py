from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator


class AlternativaBase(BaseModel):
    texto: str
    correta: bool


class AlternativaCreate(AlternativaBase):
    pass


class Alternativa(AlternativaBase):
    id: int
    pergunta_id: int

    class Config:
        orm_mode = True


class PerguntaBase(BaseModel):
    texto: str


class PerguntaCreate(PerguntaBase):
    alternativas: List[AlternativaCreate]

    @field_validator("alternativas")
    def exatamente_quatro_alternativas(cls, alternativas):
        if len(alternativas) != 4:
            raise ValueError("Cada pergunta deve ter exatamente 4 alternativas")
        if sum(alt.correta for alt in alternativas) != 1:
            raise ValueError("Deve haver exatamente 1 alternativa correta")
        return alternativas


class Pergunta(PerguntaBase):
    id: int
    fase_id: int
    alternativas: List[Alternativa]

    class Config:
        orm_mode = True


class FaseBase(BaseModel):
    nome: str
    descricao: Optional[str] = None


class FaseCreate(FaseBase):
    pass


class Fase(FaseBase):
    id: int
    tema_id: int
    perguntas: List[Pergunta] = []

    class Config:
        orm_mode = True


class TemaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None


class TemaCreate(TemaBase):
    pass


class Tema(TemaBase):
    id: int
    fases: List[Fase] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserProgressBase(BaseModel):
    tema_id: int
    fase_id: int
    completed: bool
    score: int


class UserProgressCreate(UserProgressBase):
    pass


class UserProgress(UserProgressBase):
    id: int
    user_id: int
    date_completed: Optional[datetime] = None

    class Config:
        orm_mode = True


class PerguntaSimpleCreate(BaseModel):
    texto: str
    alternativas: List[AlternativaCreate]

    @field_validator("alternativas")
    def exatamente_quatro_alternativas(cls, alternativas):
        if len(alternativas) != 4:
            raise ValueError("Cada pergunta deve ter exatamente 4 alternativas")
        if sum(alt.correta for alt in alternativas) != 1:
            raise ValueError("Deve haver exatamente 1 alternativa correta")
        return alternativas


class MultiplePerguntas(BaseModel):
    perguntas: List[PerguntaSimpleCreate]
