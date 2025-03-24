# models.py
from settings.database import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))

    temas = relationship("Tema", back_populates="owner")
    progress = relationship("UserProgress", back_populates="user")


class Tema(Base):
    __tablename__ = "temas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True)
    descricao = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="temas")
    fases = relationship("Fase", back_populates="tema", cascade="all, delete-orphan")


class Fase(Base):
    __tablename__ = "fases"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True)
    descricao = Column(Text, nullable=True)
    tema_id = Column(Integer, ForeignKey("temas.id"))

    tema = relationship("Tema", back_populates="fases")
    perguntas = relationship(
        "Pergunta", back_populates="fase", cascade="all, delete-orphan"
    )


class Pergunta(Base):
    __tablename__ = "perguntas"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text)
    fase_id = Column(Integer, ForeignKey("fases.id"))

    fase = relationship("Fase", back_populates="perguntas")
    alternativas = relationship(
        "Alternativa", back_populates="pergunta", cascade="all, delete-orphan"
    )


class Alternativa(Base):
    __tablename__ = "alternativas"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(Text)
    correta = Column(Boolean, default=False)
    pergunta_id = Column(Integer, ForeignKey("perguntas.id"))

    pergunta = relationship("Pergunta", back_populates="alternativas")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tema_id = Column(Integer, ForeignKey("temas.id"))
    fase_id = Column(Integer, ForeignKey("fases.id"))
    completed = Column(Boolean, default=False)
    score = Column(Integer, default=0)
    date_completed = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="progress")
