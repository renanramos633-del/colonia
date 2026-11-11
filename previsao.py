# Ajusta uma reta usando as listas de vento e energia.
def ajustar_reta(ventos, energias):
    media_vento = sum(ventos) / len(ventos)
    media_energia = sum(energias) / len(energias)
    numerador = 0
    denominador = 0

    for i in range(len(ventos)):
        diferenca_vento = ventos[i] - media_vento
        diferenca_energia = energias[i] - media_energia
        numerador = numerador + diferenca_vento * diferenca_energia
        denominador = denominador + diferenca_vento ** 2

    if denominador == 0:
        raise ValueError('Os valores históricos de vento precisam variar.')

    a = numerador / denominador
    b = media_energia - a * media_vento
    return a, b


def prever_energia(vento, a, b):
    energia = a * vento + b
    if energia < 0:
        energia = 0
    return energia
