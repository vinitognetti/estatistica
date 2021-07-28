#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 11:40:52 2021

@author: vinicius
"""
# Importando os módulos necessários
import pandas as pd
import numpy as np
from scipy.stats import describe, t

# Defindo uma função para o teste-T com duas amostras dependentes
def teste_t_duas_amostras_dependentes(a, b, alt='!=', alpha=0.05):
    
    """Essa função recebe duas amostras dependentes e realiza um teste-T, 
    imprimindo os resultados no console.
    ---------------------------------------
    PARÂMETROS:
        
        a: Amostra A
        
        b: Amostra B
        
        alt: Hipótese Alternativa a ser testada. != para diferença entre as 
            médias; > para média de A maior que média de B; ou < para média de
            A menor que média de B (padrão !=)
            
        alpha: nível de significância, ou probabilidade de cometer Erro do 
            Tipo I (rejeitar a Hipótese Nula quando ela é verdadeira).
            (padrão 0.05)
        
        Em geral, os tipos das amostras podem ser quaisquer valores que
        possam ser manipulados pela biblioteca pandas.
        Devem ter o mesmo número de observações."""

    # Criando uma tabela pelo DataFrame pandas
    df = pd.DataFrame({'A': a, 'B': b})
    
    # Calculando a média amostral e a variância amostral das colunas
    nA, minmaxA, A_barra, A_s2, skA, kuA = describe(df.iloc[:, 0])
    nB, minmaxB, B_barra, B_s2, skB, kuB  = describe(df.iloc[:, 1])
    
    # Calculando a diferença entre as amostras
    diff = np.array(a) - np.array(b)
    
    # Calculando uma distribuíção T(n-1)
    T = t(len(diff) - 1)
    
    # Calculando a região crítica  
    rc = [round(T.ppf(1-alpha), 3), '+Inf'] if alt == '>' \
        else ['-Inf', round(T.ppf(alpha), 3)] if alt == '<' \
            else [round(T.ppf(alpha/2), 3), round(T.ppf(1 - alpha/2), 3)]
    
    # Calculando o valor observado
    to = ((len(diff) ** 0.5) * diff.mean()) \
        / ((sum([(di - diff.mean()) ** 2 for di in diff]) \
            / (len(diff) - 1))**0.5)
        
    # Checando se o valor observado está na região crítica
    ho = to < rc[1] if alt == '<' \
        else to > rc[0] if alt == '>' \
            else ((to < rc[0]) | (to > rc[1]))
            
    # Calculando P-Valor
    p_valor = T.cdf(to) if alt == '<' \
        else 1 - T.cdf(to) if alt == '>' \
            else T.cdf(-abs(to)) + (1 - T.cdf(abs(to)))
    
    # Imprimindo um resumo descritivo e o resultado do teste
    print(
f"""{df.head(20) if df.shape[1] > 20 else df}
{'-'*40}
Amostra A:
    n: {nA}
    min: {minmaxA[0]}
    max: {minmaxA[1]}
    média: {round(A_barra, 3)}
    variância: {round(A_s2, 3)}
    
Amostra B:
    n: {nB}
    min: {minmaxB[0]}
    max: {minmaxB[1]}
    média: {round(B_barra, 3)}
    variância: {round(B_s2, 3)}
{'-'*40}
Hipótese Nula: Média de A é igual a Média de B.
Hipótese Alternativa: Média de A é {'maior' if alt == '>' else 'menor'
if alt == '<' else 'diferente'} da Média de B.
{'-'*40}
Nível de significância: {alpha}

Região Crítica: ]{rc[0]}; {rc[1]}[

Valor observado: {round(to, 3)}

A hipótese nula {'foi' if ho else 'não foi'} rejeitada.  

P-Valor: {round(p_valor, 5)}  
""")

#MAIN
# Definindo os valores para as amostras A e B
a = [13, 18, 14, 16, 19, 12, 22]
b = [16, 24, 18, 14, 26, 17, 29]

# Chamando o teste
teste_t_duas_amostras_dependentes(a, b, alt='!=', alpha=0.05)
