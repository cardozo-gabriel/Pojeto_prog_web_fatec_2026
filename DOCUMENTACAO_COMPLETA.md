# DOCUMENTAÇÃO COMPLETA DO PROJETO

## 1. Visão geral

Este projeto é uma API FastAPI para:

- cadastro e autenticação de usuários
- cadastro e listagem de jogadores
- criação e consulta de partidas
- confirmação de jogadores em partidas
- balanceamento automático de times com otimização matemática usando `gurobipy`

A API roda em modo local com SQLite, usa autenticação JWT e expõe documentação interativa via Swagger/OpenAPI.

> O projeto atual ainda não possui uma camada separada de `services`. A lógica fica concentrada em `routes`, `models`, `schemas`, `config` e `balanceador`.

---

## 2. Estrutura atual do projeto

### Arquivo raiz

- [balanceador.py](balanceador.py)
- [requirements.txt](requirements.txt)
- [database.db](database.db)
- [DOCUMENTACAO_TECNICA.md](DOCUMENTACAO_TECNICA.md)

### Pacote `app`

- [app/main.py](app/main.py)

#### Config

- [app/config/database.py](app/config/database.py)
- [app/config/security.py](app/config/security.py)
- [app/config/settings.py](app/config/settings.py)

#### Models

- [app/models/usuario_model.py](app/models/usuario_model.py)
- [app/models/jogadores_model.py](app/models/jogadores_model.py)
- [app/models/partidas_model.py](app/models/partidas_model.py)
- [app/models/jogador_time_model.py](app/models/jogador_time_model.py)

#### Schemas

- [app/schemas/auth_schema.py](app/schemas/auth_schema.py)
- [app/schemas/usuario_schema.py](app/schemas/usuario_schema.py)
- [app/schemas/jogadores_schema.py](app/schemas/jogadores_schema.py)
- [app/schemas/partidas_schema.py](app/schemas/partidas_schema.py)
- [app/schemas/jogador_time_schema.py](app/schemas/jogador_time_schema.py)
- [app/schemas/balanceamento_schema.py](app/schemas/balanceamento_schema.py)

#### Rotas

- [app/routes/auth_routes.py](app/routes/auth_routes.py)
- [app/routes/jogadores_routes.py](app/routes/jogadores_routes.py)
- [app/routes/partidas_routes.py](app/routes/partidas_routes.py)
- [app/routes/balanceamento_routes.py](app/routes/balanceamento_routes.py)

#### Balanceador

- [app/balanceador/balanceador.py](app/balanceador/balanceador.py)

---

## 3. Tecnologias usadas

- Python 3.13
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- python-jose
- passlib + bcrypt
- gurobipy
- python-dotenv

---

## 4. Como o projeto funciona

### 4.1 Inicialização da aplicação

O ponto de entrada é [app/main.py](app/main.py).

Quando o app inicia:

1. o `FastAPI` é criado
2. o banco SQLite é conectado
3. as tabelas são criadas automaticamente com `Base.metadata.create_all(bind=engine)`
4. os routers são registrados

#### Routers registrados

- `/auth`
- `/jogadores`
- `/partidas`
- `/balanceamento`

### 4.2 Banco de dados

O banco usado é SQLite e o arquivo é `database.db`.

A conexão fica em [app/config/database.py](app/config/database.py):

- `engine` cria a conexão com `settings.DATABASE_URL`
- `SessionLocal` cria a sessão SQLAlchemy
- `get_db()` fornece a sessão para cada request

### 4.3 Configurações de ambiente

As configurações ficam em [app/config/settings.py](app/config/settings.py).

Valores atuais:

- `DATABASE_URL = sqlite:///./database.db`
- `SECRET_KEY = super-secret-key-change-me`
- `ALGORITHM = HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES = 60`

### 4.4 Autenticação

A autenticação é feita com JWT Bearer Token.

A lógica de segurança fica em [app/config/security.py](app/config/security.py):

- `get_password_hash()` gera hash da senha com `passlib` + `bcrypt`
- `verify_password()` valida a senha
- `create_access_token()` cria o JWT
- `get_current_user()` valida o token vindo do header `Authorization`

### 4.5 Modelos do banco

#### Usuario

Arquivo: [app/models/usuario_model.py](app/models/usuario_model.py)

Campos:

- `id`
- `nome`
- `email`
- `senha`

#### Jogador

Arquivo: [app/models/jogadores_model.py](app/models/jogadores_model.py)

Campos:

- `id`
- `nome`
- `habilidade_ataque`
- `habilidade_defesa`
- `habilidade_meio`

#### Partida

Arquivo: [app/models/partidas_model.py](app/models/partidas_model.py)

Campos:

- `id`
- `tipo_partida`
- `data_hora`
- `local`
- `criado_por`
- `status`

#### JogadorTime

Arquivo: [app/models/jogador_time_model.py](app/models/jogador_time_model.py)

Campos:

- `id`
- `partida_id`
- `jogador_id`
- `time`
- `posicao_selecionada`

### 4.6 Schemas

Os schemas definem o formato dos dados de entrada e saída.

#### auth_schema

Arquivo: [app/schemas/auth_schema.py](app/schemas/auth_schema.py)

- `LoginRequest`
- `TokenResponse`

#### usuario_schema

Arquivo: [app/schemas/usuario_schema.py](app/schemas/usuario_schema.py)

- `UsuarioCreate`
- `UsuarioOut`

#### jogadores_schema

Arquivo: [app/schemas/jogadores_schema.py](app/schemas/jogadores_schema.py)

- `JogadorCreate`
- `JogadorOut`

#### partidas_schema

Arquivo: [app/schemas/partidas_schema.py](app/schemas/partidas_schema.py)

- `PartidaCreate`
- `PartidaOut`

#### jogador_time_schema

Arquivo: [app/schemas/jogador_time_schema.py](app/schemas/jogador_time_schema.py)

- `JogadorTimeCreate`
- `JogadorTimeOut`

#### balanceamento_schema

Arquivo: [app/schemas/balanceamento_schema.py](app/schemas/balanceamento_schema.py)

- `BalanceamentoResponse`

---

## 5. Endpoints da API

## 5.1 Saúde da API

### GET /health

Retorna:

```json
{
  "status": "ok"
}
```

### 5.2 Autenticação

#### POST /auth/register

Cadastro de usuário.

Body:

```json
{
  "nome": "Matheus",
  "email": "matheus@teste.com",
  "senha": "123456"
}
```

Resposta:

```json
{
  "message": "Usuário cadastrado com sucesso"
}
```

#### POST /auth/login

Login do usuário.

Body:

```json
{
  "email": "matheus@teste.com",
  "senha": "123456"
}
```

Resposta:

```json
{
  "access_token": "TOKEN_JWT",
  "token_type": "bearer"
}
```

#### GET /auth/me

Retorna o usuário autenticado.

Headers:

```http
Authorization: Bearer TOKEN_JWT
```

### 5.3 Jogadores

#### POST /jogadores

Cadastro de jogador.

Headers:

```http
Authorization: Bearer TOKEN_JWT
```

Body:

```json
{
  "nome": "Gabriel",
  "habilidade_ataque": 8,
  "habilidade_defesa": 6,
  "habilidade_meio": 7
}
```

Resposta:

```json
{
  "message": "Jogador cadastrado com sucesso"
}
```

#### GET /jogadores

Lista todos os jogadores cadastrados.

Headers:

```http
Authorization: Bearer TOKEN_JWT
```

### 5.4 Partidas

#### POST /partidas

Cria uma partida.

Headers:

```http
Authorization: Bearer TOKEN_JWT
```

Body:

```json
{
  "tipo_partida": "Fut7",
  "data_hora": "2026-06-10 20:00",
  "local": "Arena Society",
  "status": "Aberta"
}
```

Resposta:

```json
{
  "message": "Partida criada com sucesso"
}
```

#### GET /partidas

Lista todas as partidas.

Headers:

```http
Authorization: Bearer TOKEN_JWT
```

#### POST /partidas/confirmar-jogador

Confirma um jogador em uma partida.

Headers:

```http
Authorization: Bearer TOKEN_JWT
```

Body:

```json
{
  "partida_id": 1,
  "jogador_id": 2,
  "time": 1,
  "posicao_selecionada": "ataque"
}
```

Resposta:

```json
{
  "message": "Jogador confirmado na partida"
}
```

### 5.5 Balanceamento

#### GET /balanceamento

Balanceia os jogadores confirmados em uma partida.

Headers:

```http
Authorization: Bearer TOKEN_JWT
```

Query param:

```text
partida_id=1
```

Resposta:

```json
{
  "time_1": ["Gabriel", "Matheus", "João", "Carlos", "Rafael", "Igor"],
  "time_2": ["Lucas", "Pedro", "André", "Bruno", "Diego", "Thiago"],
  "diferenca": 0
}
```

> O endpoint exige exatamente 12 confirmações. Se a partida tiver menos ou mais de 12 jogadores confirmados, ele retorna erro 400.

---

## 6. Como o balanceador funciona

O balanceador real está em [app/balanceador/balanceador.py](app/balanceador/balanceador.py).

### Regras atuais

- recebe uma lista com **12 jogadores**
- cada jogador precisa ter:
  - `nome`
  - `habilidade_ataque`
  - `habilidade_meio`
  - `habilidade_defesa`
- cria uma matriz de habilidades
- monta um modelo inteiro com `gurobipy`
- resolve o problema com as seguintes restrições:
  - cada jogador vai para exatamente um time
  - cada time recebe 6 jogadores
  - cada time recebe 2 jogadores em cada posição
  - a diferença entre os times é minimizada

### Saída

O retorno é um JSON com:

- `time_1`
- `time_2`
- `diferenca`

### Arquivo legado

O arquivo [balanceador.py](balanceador.py) no root é um arquivo de exemplo/legado que ainda não foi integrado como serviço principal da API.

A API atual usa o balanceador em [app/balanceador/balanceador.py](app/balanceador/balanceador.py).

---

## 7. Fluxo completo de uso da API

### 7.1 Fluxo básico

1. cadastrar usuário
2. fazer login
3. cadastrar jogadores
4. criar partida
5. confirmar jogadores na partida
6. chamar `/balanceamento`

### 7.2 Exemplo de fluxo lógico

- `POST /auth/register`
- `POST /auth/login`
- `POST /jogadores`
- `POST /partidas`
- `POST /partidas/confirmar-jogador`
- `GET /balanceamento`

---

## 8. Como testar no Insomnia

### 8.1 Pré-requisitos

- servidor rodando localmente
- Insomnia instalado
- base URL definida como `http://127.0.0.1:8000`

### 8.2 Configuração do ambiente no Insomnia

Crie um ambiente com:

```json
{
  "base_url": "http://127.0.0.1:8000",
  "token": ""
}
```

### 8.3 Como criar uma requisição

1. abra o Insomnia
2. clique em `Create` -> `Request`
3. escolha o método HTTP
4. coloque a URL usando a variável `{{ base_url }}`
5. envie o JSON no body
6. se a rota for protegida, adicione o header:

```http
Authorization: Bearer {{ token }}
```

### 8.4 Passo a passo completo

#### 1. Cadastrar usuário

Request:

- Método: `POST`
- URL: `{{ base_url }}/auth/register`

Body JSON:

```json
{
  "nome": "Matheus",
  "email": "matheus@teste.com",
  "senha": "123456"
}
```

#### 2. Fazer login

Request:

- Método: `POST`
- URL: `{{ base_url }}/auth/login`

Body JSON:

```json
{
  "email": "matheus@teste.com",
  "senha": "123456"
}
```

Após a resposta, copie o `access_token` e salve no ambiente `token`.

#### 3. Cadastrar jogadores

Repita esta requisição 12 vezes com jogadores diferentes.

Request:

- Método: `POST`
- URL: `{{ base_url }}/jogadores`

Header:

```http
Authorization: Bearer {{ token }}
```

Body exemplo:

```json
{
  "nome": "Gabriel",
  "habilidade_ataque": 8,
  "habilidade_defesa": 6,
  "habilidade_meio": 7
}
```

#### 4. Criar partida

Request:

- Método: `POST`
- URL: `{{ base_url }}/partidas`

Header:

```http
Authorization: Bearer {{ token }}
```

Body:

```json
{
  "tipo_partida": "Fut7",
  "data_hora": "2026-06-10 20:00",
  "local": "Arena Society",
  "status": "Aberta"
}
```

#### 5. Confirmar jogadores na partida

Para cada jogador cadastrado, confirme a presença.

Request:

- Método: `POST`
- URL: `{{ base_url }}/partidas/confirmar-jogador`

Header:

```http
Authorization: Bearer {{ token }}
```

Body:

```json
{
  "partida_id": 1,
  "jogador_id": 1,
  "time": 1,
  "posicao_selecionada": "ataque"
}
```

> O `jogador_id` deve ser o id do jogador cadastrado. O `partida_id` deve ser o id da partida criada. O `time` pode ser `1` ou `2`. `posicao_selecionada` pode ser `ataque`, `meio` ou `defesa`.

#### 6. Chamar o balanceamento

Request:

- Método: `GET`
- URL: `{{ base_url }}/balanceamento?partida_id=1`

Header:

```http
Authorization: Bearer {{ token }}
```

Resposta esperada:

```json
{
  "time_1": ["..."],
  "time_2": ["..."],
  "diferenca": 0
}
```

#### 7. Testar /health

Request:

- Método: `GET`
- URL: `{{ base_url }}/health`

Resposta:

```json
{
  "status": "ok"
}
```

#### 8. Testar /auth/me

Request:

- Método: `GET`
- URL: `{{ base_url }}/auth/me`

Header:

```http
Authorization: Bearer {{ token }}
```

### 8.5 Como validar se o fluxo funcionou

O fluxo está correto quando:

1. `/auth/register` retorna sucesso
2. `/auth/login` retorna token
3. `/jogadores` cadastra jogadores sem erro
4. `/partidas` cria partida sem erro
5. `/partidas/confirmar-jogador` aceita 12 confirmações
6. `/balanceamento` retorna dois times e `diferenca`

---

## 9. Regras importantes do projeto

- `POST /jogadores` e `POST /partidas` exigem token JWT
- `GET /balanceamento` exige token JWT
- o balanceamento só funciona com exatamente 12 confirmações
- os IDs usados nas confirmações devem existir no banco
- `status` da partida pode ser `Aberta` ou `Encerrada`
- o banco é SQLite e o arquivo local é `database.db`

---

## 10. O que cada arquivo faz, de forma resumida

### [app/main.py](app/main.py)

- cria a aplicação FastAPI
- cria as tabelas no banco
- registra os routers

### [app/config/database.py](app/config/database.py)

- conecta ao SQLite
- cria o `engine`
- fornece a sessão SQLAlchemy

### [app/config/settings.py](app/config/settings.py)

- guarda as configurações do projeto

### [app/config/security.py](app/config/security.py)

- autenticação com JWT
- hash de senha
- verificação de senha
- leitura do token do header

### [app/models/usuario_model.py](app/models/usuario_model.py)

- representa o usuário na tabela `usuarios`

### [app/models/jogadores_model.py](app/models/jogadores_model.py)

- representa o jogador na tabela `jogadores`

### [app/models/partidas_model.py](app/models/partidas_model.py)

- representa a partida na tabela `partidas`

### [app/models/jogador_time_model.py](app/models/jogador_time_model.py)

- representa a confirmação do jogador em uma partida

### [app/schemas/auth_schema.py](app/schemas/auth_schema.py)

- define login e token

### [app/schemas/usuario_schema.py](app/schemas/usuario_schema.py)

- define cadastro e retorno de usuário

### [app/schemas/jogadores_schema.py](app/schemas/jogadores_schema.py)

- define cadastro e resposta de jogador

### [app/schemas/partidas_schema.py](app/schemas/partidas_schema.py)

- define criação e retorno de partida

### [app/schemas/jogador_time_schema.py](app/schemas/jogador_time_schema.py)

- define confirmação de jogador

### [app/schemas/balanceamento_schema.py](app/schemas/balanceamento_schema.py)

- define resposta do balanceamento

### [app/routes/auth_routes.py](app/routes/auth_routes.py)

- registra usuário
- faz login
- retorna usuário autenticado

### [app/routes/jogadores_routes.py](app/routes/jogadores_routes.py)

- cadastra jogador
- lista jogadores

### [app/routes/partidas_routes.py](app/routes/partidas_routes.py)

- cria partida
- lista partidas
- confirma jogador na partida

### [app/routes/balanceamento_routes.py](app/routes/balanceamento_routes.py)

- valida a partida
- busca as confirmações
- chama o balanceador
- retorna os times

### [app/balanceador/balanceador.py](app/balanceador/balanceador.py)

- resolve o problema de balanceamento com `gurobipy`

### [balanceador.py](balanceador.py)

- arquivo de exemplo/legado
- não é usado pela API atual

### [requirements.txt](requirements.txt)

- lista todas as dependências necessárias

### [database.db](database.db)

- banco SQLite local gerado pela aplicação

### [DOCUMENTACAO_TECNICA.md](DOCUMENTACAO_TECNICA.md)

- documentação antiga do projeto
- pode ser desatualizada em relação ao estado real

---

## 11. Como rodar o projeto

### 11.1 Instalar dependências

```powershell
pip install -r requirements.txt
```

### 11.2 Rodar o servidor

```powershell
cd C:\Users\Usuario\Desktop\api_trabalho
uvicorn app.main:app --reload --host 127.0.0.1
```

### 11.3 Acessar documentação

```text
http://127.0.0.1:8000/docs
```

---

## 12. Possíveis problemas e como resolver

### 12.1 Erro de bcrypt / passlib

Se aparecer erro relacionado a `bcrypt`, o problema costuma ser incompatibilidade entre a versão de `passlib` e a versão de `bcrypt` instalada.

A solução mais segura é alinhar as versões em [requirements.txt](requirements.txt).

### 12.2 Porta em uso

Se a porta 8000 já estiver ocupada, pare o processo em execução e suba o servidor novamente.

### 12.3 Balanceamento sem 12 jogadores

Se `/balanceamento` retornar erro 400, verifique se existem exatamente 12 confirmações.

### 12.4 Token expirado

O token expira após 60 minutos, conforme [app/config/settings.py](app/config/settings.py).

---

## 13. Conclusão

Este projeto funciona como uma API completa de cadastro, autenticação, partidas e balanceamento.

A parte mais importante para entender é:

1. o app inicializa no [app/main.py](app/main.py)
2. o banco é criado automaticamente
3. o usuário autentica e recebe JWT
4. os jogadores são cadastrados
5. a partida é criada
6. os jogadores são confirmados
7. o balanceamento usa o solver `gurobipy`

Se você quiser, no próximo passo eu posso também transformar esta documentação em um `README.md` pronto para apresentação em aula.

---

## 14. Agradecimento

Obrigado pela sua atenção e pela sua curiosidade em entender esse projeto.

Você chegou aqui com consistência, e isso faz toda a diferença para aprender e ensinar.

---
