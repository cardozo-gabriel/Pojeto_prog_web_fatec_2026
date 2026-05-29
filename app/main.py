from fastapi import FastAPI

from app.config.database import Base, engine
from app.models import jogador_time_model, jogadores_model, partidas_model, usuario_model
from app.routes.auth_routes import router as auth_router
from app.routes.balanceamento_routes import router as balanceamento_router
from app.routes.jogadores_routes import router as jogadores_router
from app.routes.partidas_routes import router as partidas_router

app = FastAPI(title="API de Agendamento e Balanceamento")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(jogadores_router)
app.include_router(partidas_router)
app.include_router(balanceamento_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
