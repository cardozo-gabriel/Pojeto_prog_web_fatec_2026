from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.models.jogador_time_model import JogadorTime
from app.models.jogadores_model import Jogador
from app.models.partidas_model import Partida
from app.models.usuario_model import Usuario
from app.schemas.jogador_time_schema import JogadorConfirmadoOut, JogadorTimeCreate, JogadorTimeUpdate
from app.schemas.partidas_schema import PartidaCreate, PartidaOut, PartidaUpdate

router = APIRouter(prefix="/partidas", tags=["partidas"])


@router.post("", response_model=dict)
def criar_partida(payload: PartidaCreate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    partida = Partida(
        tipo_partida=payload.tipo_partida,
        data_hora=payload.data_hora,
        local=payload.local,
        criado_por=usuario.id,
        status=payload.status,
    )
    db.add(partida)
    db.commit()
    db.refresh(partida)
    return {"message": "Partida criada com sucesso"}


@router.post("/confirmar-jogador", response_model=dict)
def confirmar_jogador(payload: JogadorTimeCreate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    partida = db.query(Partida).filter(Partida.id == payload.partida_id).first()
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada")

    jogador = db.query(Jogador).filter(Jogador.id == payload.jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jogador não encontrado")

    existing = db.query(JogadorTime).filter(
        JogadorTime.partida_id == payload.partida_id,
        JogadorTime.jogador_id == payload.jogador_id,
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Jogador já confirmado nessa partida")

    count = db.query(JogadorTime).filter(JogadorTime.partida_id == payload.partida_id).count()
    if count >= 12:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Partida lotada")

    confirmado = JogadorTime(
        partida_id=payload.partida_id,
        jogador_id=payload.jogador_id,
        time=payload.time,
        posicao_selecionada=payload.posicao_selecionada,
    )
    db.add(confirmado)
    db.commit()
    return {"message": "Jogador confirmado na partida"}


@router.put("/confirmar-jogador/{confirmacao_id}", response_model=dict)
def atualizar_confirmacao(confirmacao_id: int, payload: JogadorTimeUpdate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    confirmacao = db.query(JogadorTime).filter(JogadorTime.id == confirmacao_id).first()
    if not confirmacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confirmação não encontrada")

    update_data = payload.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(confirmacao, key, value)

    db.commit()
    db.refresh(confirmacao)
    return {"message": "Confirmação atualizada com sucesso"}


@router.delete("/confirmar-jogador/{confirmacao_id}", response_model=dict)
def deletar_confirmacao(confirmacao_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    confirmacao = db.query(JogadorTime).filter(JogadorTime.id == confirmacao_id).first()
    if not confirmacao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Confirmação não encontrada")

    db.delete(confirmacao)
    db.commit()
    return {"message": "Confirmação deletada com sucesso"}


@router.get("", response_model=list[PartidaOut])
def listar_partidas(email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    return db.query(Partida).all()


@router.put("/{partida_id}", response_model=dict)
def atualizar_partida(partida_id: int, payload: PartidaUpdate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada")

    update_data = payload.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(partida, key, value)

    db.commit()
    db.refresh(partida)
    return {"message": "Partida atualizada com sucesso"}


@router.delete("/{partida_id}", response_model=dict)
def deletar_partida(partida_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada")

    db.query(JogadorTime).filter(JogadorTime.partida_id == partida_id).delete()
    db.delete(partida)
    db.commit()
    return {"message": "Partida deletada com sucesso"}


@router.get("/{partida_id}/confirmados", response_model=list[JogadorConfirmadoOut])
def listar_confirmados_partida(partida_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partida não encontrada")

    confirmacoes = (
        db.query(JogadorTime, Jogador)
        .join(Jogador, Jogador.id == JogadorTime.jogador_id)
        .filter(JogadorTime.partida_id == partida_id)
        .all()
    )

    return [
        JogadorConfirmadoOut(
            confirmacao_id=confirmacao.id,
            partida_id=confirmacao.partida_id,
            jogador_id=confirmacao.jogador_id,
            time=confirmacao.time,
            posicao_selecionada=confirmacao.posicao_selecionada,
            nome=jogador.nome,
            habilidade_ataque=jogador.habilidade_ataque,
            habilidade_defesa=jogador.habilidade_defesa,
            habilidade_meio=jogador.habilidade_meio,
        )
        for confirmacao, jogador in confirmacoes
    ]
