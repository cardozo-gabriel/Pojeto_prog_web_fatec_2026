from typing import Optional

from pydantic import BaseModel


class PartidaCreate(BaseModel):
    tipo_partida: str
    data_hora: str
    local: str
    status: str = "Aberta"


class PartidaUpdate(BaseModel):
    tipo_partida: Optional[str] = None
    data_hora: Optional[str] = None
    local: Optional[str] = None
    status: Optional[str] = None


class PartidaOut(BaseModel):
    id: int
    tipo_partida: str
    data_hora: str
    local: str
    criado_por: int
    status: str

    model_config = {"from_attributes": True}
