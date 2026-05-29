from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.security import create_access_token, get_current_user, get_password_hash, verify_password
from app.config.settings import settings
from app.models.usuario_model import Usuario
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.schemas.usuario_schema import UsuarioCreate, UsuarioOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=dict)
def register_user(payload: UsuarioCreate, db: Session = Depends(get_db)):
    existing = db.query(Usuario).filter(Usuario.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

    usuario = Usuario(
        nome=payload.nome,
        email=payload.email,
        senha=get_password_hash(payload.senha),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return {"message": "Usuário cadastrado com sucesso"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == payload.email).first()
    if not usuario or not verify_password(payload.senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    token = create_access_token(data={"sub": usuario.email}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UsuarioOut)
def get_me(email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario


@router.delete("/me", response_model=dict)
def delete_current_user(email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    db.delete(usuario)
    db.commit()
    return {"message": "Usuário deletado com sucesso"}
