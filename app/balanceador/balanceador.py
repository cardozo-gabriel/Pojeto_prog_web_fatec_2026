from __future__ import annotations

import gurobipy as gp


def balancear_jogadores(jogadores: list[dict]) -> dict[str, list[str] | float]:
    if len(jogadores) != 12:
        raise ValueError("O balanceamento exige exatamente 12 jogadores confirmados.")

    matrix = [
        [int(jogador["habilidade_ataque"]) for jogador in jogadores],
        [int(jogador["habilidade_meio"]) for jogador in jogadores],
        [int(jogador["habilidade_defesa"]) for jogador in jogadores],
    ]

    n = len(matrix)
    m = len(jogadores)
    times = 2

    model = gp.Model()
    model.setParam("OutputFlag", 0)

    x = model.addVars(n, m, times, vtype=gp.GRB.BINARY)
    S = model.addVars(times, vtype=gp.GRB.CONTINUOUS, name="S")
    D = model.addVar(vtype=gp.GRB.CONTINUOUS, name="D")

    model.addConstrs(sum(x[i, j, z] for i in range(n) for z in range(times)) == 1 for j in range(m))
    model.addConstrs(sum(x[i, j, z] for i in range(n) for j in range(m)) == 6 for z in range(times))
    model.addConstrs(
        S[z] == sum(x[i, j, z] * matrix[i][j] for i in range(n) for j in range(m))
        for z in range(times)
    )
    model.addConstr(S[0] - S[1] <= D)
    model.addConstr(S[1] - S[0] <= D)
    model.addConstrs(sum(x[i, j, z] for j in range(m)) == 2 for i in range(n) for z in range(times))

    model.setObjective(S[0] + S[1] - 1000 * D, gp.GRB.MAXIMIZE)
    model.optimize()

    if model.status not in (gp.GRB.OPTIMAL, gp.GRB.SUBOPTIMAL):
        raise RuntimeError("Não foi possível encontrar um balanceamento válido.")

    time_1: list[dict[str, str]] = []
    time_2: list[dict[str, str]] = []
    position_by_index = {0: "Ataque", 1: "Meio", 2: "Defesa"}

    for j in range(m):
        assigned_team = None
        assigned_position = None
        for i in range(n):
            if x[i, j, 0].x > 0.5:
                assigned_team = 1
                assigned_position = position_by_index[i]
                break
            if x[i, j, 1].x > 0.5:
                assigned_team = 2
                assigned_position = position_by_index[i]
                break

        if assigned_team is None or assigned_position is None:
            raise RuntimeError("Não foi possível determinar a posição do jogador no balanceamento.")

        player_info = {
            "nome": str(jogadores[j]["nome"]),
            "posicao": assigned_position,
        }

        if assigned_team == 1:
            time_1.append(player_info)
        else:
            time_2.append(player_info)

    return {
        "time_1": time_1,
        "time_2": time_2,
        "diferenca": round(float(D.X), 2),
    }
