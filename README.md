# API de Balanceamento de Times

Este projeto é uma API em FastAPI para gerenciar jogadores, partidas, confirmações e balancear times de forma equilibrada.

## Visão geral

- Autenticação JWT para usuários.
- CRUD de jogadores e partidas.
- Confirmação de jogadores em partidas com posição e time.
- Balanceamento automático de 12 jogadores em dois times, com retorno da posição de cada jogador.
- SQLite como banco de dados local.

## Estrutura do projeto

- `app/`: código principal da aplicação.
  - `config/`: configuração de banco, segurança e settings.
  - `models/`: modelos SQLAlchemy para tabelas do banco.
  - `schemas/`: schemas Pydantic para request/response.
  - `routes/`: rotas FastAPI para autenticação, jogadores, partidas e balanceamento.
  - `balanceador/`: lógica de balanceamento usando Gurobi.
- `tests/`: testes automatizados.
- `clear_database.py`: utilitário para limpar o banco local e resetar IDs.
- `requirements.txt`: dependências Python necessárias.

## Como rodar

1. Criar e ativar um ambiente virtual Python.
2. Instalar dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Executar a API:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Acessar a documentação automática em:
   ```
   http://127.0.0.1:8000/docs
   ```

## Observações

- O arquivo `database.db` é o banco local SQLite. Ele está no `.gitignore` e não deve ser enviado ao repositório, pois contém dados de execução local.
- Se quiser começar do zero, rode:
  ```bash
  python clear_database.py
  ```

## Próximo passo para publicar no GitHub

- Se quiser que eu conecte ao GitHub, precisamos criar o repositório remoto e adicionar o remote `origin`.
- Use um token do GitHub ou a GitHub CLI para criar o repositório e fazer push.
