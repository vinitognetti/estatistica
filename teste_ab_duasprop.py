#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 17:35:19 2021

Esse é um script para teste A/B de duas amostras de duas populações que seguem
uma Distribuíção de Bernoulli.

A hipótese testada é 
    
    Ho: p1 = p2
    Ha: p1 > p2

@author: vinicius
"""
# Importando módulos necessários
import pandas as pd
from scipy.stats import norm

# Criando um dicionário para a tabela
tabela = {'A': [298, 202], 
          'B': [147, 153]}

# Criando a tabela como um DataFrame pandas
df = pd.DataFrame(tabela, index=['Sucesso (p)', 'Fracasso (1 - p)'])

# Definindo nível de significância
alpha = 0.1

# Calculando as somas

nA = df.iloc[:, 0].sum()
nB = df.iloc[:, 1].sum()

# Calculando as probabilidades amostrais
pA = df.iloc[0, 0] / nA
pB = df.iloc[0, 1] / nB

# Calculando a probabilidade amostral conjunta
pc = (nA * pA + nB * pB) / (nA + nB)

# Calculando a estatística de teste
zo = (pA - pB) / ((pc * (1 - pc) * (1/nA + 1/nB)) ** 0.5)

# Calculando o p-valor
p_valor = round(1 - norm(0, 1).cdf(zo), 5)

# Imprimindo os resultados
print(df)
print('-'*50)
print(
f"""Hipótese nula: Sucesso de A é igual a Sucesso de B
Hipótese Alternativa: Sucesso de A é maior que Sucesso de B
{'-'*50}
Nível de significância: {alpha}
P-valor: {p_valor}

Hipótese nula {'foi' if p_valor <= alpha else 'não foi'} rejeitada."""
)
