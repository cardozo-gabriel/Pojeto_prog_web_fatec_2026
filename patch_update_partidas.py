from pathlib import Path

path = Path('app/routes/partidas_routes.py')
text = path.read_text(encoding='utf-8')
text = text.replace(
    'from app.schemas.jogador_time_schema import JogadorConfirmadoOut, JogadorTimeCreate\nfrom app.schemas.partidas_schema import PartidaCreate, PartidaOut',
    'from app.schemas.jogador_time_schema import JogadorConfirmadoOut, JogadorTimeCreate, JogadorTimeUpdate\nfrom app.schemas.partidas_schema import PartidaCreate, PartidaOut, PartidaUpdate'
)
# Insert update/delete partida after listar_partidas
insert_partida = "\n\n@router.put(\"/{partida_id}\", response_model=dict)\ndef atualizar_partida(partida_id: int, payload: PartidaUpdate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n    usuario = db.query(Usuario).filter(Usuario.email == email).first()\n    if not usuario:\n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Token inválido\")\n\n    partida = db.query(Partida).filter(Partida.id == partida_id).first()\n    if not partida:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Partida não encontrada\")\n\n    update_data = payload.model_dump(exclude_none=True)\n    for key, value in update_data.items():\n        setattr(partida, key, value)\n\n    db.commit()\n    db.refresh(partida)\n    return {\"message\": \"Partida atualizada com sucesso\"}\n\n\n@router.delete(\"/{partida_id}\", response_model=dict)\ndef deletar_partida(partida_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n    usuario = db.query(Usuario).filter(Usuario.email == email).first()\n    if not usuario:\n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Token inválido\")\n\n    partida = db.query(Partida).filter(Partida.id == partida_id).first()\n    if not partida:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Partida não encontrada\")\n\n    db.query(JogadorTime).filter(JogadorTime.partida_id == partida_id).delete()\n    db.delete(partida)\n    db.commit()\n    return {\"message\": \"Partida deletada com sucesso\"}\n"
text = text.replace('@router.get("", response_model=list[PartidaOut])', '@router.get("", response_model=list[PartidaOut])')
# Insert before the final route definition maybe after listar_partidas block
marker = '    return db.query(Partida).all()\n\n\n@router.get("/{partida_id}/confirmados", response_model=list[JogadorConfirmadoOut])\n'
text = text.replace(marker, marker + insert_partida)
# Update confirmar_jogador block with capacity and duplicate checks, and add update/delete confirmacao endpoints
old_confirm = "@router.post(\"/confirmar-jogador\", response_model=dict)\ndef confirmar_jogador(payload: JogadorTimeCreate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n    usuario = db.query(Usuario).filter(Usuario.email == email).first()\n    if not usuario:\n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Token inválido\")\n\n    partida = db.query(Partida).filter(Partida.id == payload.partida_id).first()\n    if not partida:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Partida não encontrada\")\n\n    jogador = db.query(Jogador).filter(Jogador.id == payload.jogador_id).first()\n    if not jogador:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Jogador não encontrado\")\n\n    confirmado = JogadorTime(\n        partida_id=payload.partida_id,\n        jogador_id=payload.jogador_id,\n        time=payload.time,\n        posicao_selecionada=payload.posicao_selecionada,\n    )\n    db.add(confirmado)\n    db.commit()\n    return {\"message\": \"Jogador confirmado na partida\"}\n\n\n@router.get("/{partida_id}/confirmados", response_model=list[JogadorConfirmadoOut])\ndef listar_confirmados_partida(partida_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n"
replace_confirm = "@router.post(\"/confirmar-jogador\", response_model=dict)\ndef confirmar_jogador(payload: JogadorTimeCreate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n    usuario = db.query(Usuario).filter(Usuario.email == email).first()\n    if not usuario:\n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Token inválido\")\n\n    partida = db.query(Partida).filter(Partida.id == payload.partida_id).first()\n    if not partida:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Partida não encontrada\")\n\n    jogador = db.query(Jogador).filter(Jogador.id == payload.jogador_id).first()\n    if not jogador:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Jogador não encontrado\")\n\n    existing = db.query(JogadorTime).filter(JogadorTime.partida_id == payload.partida_id, JogadorTime.jogador_id == payload.jogador_id).first()\n    if existing:\n        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=\"Jogador já confirmado nessa partida\")\n\n    count = db.query(JogadorTime).filter(JogadorTime.partida_id == payload.partida_id).count()\n    if count >= 12:\n        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=\"Partida lotada\")\n\n    confirmado = JogadorTime(\n        partida_id=payload.partida_id,\n        jogador_id=payload.jogador_id,\n        time=payload.time,\n        posicao_selecionada=payload.posicao_selecionada,\n    )\n    db.add(confirmado)\n    db.commit()\n    return {\"message\": \"Jogador confirmado na partida\"}\n\n\n@router.put(\"/confirmar-jogador/{confirmacao_id}\", response_model=dict)\ndef atualizar_confirmacao(confirmacao_id: int, payload: JogadorTimeUpdate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n    usuario = db.query(Usuario).filter(Usuario.email == email).first()\n    if not usuario:\n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Token inválido\")\n\n    confirmacao = db.query(JogadorTime).filter(JogadorTime.id == confirmacao_id).first()\n    if not confirmacao:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Confirmação não encontrada\")\n\n    update_data = payload.model_dump(exclude_none=True)
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


@router.get("/{partida_id}/confirmados", response_model=list[JogadorConfirmadoOut])
def listar_confirmados_partida(partida_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n"
text = text.replace(old_confirm, replace_confirm)
path.write_text(text, encoding='utf-8')
print('updated partidas_routes.py')
