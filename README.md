# TechFlow Enterprise

API REST para gerenciamento de chamados de suporte técnico, desenvolvida com Python e FastAPI, utilizando testes automatizados com Pytest.

## Tecnologias utilizadas

- Python 3.14
- FastAPI
- Pytest
- Pytest-Cov
- Git e GitHub

## Funcionalidades

- Cadastro de chamados
- Listagem de chamados
- Consulta por ID
- Atualização de chamados
- Exclusão de chamados
- Validação de campos obrigatórios
- Validação de prioridade
- Tratamento de chamados inexistentes
- Identificadores únicos para chamados
- Endpoint de verificação de funcionamento (health check)

## Testes automatizados

O projeto possui 19 testes automatizados com Pytest, abrangendo operações CRUD, validações e tratamento de erros.

**Resultados da última execução:**

- 19 testes aprovados
- 100% de cobertura de linhas do código da aplicação
- Nenhuma falha ou aviso

## Como executar os testes

```powershell
python -m pip install -r requirements.txt
python -m pytest tests/ -v --cov=app --cov-report=term-missing
```

## Objetivo

Demonstrar conhecimentos práticos em desenvolvimento backend, construção de APIs REST, validação de dados, controle de versão e qualidade de software por meio de testes automatizados.
