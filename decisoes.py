"""Regras e balanço energético de um intervalo de uma hora."""
from math import isfinite

LIMITE_RESERVA = 50
CONSUMO_ALTO = 60

def analisar_energia(geracao, consumo, reserva, capacidade):
    valores = [geracao, consumo, reserva, capacidade]
    if not all(isfinite(v) and v >= 0 for v in valores) or reserva > capacidade:
        raise ValueError('Energias inválidas ou reserva acima da capacidade.')
    saldo = geracao - consumo
    armazenada = min(max(saldo, 0), capacidade - reserva)
    retirada = min(max(-saldo, 0), reserva)
    return {'saldo': saldo, 'armazenada': armazenada, 'retirada': retirada,
            'reserva_final': reserva + armazenada - retirada,
            'deficit_nao_atendido': max(0, -saldo - retirada),
            'excedente_nao_armazenado': max(0, saldo - armazenada)}

def decidir(geracao, consumidores, reserva, capacidade):
    """Prioriza suporte à vida; corta lazer e depois pesquisa quando necessário."""
    if set(consumidores) != {'suporte_vida', 'pesquisa', 'lazer'}:
        raise ValueError('Informe suporte_vida, pesquisa e lazer.')
    if not all(isfinite(v) and v >= 0 for v in consumidores.values()):
        raise ValueError('Consumos devem ser finitos e não negativos.')
    consumo = sum(consumidores.values())
    antes = analisar_energia(geracao, consumo, reserva, capacidade)
    mensagens = []
    economia = reserva < LIMITE_RESERVA and consumo > CONSUMO_ALTO
    if reserva < LIMITE_RESERVA:
        mensagens.append('ALERTA: reduzir consumo; reserva abaixo de 50 kWh.')
    if economia:
        mensagens.append('AÇÃO: ativar modo economia.')
    if consumo > geracao:
        mensagens.append('ALERTA: consumo maior que geração.')
    elif geracao > consumo:
        mensagens.append('SUGESTÃO: armazenar energia excedente.')
    else:
        mensagens.append('ESTADO: geração e consumo em equilíbrio.')
    ativos = dict(consumidores)
    desligados = []
    for nome in ['lazer', 'pesquisa']:
        if economia or sum(ativos.values()) > geracao + reserva:
            ativos[nome] = 0
            desligados.append(nome)
    if desligados:
        mensagens.append('AÇÃO: desligar ' + ', '.join(desligados) + '; manter suporte à vida ligado.')
    depois = analisar_energia(geracao, sum(ativos.values()), reserva, capacidade)
    if depois['deficit_nao_atendido'] > 0:
        mensagens.append('EMERGÊNCIA: energia insuficiente para suporte à vida; solicitar fonte auxiliar.')
    if depois['excedente_nao_armazenado'] > 0:
        mensagens.append('ALERTA: bateria cheia; limitar geração ou realocar excedente.')
    return {'mensagens': mensagens, 'modo_economia': economia, 'consumo_original': consumo,
            'consumos_apos_decisao': ativos, 'antes': antes, 'depois': depois}
