from pathlib import Path

path = Path('app/routes/jogadores_routes.py')
text = path.read_text(encoding='utf-8')
text = text.replace(
    'from app.schemas.jogadores_schema import JogadorCreate, JogadorOut',
    'from app.schemas.jogadores_schema import JogadorCreate, JogadorOut, JogadorUpdate'
)
insert = "\n\n@router.put(\"/{jogador_id}\", response_model=dict)\ndef atualizar_jogador(jogador_id: int, payload: JogadorUpdate, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n    usuario = db.query(Usuario).filter(Usuario.email == email).first()\n    if not usuario:\n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Token inválido\")\n\n    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()\n    if not jogador:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Jogador não encontrado\")\n\n    update_data = payload.model_dump(exclude_none=True)\n    for key, value in update_data.items():\n        setattr(jogador, key, value)\n\n    db.commit()\n    db.refresh(jogador)\n    return {\"message\": \"Jogador atualizado com sucesso\"}\n\n\n@router.delete(\"/{jogador_id}\", response_model=dict)\ndef deletar_jogador(jogador_id: int, email: str = Depends(get_current_user), db: Session = Depends(get_db)):\n    usuario = db.query(Usuario).filter(Usuario.email == email).first()\n    if not usuario:\n        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=\"Token inválido\")\n\n    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()\n    if not jogador:\n        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Jogador não encontrado\")\n\n    db.delete(jogador)\n    db.commit()\n    return {\"message\": \"Jogador deletado com sucesso\"}\n"
text = text.replace('return db.query(Jogador).all()\n', 'return db.query(Jogador).all()\n' + insert)
path.write_text(text, encoding='utf-8')
print('updated jogadores_routes.py')
