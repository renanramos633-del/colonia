from dados import carregar_dados
from previsao import ajustar_reta, prever_energia
from decisoes import analisar_energia, tomar_decisoes, atualizar_reserva


def executar_sistema():
    colonia = carregar_dados()
    energetico = colonia['sistemas']['energetico']
    eolico = energetico['eolico']
    bateria = energetico['bateria']
    consumidores = colonia['sistemas']['consumidores']
    vento = colonia['clima']['vento']

    # Usa os dados históricos para prever a geração eólica.
    a, b = ajustar_reta(eolico['vento_historico'], eolico['energia_historica'])
    energia_eolica = prever_energia(vento, a, b)
    geracao = energetico['solar']['energia'] + energia_eolica
    consumo = sum(consumidores.values())

    print('COLÔNIA ' + colonia['nome'].upper())
    print('Previsão eólica:', energia_eolica, 'kWh')
    print('Geração total:', geracao, 'kWh')
    print('Consumo inicial:', consumo, 'kWh')
    print('Reserva inicial:', bateria['reserva'], 'kWh')
    print(analisar_energia(geracao, consumo))

    # Aplica as regras e apresenta as ações escolhidas.
    ajustados, mensagens = tomar_decisoes(geracao, consumidores, bateria['reserva'])
    for mensagem in mensagens:
        print(mensagem)

    consumo_final = sum(ajustados.values())
    reserva_final, aviso = atualizar_reserva(
        geracao, consumo_final, bateria['reserva'], bateria['capacidade']
    )
    print('Consumo após decisões:', consumo_final, 'kWh')
    print('Reserva final:', reserva_final, 'kWh')
    if aviso != '':
        print(aviso)


if __name__ == '__main__':
    executar_sistema()
