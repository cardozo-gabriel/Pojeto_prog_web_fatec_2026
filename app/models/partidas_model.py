from sqlalchemy import Column, ForeignKey, Integer, String

from app.config.database import Base


class Partida(Base):
    __tablename__ = "partidas"

    id = Column(Integer, primary_key=True, index=True)
    tipo_partida = Column(String, nullable=False)
    data_hora = Column(String, nullable=False)
    local = Column(String, nullable=False)
    criado_por = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(String, nullable=False, default="Aberta")
