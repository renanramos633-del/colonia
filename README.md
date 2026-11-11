# Colônia Aurora - FIAP, Fase 3

Sistema integrado em Python para organizar os dados de uma colônia, prever a geração eólica e tomar decisões sobre o uso de energia. Utiliza listas, dicionários, funções, repetições e condições, sem bibliotecas externas.

## Como executar

É necessário ter Python 3 instalado. Baixe os arquivos, abra o terminal na pasta do projeto e execute:

```bash
python main.py
```

No Linux, o comando pode ser `python3 main.py`. Para alterar a entrada, edite os valores em `dados.py` e execute novamente.

## Organização dos arquivos

| Arquivo | Função |
| --- | --- |
| dados.py | Guarda os dados e a hierarquia dos sistemas |
| previsao.py | Calcula a reta e a previsão eólica |
| decisoes.py | Compara energia, aplica regras e atualiza a reserva |
| main.py | Integra as funções e apresenta as saídas |
| relatorio.pdf | Explica o sistema |

## Dados e decisões

As listas históricas são `vento = [8, 10, 12]` e `energia = [20, 25, 30]`. Os dicionários organizam clima, consumidores e sistema energético. Dentro do sistema energético estão solar, eólico e bateria.

Todas as energias são medidas em kWh, para um período de uma hora. O vento é medido em m/s. Neste projeto, energia baixa significa reserva abaixo de 50 kWh e consumo alto significa consumo acima de 60 kWh.

- Se reserva < 50: emitir alerta para reduzir consumo.
- Se reserva < 50 E consumo > 60: ativar economia e desligar lazer e pesquisa.
- Se consumo > geração: alertar sobre o déficit.
- Se geração > consumo: sugerir armazenamento.
- Se geração + reserva não atender ao consumo: desligar lazer e depois pesquisa, conforme necessário.
- Manter suporte à vida como prioridade; emitir emergência se a energia continuar insuficiente.
- Atualizar a reserva sem ultrapassar a capacidade ou ficar abaixo de zero; informar energia excedente ou faltante.

## Previsão por regressão

A função ajusta uma reta `energia = a * vento + b` por mínimos quadrados. Com as listas de exemplo, o resultado é `energia = 2,5 * vento`. Para vento de 11 m/s, a previsão é **27,5 kWh**. Essa previsão é somada à energia solar e usada nas decisões.

## Exemplo de entrada

Vento = 8; solar = 20; reserva = 40; capacidade = 100; suporte à vida = 30; pesquisa = 25; lazer = 15.

## Exemplo de saída

```text
COLÔNIA AURORA
Previsão eólica: 20.0 kWh
Geração total: 40.0 kWh
Consumo inicial: 70 kWh
Reserva inicial: 40 kWh
ALERTA: consumo maior que geração.
ALERTA: reduzir consumo; reserva abaixo de 50 kWh.
AÇÃO: ativar modo economia.
AÇÃO: desligar lazer e pesquisa.
PRIORIDADE: manter suporte à vida ligado.
Consumo após decisões: 30 kWh
Reserva final: 50.0 kWh
```

Os dados são fictícios e a bateria não considera perdas. O programa simula um período, sem controlar equipamentos reais. A reta é uma aproximação didática para os valores de vento próximos ao histórico. Os dados editados devem ser não negativos, a reserva não pode exceder a capacidade e as listas devem ter o mesmo tamanho, pelo menos dois pares e ventos diferentes.

## Repositório público

https://github.com/renanramos633-del/colonia
