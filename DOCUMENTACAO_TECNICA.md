# Documentação Técnica — Balanceador de Partidas

## Visão Geral

O projeto atual contém apenas um módulo de balanceamento de times para partidas de futebol, implementado em [balanceador.py](balanceador.py).

Este módulo utiliza o solver `gurobipy` para montar dois times equilibrados a partir de um conjunto de jogadores previamente definido e um modelo matemático de otimização inteira.

> **Observação:** a API completa descrita no enunciado não está presente no workspace atual. O que existe hoje é o núcleo de balanceamento.

---

## Escopo Atual

### O que está implementado

- Modelo de otimização com `gurobipy`
- Criação de variáveis binárias para alocação de jogadores
- Cálculo da habilidade total por time
- Minimização da diferença entre os times
- Impressão dos times e da diferença final

### O que não está implementado

- API FastAPI
- Rotas HTTP
- Persistência em SQLite
- ORM com SQLAlchemy
- Autenticação JWT
- Schemas Pydantic
- Serviços e camadas de domínio

---

## Arquitetura Atual

### Estrutura observada

- [balanceador.py](balanceador.py)

### Composição do módulo

O arquivo [balanceador.py](balanceador.py) concentra toda a lógica do balanceamento:

1. Definição da matriz de habilidades
2. Criação do modelo do solver
3. Restrições de alocação
4. Função objetivo
5. Execução da otimização
6. Impressão dos resultados

---

## Modelagem Matemática

### Dados de entrada

A matriz `N` representa as habilidades dos jogadores nas posições:

- ataque
- meio
- defesa

Cada coluna corresponde a um jogador e cada linha corresponde a uma posição.

### Variáveis

- `x[i, j, z]`: variável binária que indica se o jogador `j` na posição `i` foi alocado ao time `z`
- `S[z]`: soma total de habilidade do time `z`
- `D`: diferença absoluta entre os pontos dos dois times

### Restrições

1. Cada jogador deve ser alocado a exatamente um time.
2. Cada time deve ter exatamente 6 jogadores.
3. Cada time deve receber exatamente 2 jogadores em cada posição.
4. A diferença entre os times é modelada por `D`.

### Função objetivo

A função objetivo maximiza a soma total de habilidade dos dois times e penaliza a diferença entre eles:

- maior soma de habilidade é preferida
- menor diferença entre os times é priorizada

---

## Fluxo de Execução

1. O script importa `gurobipy`
2. A matriz de habilidades é carregada
3. O modelo é montado
4. O solver é executado
5. Os nomes dos jogadores são associados às posições selecionadas
6. Os times finais são impressos no terminal

---

## Saída Esperada

A execução atual imprime:

- valor objetivo
- composição do time 1
- composição do time 2
- habilidade total de cada time
- diferença entre os times

---

## Dependências

### Obrigatórias

- `gurobipy`

### Observação

A execução atual falhou durante a validação porque `gurobipy` não está instalado no ambiente local.

---

## Como Executar

```bash
python balanceador.py
```

Antes da execução, certifique-se de que `gurobipy` esteja instalado.

---

## Estado Atual do Projeto

### Status

- **Balanceador matemático:** implementado
- **API REST:** não implementada
- **Banco de dados:** não implementado
- **Autenticação:** não implementada
- **Swagger/OpenAPI:** não implementado

### Conclusão

O workspace atual contém apenas o núcleo do balanceamento. Se quiser, posso seguir em um dos caminhos abaixo:

1. transformar esta documentação em um `README.md` completo
2. esboçar a API FastAPI completa com as rotas descritas
3. implementar o balanceador como serviço reutilizável dentro de uma API
4. montar a estrutura de projeto com `FastAPI`, `SQLAlchemy` e `SQLite`
