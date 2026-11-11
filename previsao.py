"""Regressão linear simples calculada sem bibliotecas externas."""
from math import isfinite

def ajustar_reta(x, y):
    if len(x) != len(y) or len(x) < 2:
        raise ValueError('Informe duas listas de mesmo tamanho, com pelo menos dois pares.')
    if not all(isfinite(v) for v in x + y):
        raise ValueError('Os dados devem ser finitos.')
    media_x, media_y = sum(x) / len(x), sum(y) / len(y)
    denominador = sum((v - media_x) ** 2 for v in x)
    if denominador == 0:
        raise ValueError('Os valores de vento precisam variar.')
    a = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y)) / denominador
    return a, media_y - a * media_x

def prever_energia(vento, a, b):
    if not isfinite(vento) or vento < 0:
        raise ValueError('Vento deve ser finito e não negativo.')
    return max(0, a * vento + b)
