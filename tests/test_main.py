from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_inicio():

    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Bem-vindo ao TechFlow Enterprise"

def test_health():

    resposta = client.get("/health")

    assert resposta.status_code == 200


    assert resposta.json()["status"] == "ok"

    
    
    





