from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator


class Chamado(BaseModel):
    solicitante: str = Field(min_length=1, strict=True)
    problema: str = Field(min_length=1, strict=True)
    prioridade: str = Field(min_length=1, strict=True)

    @field_validator("solicitante", "problema", "prioridade")
    @classmethod
    def nao_permitir_espacos(cls, valor: str):
        if not valor.strip():
            raise ValueError("O campo não pode estar vazio")
        return valor

    @field_validator("prioridade")
    @classmethod
    def validar_prioridade(cls, valor: str):
        prioridades_validas = ["Alta", "Media", "Baixa"]

        if valor not in prioridades_validas:
            raise ValueError("Prioridade inválida")

        return valor


router = APIRouter()
chamados_db = []


@router.get("/chamados")
def listar_chamados():
    return {"chamados": chamados_db}
@router.get("/chamados/{chamado_id}")
def consultar_chamado(chamado_id: int):
    for chamado in chamados_db:
        if chamado["id"] == chamado_id:
            return chamado

    raise HTTPException(
        status_code=404,
        detail="Chamado não encontrado"
    )


@router.post("/chamados")
def criar_chamado(chamado: Chamado):
    novo_id = max(
        (item["id"] for item in chamados_db),
        default=0
    ) + 1

    novo_chamado = {
        "id": novo_id,
        **chamado.model_dump()
    }

    chamados_db.append(novo_chamado)

    return {
        "mensagem": "Chamado criado com sucesso",
        "chamado": novo_chamado
    }
@router.put("/chamados/{chamado_id}")
def atualizar_chamado(chamado_id: int, dados: Chamado):
    for chamado in chamados_db:
        if chamado["id"] == chamado_id:
            chamado.update(dados.model_dump())

            return {
                "mensagem": "Chamado atualizado com sucesso",
                "chamado": chamado
            }

    raise HTTPException(
        status_code=404,
        detail="Chamado não encontrado"
    )

@router.delete("/chamados/{chamado_id}")
def excluir_chamado(chamado_id: int):
    for chamado in chamados_db:
        if chamado["id"] == chamado_id:
            chamados_db.remove(chamado)

            return {
                "mensagem": "Chamado excluído com sucesso"
            }

    raise HTTPException(
        status_code=404,
        detail="Chamado não encontrado"
    )