import pytest

import repositorio
from app import criar_app
from repositorio import RepositorioMemoria


@pytest.fixture
def cliente():
    return criar_app(RepositorioMemoria()).test_client()


def test_saude(cliente):
    assert cliente.get("/saude").get_json() == {"status": "ok"}


def test_lista_comeca_vazia(cliente):
    assert cliente.get("/tarefas").get_json() == []


def test_cria_tarefa(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "Revisar Docker"})
    assert resposta.status_code == 201
    assert resposta.get_json()["titulo"] == "Revisar Docker"
    assert len(cliente.get("/tarefas").get_json()) == 1


def test_rejeita_titulo_vazio(cliente):
    resposta = cliente.post("/tarefas", json={"titulo": "   "})
    assert resposta.status_code == 400


def test_database_url_seleciona_repositorio_postgres(monkeypatch):
    class RepositorioPostgresFalso:
        def __init__(self, dsn):
            self.dsn = dsn

    monkeypatch.setenv("DATABASE_URL", "postgresql://teste")
    monkeypatch.setattr(repositorio, "RepositorioPostgres", RepositorioPostgresFalso)

    repo = repositorio.criar_repositorio()

    assert isinstance(repo, RepositorioPostgresFalso)
    assert repo.dsn == "postgresql://teste"
