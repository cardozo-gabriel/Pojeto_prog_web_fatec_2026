from app.balanceador.balanceador import balancear_jogadores


if __name__ == "__main__":
    jogadores = [
        {"nome": "Gabriel", "habilidade_ataque": 8, "habilidade_meio": 7, "habilidade_defesa": 6},
        {"nome": "Matheus", "habilidade_ataque": 5, "habilidade_meio": 6, "habilidade_defesa": 9},
        {"nome": "Lucas", "habilidade_ataque": 7, "habilidade_meio": 5, "habilidade_defesa": 8},
        {"nome": "João", "habilidade_ataque": 6, "habilidade_meio": 8, "habilidade_defesa": 7},
        {"nome": "Pedro", "habilidade_ataque": 9, "habilidade_meio": 4, "habilidade_defesa": 5},
        {"nome": "Carlos", "habilidade_ataque": 7, "habilidade_meio": 6, "habilidade_defesa": 6},
        {"nome": "Rafael", "habilidade_ataque": 4, "habilidade_meio": 7, "habilidade_defesa": 8},
        {"nome": "André", "habilidade_ataque": 6, "habilidade_meio": 5, "habilidade_defesa": 7},
        {"nome": "Bruno", "habilidade_ataque": 8, "habilidade_meio": 8, "habilidade_defesa": 4},
        {"nome": "Diego", "habilidade_ataque": 5, "habilidade_meio": 9, "habilidade_defesa": 5},
        {"nome": "Igor", "habilidade_ataque": 7, "habilidade_meio": 6, "habilidade_defesa": 9},
        {"nome": "Thiago", "habilidade_ataque": 6, "habilidade_meio": 7, "habilidade_defesa": 6},
    ]

    resultado = balancear_jogadores(jogadores)
    print(resultado)
