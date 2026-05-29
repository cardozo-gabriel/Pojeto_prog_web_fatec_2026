from typing import Optional

from pydantic import BaseModel


class JogadorTimeCreate(BaseModel):
    partida_id: int
    jogador_id: int
    time: int
    posicao_selecionada: str


class JogadorTimeUpdate(BaseModel):
    time: Optional[int] = None
    posicao_selecionada: Optional[str] = None


class JogadorTimeOut(BaseModel):
    id: int
    partida_id: int
    jogador_id: int
    time: int
    posicao_selecionada: str

    model_config = {"from_attributes": True}


class JogadorConfirmadoOut(BaseModel):
    confirmacao_id: int
    partida_id: int
    jogador_id: int
    time: int
    posicao_selecionada: str
    nome: str
    habilidade_ataque: int
    habilidade_defesa: int
    habilidade_meio: int

    model_config = {"from_attributes": True}
