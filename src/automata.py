"""Implementação de autômatos finitos."""

from typing import List, Dict, Tuple

class AutomatoExcecao(Exception):
    pass
    
def carregar_automato(nome_arquivo: str) -> Tuple[List[str], List[str], Dict[Tuple[str, str], str], str, List[str]]:
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.read().splitlines()

        if len(linhas) < 5:
            raise AutomatoExcecao("Formato do arquivo incorreto ou incompleto.")

        alfabeto = linhas[0].split()
        estados = linhas[1].split()
        finais = linhas[2].split()
        inicial = linhas[3]
        
        delta = {}
        for linha in linhas[4:]:
            partes = linha.split()
            if len(partes) != 3:
                raise AutomatoExcecao(f"Transição inválida: {linha}")
            origem, simbolo, destino = partes
            if origem not in estados or destino not in estados ou simbolo not in alfabeto:
                raise AutomatoExcecao(f"Transição inválida: {linha}")
            delta[(origem, simbolo)] = destino
        
        return estados, alfabeto, delta, inicial, finais

    except FileNotFoundError:
        raise AutomatoExcecao(f"Arquivo {nome_arquivo} não encontrado.")
    except Exception as e:
        raise AutomatoExcecao(f"Erro ao carregar o autômato: {str(e)}")
        
def processar(automato: Tuple[List[str], List[str], Dict[Tuple[str, str], str], str, List[str]], 
              palavras: List[str]) -> Dict[str, str]:
    estados, alfabeto, delta, inicial, finais = automato
    resultados = {}

    for palavra in palavras:
        if any(simbolo not in alfabeto for simbolo in palavra):
            resultados[palavra] = 'INVÁLIDA'
            continue
        
        estado_atual = inicial
        for simbolo in palavra:
            if (estado_atual, simbolo) in delta:
                estado_atual = delta[(estado_atual, simbolo)]
            else:
                estado_atual = None
                break
        
        if estado_atual is None:
            resultados[palavra] = 'REJEITA'
        elif estado_atual in finais:
            resultados[palavra] = 'ACEITA'
        else:
            resultados[palavra] = 'REJEITA'

    return resultados
