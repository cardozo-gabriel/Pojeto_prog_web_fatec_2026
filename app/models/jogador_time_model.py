from sqlalchemy import Column, ForeignKey, Integer, String

from app.config.database import Base


class JogadorTime(Base):
    __tablename__ = "jogador_time"

    id = Column(Integer, primary_key=True, index=True)
    partida_id = Column(Integer, ForeignKey("partidas.id"), nullable=False)
    jogador_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    time = Column(Integer, nullable=False)
    posicao_selecionada = Column(String, nullable=False)
