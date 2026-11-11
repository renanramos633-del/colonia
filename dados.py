# Dados de exemplo da colônia. Energia em kWh e vento em m/s.
# Cada execução representa um período de uma hora.

def carregar_dados():
    return {
        'nome': 'Aurora',
        'clima': {'vento': 8},
        'sistemas': {
            'energetico': {
                'solar': {'energia': 20},
                'eolico': {
                    'vento_historico': [8, 10, 12],
                    'energia_historica': [20, 25, 30]
                },
                'bateria': {'reserva': 40, 'capacidade': 100}
            },
            'consumidores': {'suporte_vida': 30, 'pesquisa': 25, 'lazer': 15}
        }
    }
