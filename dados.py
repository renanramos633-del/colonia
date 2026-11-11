"""Dados didáticos: energias em kWh por intervalo de uma hora; vento em m/s."""
from copy import deepcopy

HISTORICO = {'vento': [8, 10, 12], 'energia_eolica': [20, 25, 30]}
CENARIOS = {
    'deficit': {'reserva': 40, 'capacidade': 100, 'solar': 20,
                'vento': 8, 'consumos': {'suporte_vida': 30, 'pesquisa': 25, 'lazer': 15}},
    'excedente': {'reserva': 40, 'capacidade': 100, 'solar': 60,
                  'vento': 8, 'consumos': {'suporte_vida': 20, 'pesquisa': 5, 'lazer': 5}},
    'equilibrio': {'reserva': 60, 'capacidade': 100, 'solar': 40,
                   'vento': 12, 'consumos': {'suporte_vida': 30, 'pesquisa': 25, 'lazer': 15}},
}

def carregar_cenario(nome):
    """Monta hierarquia independente para cada execução."""
    c = deepcopy(CENARIOS[nome])
    return {'nome': 'Aurora', 'clima': {'vento': c['vento']},
            'sistemas': {'energetico': {'solar': {'energia': c['solar']},
                                      'eolico': {'historico': deepcopy(HISTORICO)},
                                      'bateria': {'reserva': c['reserva'], 'capacidade': c['capacidade']}},
                         'consumidores': c['consumos']}}
