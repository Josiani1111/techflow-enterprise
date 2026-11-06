import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers.chamados import chamados_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpar_chamados():
    chamados_db.clear()
    yield
    chamados_db.clear()


def test_listar_chamados():
    resposta = client.get("/chamados")

    assert resposta.status_code == 200
    assert "chamados" in resposta.json()


def test_criar_chamado():
    novo_chamado = {
        "solicitante": "Maria",
        "problema": "Computador nÃ£o liga",
        "prioridade": "Alta"
    }

    resposta = client.post("/chamados", json=novo_chamado)

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Chamado criado com sucesso"

    dados = resposta.json()["chamado"]

    assert dados["solicitante"] == "Maria"
    assert dados["problema"] == "Computador nÃ£o liga"
    assert dados["prioridade"] == "Alta"


def test_criar_chamado_sem_solicitante():
    novo_chamado = {
        "problema": "Computador nÃ£o liga",
        "prioridade": "Alta"
    }

    resposta = client.post("/chamados", json=novo_chamado)

    assert resposta.status_code == 422
    assert "detail" in resposta.json()


def test_criar_chamado_sem_prioridade():
    novo_chamado = {
        "solicitante": "Carlos",
        "problema": "Internet nÃ£o funciona"
    }

    resposta = client.post("/chamados", json=novo_chamado)

    assert resposta.status_code == 422
    assert "detail" in resposta.json()


def test_chamado_aparece_na_listagem():
    novo_chamado = {
        "solicitante": "Ana",
        "problema": "Sem acesso ao sistema",
        "prioridade": "Media"
    }

    resposta = client.post("/chamados", json=novo_chamado)
    assert resposta.status_code == 200

    resposta_lista = client.get("/chamados")
    assert resposta_lista.status_code == 200

    chamados = resposta_lista.json()["chamados"]

    assert resposta.json()["chamado"] in chamados

def test_criar_chamado_campos_vazios():
    novo_chamado = {
        "solicitante": "",
        "problema": "",
        "prioridade": ""
    }

    resposta = client.post("/chamados", json=novo_chamado)

    assert resposta.status_code == 422
    assert "detail" in resposta.json()

    
def test_criar_chamado_somente_espacos():
    novo_chamado = {
        "solicitante": "   ",
        "problema": "   ",
        "prioridade": "   "
    }

    resposta = client.post("/chamados", json=novo_chamado)

    assert resposta.status_code == 422
    assert "detail" in resposta.json()

def test_criar_chamado_prioridade_invalida():
    novo_chamado = {
        "solicitante": "Pedro",
        "problema": "Sistema lento",
        "prioridade": "Urgentissima"
    }

    resposta = client.post("/chamados", json=novo_chamado)

    assert resposta.status_code == 422
    assert "detail" in resposta.json()

def test_erro_identifica_campo_prioridade():
    novo_chamado = {
        "solicitante": "Pedro",
        "problema": "Sistema lento",
        "prioridade": "Urgentissima"
    }

    resposta = client.post("/chamados", json=novo_chamado)

    assert resposta.status_code == 422

    erros = resposta.json()["detail"]

    assert any(
        "prioridade" in erro["loc"]
        for erro in erros
    )

def test_criar_chamado_com_id():
    novo_chamado = {
        "solicitante": "Carlos",
        "problema": "Impressora não funciona",
        "prioridade": "Alta"
    }

    resposta = client.post("/chamados", json=novo_chamado)

    assert resposta.status_code == 200

    dados = resposta.json()["chamado"]

    assert dados["id"] == 1
    assert dados["solicitante"] == "Carlos"

def test_consultar_chamado_por_id():
    novo_chamado = {
        "solicitante": "Ana",
        "problema": "Internet lenta",
        "prioridade": "Alta"
    }

    cadastro = client.post("/chamados", json=novo_chamado)

    assert cadastro.status_code == 200

    chamado_id = cadastro.json()["chamado"]["id"]

    resposta = client.get(f"/chamados/{chamado_id}")

    assert resposta.status_code == 200
    assert resposta.json()["id"] == chamado_id
    assert resposta.json()["solicitante"] == "Ana"

def test_consultar_chamado_inexistente():
    resposta = client.get("/chamados/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Chamado não encontrado"

def test_atualizar_chamado():
    novo_chamado = {
        "solicitante": "Maria",
        "problema": "Computador lento",
        "prioridade": "Baixa"
    }

    cadastro = client.post("/chamados", json=novo_chamado)
    assert cadastro.status_code == 200

    chamado_id = cadastro.json()["chamado"]["id"]

    dados_atualizados = {
        "solicitante": "Maria",
        "problema": "Computador não liga",
        "prioridade": "Alta"
    }

    resposta = client.put(
        f"/chamados/{chamado_id}",
        json=dados_atualizados
    )

    assert resposta.status_code == 200
    assert resposta.json()["chamado"]["problema"] == "Computador não liga"
    assert resposta.json()["chamado"]["prioridade"] == "Alta"

def test_atualizar_chamado_inexistente():
    dados_atualizados = {
        "solicitante": "Carlos",
        "problema": "Impressora não funciona",
        "prioridade": "Alta"
    }

    resposta = client.put(
        "/chamados/999",
        json=dados_atualizados
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Chamado não encontrado"

def test_excluir_chamado():
    novo_chamado = {
        "solicitante": "Ana",
        "problema": "Teclado não funciona",
        "prioridade": "Baixa"
    }

    cadastro = client.post("/chamados", json=novo_chamado)

    assert cadastro.status_code == 200

    chamado_id = cadastro.json()["chamado"]["id"]

    resposta = client.delete(f"/chamados/{chamado_id}")

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Chamado excluído com sucesso"

    consulta = client.get(f"/chamados/{chamado_id}")

    assert consulta.status_code == 404

def test_excluir_chamado_inexistente():
    resposta = client.delete("/chamados/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Chamado não encontrado"

def test_ids_nao_repetem_apos_exclusao():
    dados = {
        "solicitante": "Ana",
        "problema": "Sistema lento",
        "prioridade": "Alta"
    }

    primeiro = client.post("/chamados", json=dados)
    segundo = client.post("/chamados", json=dados)

    id_primeiro = primeiro.json()["chamado"]["id"]
    id_segundo = segundo.json()["chamado"]["id"]

    client.delete(f"/chamados/{id_primeiro}")

    terceiro = client.post("/chamados", json=dados)
    id_terceiro = terceiro.json()["chamado"]["id"]

    assert id_terceiro != id_segundo