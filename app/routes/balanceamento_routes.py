from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.balanceador.balanceador import balancear_jogadores
from app.config.database import get_db
from app.config.security import get_current_user
from app.models.jogador_time_model import JogadorTime
from app.models.jogadores_model import Jogador
from app.models.partidas_model import Partida
from app.models.usuario_model import Usuario
from app.schemas.balanceamento_schema import BalanceamentoResponse

router = APIRouter(prefix="/balanceamento", tags=["balanceamento"])


@router.get("", response_model=BalanceamentoResponse)
def balancear_partida(partida_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada")

    confirmacoes = db.query(JogadorTime).filter(JogadorTime.partida_id == partida_id).all()
    if len(confirmacoes) != 12:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="É necessário confirmar exatamente 12 jogadores para balancear")

    jogadores = []
    for confirmacao in confirmacoes:
        jogador = db.query(Jogador).filter(Jogador.id == confirmacao.jogador_id).first()
        if not jogador:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jogador não encontrado")

        jogadores.append(
            {
                "nome": jogador.nome,
                "habilidade_ataque": jogador.habilidade_ataque,
                "habilidade_defesa": jogador.habilidade_defesa,
                "habilidade_meio": jogador.habilidade_meio,
            }
        )

    resultado = balancear_jogadores(jogadores)
    return BalanceamentoResponse(
        time_1=resultado["time_1"],
        time_2=resultado["time_2"],
        diferenca=resultado["diferenca"],
    )
