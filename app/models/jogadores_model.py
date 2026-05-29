from sqlalchemy import Column, Integer, String

from app.config.database import Base


class Jogador(Base):
    __tablename__ = "jogadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    habilidade_ataque = Column(Integer, nullable=False)
    habilidade_defesa = Column(Integer, nullable=False)
    habilidade_meio = Column(Integer, nullable=False)
