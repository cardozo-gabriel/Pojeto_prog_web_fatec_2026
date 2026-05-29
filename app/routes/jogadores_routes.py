from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import get_current_user
from app.models.jogador_time_model import JogadorTime
from app.models.jogadores_model import Jogador
from app.models.partidas_model import Partida
from app.models.usuario_model import Usuario
from app.schemas.jogadores_schema import JogadorCreate, JogadorOut, JogadorUpdate

router = APIRouter(prefix="/jogadores", tags=["jogadores"])


@router.post("", response_model=dict)
def cadastrar_jogador(payload: JogadorCreate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    jogador = Jogador(**payload.model_dump())
    db.add(jogador)
    db.commit()
    db.refresh(jogador)
    return {"message": "Jogador cadastrado com sucesso"}


@router.get("", response_model=list[JogadorOut])
def listar_jogadores(email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    return db.query(Jogador).all()


@router.put("/{jogador_id}", response_model=dict)
def atualizar_jogador(jogador_id: int, payload: JogadorUpdate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jogador não encontrado")

    update_data = payload.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(jogador, key, value)

    db.commit()
    db.refresh(jogador)
    return {"message": "Jogador atualizado com sucesso"}


@router.delete("/{jogador_id}", response_model=dict)
def deletar_jogador(jogador_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jogador não encontrado")

    db.delete(jogador)
    db.commit()
    return {"message": "Jogador deletado com sucesso"}
