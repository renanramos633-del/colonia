# Compara geração e consumo antes de aplicar as decisões.
def analisar_energia(geracao, consumo):
    if consumo > geracao:
        return 'ALERTA: consumo maior que geração.'
    elif geracao > consumo:
        return 'SUGESTÃO: armazenar energia excedente.'
    else:
        return 'ESTADO: geração e consumo em equilíbrio.'


# O suporte à vida tem prioridade sobre pesquisa e lazer.
def tomar_decisoes(geracao, consumidores, reserva):
    consumo = sum(consumidores.values())
    mensagens = []
    consumos_ajustados = consumidores.copy()

    if reserva < 50:
        mensagens.append('ALERTA: reduzir consumo; reserva abaixo de 50 kWh.')

    if reserva < 50 and consumo > 60:
        mensagens.append('AÇÃO: ativar modo economia.')
        consumos_ajustados['lazer'] = 0
        consumos_ajustados['pesquisa'] = 0
        mensagens.append('AÇÃO: desligar lazer e pesquisa.')

    # Se ainda faltar energia, desligar os sistemas não essenciais.
    for sistema in ['lazer', 'pesquisa']:
        if sum(consumos_ajustados.values()) > geracao + reserva:
            if consumos_ajustados[sistema] > 0:
                consumos_ajustados[sistema] = 0
                mensagens.append('AÇÃO: desligar ' + sistema + '.')

    mensagens.append('PRIORIDADE: manter suporte à vida ligado.')
    if sum(consumos_ajustados.values()) > geracao + reserva:
        mensagens.append('EMERGÊNCIA: energia insuficiente; solicitar fonte auxiliar.')

    return consumos_ajustados, mensagens


# Atualiza a reserva respeitando a capacidade da bateria.
def atualizar_reserva(geracao, consumo, reserva, capacidade):
    saldo = geracao - consumo
    nova_reserva = reserva + saldo
    mensagem = ''

    if nova_reserva > capacidade:
        excedente = nova_reserva - capacidade
        nova_reserva = capacidade
        mensagem = 'ALERTA: excedente de ' + str(excedente) + ' kWh sem armazenamento.'
    elif nova_reserva < 0:
        falta = -nova_reserva
        nova_reserva = 0
        mensagem = 'ALERTA: faltam ' + str(falta) + ' kWh para atender o consumo.'

    return nova_reserva, mensagem
