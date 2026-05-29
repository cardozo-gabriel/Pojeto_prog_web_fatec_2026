from typing import Optional

from pydantic import BaseModel


class JogadorCreate(BaseModel):
    nome: str
    habilidade_ataque: int
    habilidade_defesa: int
    habilidade_meio: int


class JogadorUpdate(BaseModel):
    nome: Optional[str] = None
    habilidade_ataque: Optional[int] = None
    habilidade_defesa: Optional[int] = None
    habilidade_meio: Optional[int] = None


class JogadorOut(BaseModel):
    id: int
    nome: str
    habilidade_ataque: int
    habilidade_defesa: int
    habilidade_meio: int

    model_config = {"from_attributes": True}
