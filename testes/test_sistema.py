import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dados import carregar_cenario
from main import executar
from previsao import ajustar_reta, prever_energia
from decisoes import decidir, analisar_energia

class SistemaTest(unittest.TestCase):
    def test_regressao(self):
        a, b = ajustar_reta([8, 10, 12], [20, 25, 30])
        self.assertEqual((a, b), (2.5, 0))
        self.assertEqual(prever_energia(11, a, b), 27.5)

    def test_deficit_e_prioridade(self):
        r = executar(carregar_cenario('deficit'))
        self.assertEqual(r['geracao'], 40)
        self.assertTrue(r['modo_economia'])
        self.assertEqual(r['consumos_apos_decisao'], {'suporte_vida': 30, 'pesquisa': 0, 'lazer': 0})
        self.assertEqual(r['depois']['reserva_final'], 50)

    def test_excedente_limitado(self):
        r = analisar_energia(80, 30, 90, 100)
        self.assertEqual(r['armazenada'], 10)
        self.assertEqual(r['excedente_nao_armazenado'], 40)

    def test_emergencia(self):
        r = decidir(0, {'suporte_vida': 30, 'pesquisa': 25, 'lazer': 15}, 10, 100)
        self.assertEqual(r['depois']['deficit_nao_atendido'], 20)
        self.assertTrue(any('EMERGÊNCIA' in m for m in r['mensagens']))

    def test_limites(self):
        r = decidir(70, {'suporte_vida': 30, 'pesquisa': 25, 'lazer': 15}, 50, 100)
        self.assertFalse(r['modo_economia'])
        self.assertEqual(r['depois']['saldo'], 0)

    def test_invalidos(self):
        for x, y in [([8, 8], [20, 30]), ([8], [20, 30])]:
            with self.assertRaises(ValueError): ajustar_reta(x, y)
        with self.assertRaises(ValueError): analisar_energia(10, 20, 110, 100)
        with self.assertRaises(ValueError): prever_energia(-1, 2.5, 0)

if __name__ == '__main__':
    unittest.main()
