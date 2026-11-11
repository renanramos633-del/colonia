"""Integra dados, previsão, decisões e apresentação no terminal."""
import argparse
from dados import carregar_cenario
from previsao import ajustar_reta, prever_energia
from decisoes import decidir

def executar(colonia):
    sistemas = colonia['sistemas']
    energia = sistemas['energetico']
    historico = energia['eolico']['historico']
    a, b = ajustar_reta(historico['vento'], historico['energia_eolica'])
    vento = colonia['clima']['vento']
    eolica = prever_energia(vento, a, b)
    geracao = energia['solar']['energia'] + eolica
    bateria = energia['bateria']
    resultado = decidir(geracao, sistemas['consumidores'], bateria['reserva'], bateria['capacidade'])
    resultado.update({'eolica_prevista': eolica, 'geracao': geracao, 'modelo': (a, b),
                      'extrapolacao': vento < min(historico['vento']) or vento > max(historico['vento'])})
    return resultado

def exibir(resultado):
    print('COLÔNIA AURORA | intervalo de 1 hora')
    print(f"Previsão eólica: {resultado['eolica_prevista']:.1f} kWh")
    print(f"Geração estimada: {resultado['geracao']:.1f} kWh")
    print(f"Consumo original: {resultado['consumo_original']:.1f} kWh")
    if resultado['extrapolacao']:
        print('ATENÇÃO: previsão fora da faixa histórica de vento.')
    for mensagem in resultado['mensagens']:
        print(mensagem)
    print(f"Consumo após decisão: {sum(resultado['consumos_apos_decisao'].values()):.1f} kWh")
    print(f"Reserva projetada: {resultado['depois']['reserva_final']:.1f} kWh")
    print(f"Déficit não atendido: {resultado['depois']['deficit_nao_atendido']:.1f} kWh")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cenario', choices=['deficit', 'excedente', 'equilibrio'], default='deficit')
    parser.add_argument('--vento', type=float, help='Substitui o vento do cenário, em m/s.')
    args = parser.parse_args()
    colonia = carregar_cenario(args.cenario)
    if args.vento is not None:
        colonia['clima']['vento'] = args.vento
    try:
        exibir(executar(colonia))
    except ValueError as erro:
        parser.error(str(erro))

if __name__ == '__main__':
    main()
