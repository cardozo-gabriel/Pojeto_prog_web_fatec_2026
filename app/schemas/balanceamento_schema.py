from pydantic import BaseModel


class JogadorBalanceado(BaseModel):
    nome: str
    posicao: str


class BalanceamentoResponse(BaseModel):
    time_1: list[JogadorBalanceado]
    time_2: list[JogadorBalanceado]
    diferenca: float
