from fastapi import FastAPI
from app.routers.chamados import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def inicio():
    return {"mensagem": "Bem-vindo ao TechFlow Enterprise"}


@app.get("/health")
def verificar_saude():
    return {"status": "ok"}