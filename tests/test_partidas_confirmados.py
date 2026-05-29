import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import Base
from app.models.jogador_time_model import JogadorTime
from app.models.jogadores_model import Jogador
from app.models.partidas_model import Partida
from app.models.usuario_model import Usuario
from app.routes import partidas_routes


class TestListarConfirmadosPartida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        cls.Session = sessionmaker(bind=cls.test_engine)
        Base.metadata.create_all(bind=cls.test_engine)

    def setUp(self):
        Base.metadata.drop_all(bind=self.test_engine)
        Base.metadata.create_all(bind=self.test_engine)
        self.session = self.Session()

        usuario = Usuario(nome="Teste", email="teste@teste.com", senha="hash")
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)

        jogador = Jogador(
            nome="Jogador 1",
            habilidade_ataque=8,
            habilidade_defesa=7,
            habilidade_meio=6,
        )
        self.session.add(jogador)
        self.session.commit()
        self.session.refresh(jogador)

        partida = Partida(
            tipo_partida="Futebol",
            data_hora="2026-05-26T18:00:00",
            local="Quadra Central",
            criado_por=usuario.id,
            status="Aberta",
        )
        self.session.add(partida)
        self.session.commit()
        self.session.refresh(partida)

        confirmacao = JogadorTime(
            partida_id=partida.id,
            jogador_id=jogador.id,
            time=1,
            posicao_selecionada="Atacante",
        )
        self.session.add(confirmacao)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_listar_confirmados_partida_retorna_detalhes_completos(self):
        data = partidas_routes.listar_confirmados_partida(partida_id=1, email="teste@teste.com", db=self.session)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0].confirmacao_id, 1)
        self.assertEqual(data[0].partida_id, 1)
        self.assertEqual(data[0].jogador_id, 1)
        self.assertEqual(data[0].time, 1)
        self.assertEqual(data[0].posicao_selecionada, "Atacante")
        self.assertEqual(data[0].nome, "Jogador 1")
        self.assertEqual(data[0].habilidade_ataque, 8)
        self.assertEqual(data[0].habilidade_defesa, 7)
        self.assertEqual(data[0].habilidade_meio, 6)


if __name__ == "__main__":
    unittest.main()
