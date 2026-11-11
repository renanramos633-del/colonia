# Colônia Aurora: sistema integrado de energia

Projeto didático em Python 3.8 ou superior, sem dependências externas. Integra listas, dicionários hierárquicos, regras de decisão, regressão linear e balanço de energia.

## Executar

Na pasta do projeto:

```bash
python main.py
python main.py --cenario excedente
python main.py --cenario equilibrio
python main.py --vento 11
python -m unittest discover -s testes -v
```

No Linux, use `python3` se necessário. Os cenários ficam em `dados.py`; edite seus valores para experimentar outras entradas. Cada execução simula um único intervalo independente de uma hora; não persiste resultados e não aciona equipamentos reais.

## Organização

| Arquivo | Responsabilidade |
| --- | --- |
| dados.py | Listas históricas, cenários e dicionários hierárquicos |
| previsao.py | Ajuste de reta e estimativa eólica |
| decisoes.py | Regras, prioridades e balanço antes/depois |
| main.py | Integração e saída no terminal |
| testes/test_sistema.py | Seis testes automatizados |
| relatorio.pdf | Explicação do projeto |

A hierarquia parte de `colonia`, com `clima` e `sistemas`. Em `sistemas`, `energetico` contém `solar`, `eolico` e `bateria`; `consumidores` contém `suporte_vida`, `pesquisa` e `lazer`. Por exemplo: `colonia['sistemas']['energetico']['bateria']['reserva']`.

## Unidades e regras

Todas as energias estão em kWh por intervalo de uma hora; vento em m/s. A reserva também está em kWh. O termo energia baixa significa **reserva < 50 kWh**, e consumo alto significa **consumo > 60 kWh**.

1. Reserva < 50: emitir alerta para reduzir consumo.
2. Reserva < 50 E consumo > 60: ativar economia e desligar lazer e pesquisa.
3. Consumo > geração: alertar sobre déficit; usar reserva após aplicar os cortes.
4. Se geração + reserva não cobrir o consumo: desligar lazer e depois pesquisa até caber no orçamento.
5. Suporte à vida permanece prioritário. Se ainda faltar energia, emitir emergência; manter o estado ligado não garante fornecimento físico.
6. Geração > consumo: sugerir armazenamento. Respeitar a capacidade da bateria e informar sobra não armazenada.

Saldo = geração - consumo. A reserva final é limitada a zero e à capacidade. O sistema apresenta déficit não atendido quando geração e reserva são insuficientes. O balanço é calculado antes e depois das decisões.

## Previsão

Histórico sintético: vento = [8, 10, 12]; energia eólica = [20, 25, 30]. Ajuste por mínimos quadrados: a = soma((x - média_x)(y - média_y)) / soma((x - média_x)²); b = média_y - a × média_x. Resultado: energia = 2,5 × vento + 0. Para vento 11, a previsão é **27,5 kWh**. Não se trunca para 27.

A geração total estimada soma solar informada e eólica prevista. Há aviso fora da faixa histórica (8 a 12 m/s). O modelo é uma simplificação didática: três pontos sintéticos não comprovam precisão real, e turbinas reais não seguem uma reta em toda a faixa de vento. Bateria ideal, sem perdas; solar constante no intervalo. Os valores de entrada devem ser finitos e não negativos; reserva não pode superar capacidade.

## Exemplo de entrada e saída

Entrada padrão: vento 8; solar 20; reserva 40; capacidade 100; suporte à vida 30; pesquisa 25; lazer 15.

```text
COLÔNIA AURORA | intervalo de 1 hora
Previsão eólica: 20.0 kWh
Geração estimada: 40.0 kWh
Consumo original: 70.0 kWh
ALERTA: reduzir consumo; reserva abaixo de 50 kWh.
AÇÃO: ativar modo economia.
ALERTA: consumo maior que geração.
AÇÃO: desligar lazer, pesquisa; manter suporte à vida ligado.
Consumo após decisão: 30.0 kWh
Reserva projetada: 50.0 kWh
Déficit não atendido: 0.0 kWh
```

No cenário excedente, geração = 80 e consumo = 30: armazenam-se 50 kWh e a reserva passa de 40 para 90. No equilíbrio, geração e consumo são 70, sem cortes.

## Repositório público

https://github.com/renanramos633-del/colonia
