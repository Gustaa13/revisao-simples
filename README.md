# Revisão: GitHub Actions + Docker

API de tarefas em Flask. Sem a variável `DATABASE_URL`, guarda as tarefas em
memória; com ela, usa um PostgreSQL.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/saude` | `{"status": "ok"}` |
| GET | `/tarefas` | lista as tarefas |
| POST | `/tarefas` | cria uma tarefa — corpo JSON `{"titulo": "..."}` |

## Executar com PostgreSQL

O Compose inicia a API e o PostgreSQL. As tarefas ficam no volume Docker `postgres_data` e continuam disponíveis depois que os containers forem recriados.

1. Copie `.env.example` para `.env` e ajuste `POSTGRES_PASSWORD` e a senha correspondente em `DATABASE_URL`.
2. Inicie os serviços:

   ```bash
   docker compose up --build -d
   ```

3. Confira a API em `http://localhost:5000/saude`.
4. Para parar sem apagar as tarefas, rode `docker compose down`. Para apagar também o banco, rode `docker compose down -v`.

No PowerShell, a cópia pode ser feita com `Copy-Item .env.example .env`.

O serviço da API recebe `DATABASE_URL` apontando para o hostname `db` da rede Compose. Sem essa variável, `criar_repositorio()` ainda usa memória, por exemplo nos testes unitários.

Testes: `pip install -r requirements-dev.txt && pytest -v`

Exemplos com curl:

```bash
curl http://localhost:5000/saude
curl -X POST -H "Content-Type: application/json" \
  -d '{"titulo": "Revisar Docker"}' http://localhost:5000/tarefas
curl http://localhost:5000/tarefas
```

PowerShell:

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:5000/tarefas `
  -ContentType "application/json" -Body '{"titulo": "Revisar Docker"}'
```
