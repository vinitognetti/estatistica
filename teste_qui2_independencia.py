#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 10:52:06 2021

@author: vinicius
"""
import pandas as pd
import numpy as np
from scipy.stats import chi2

exc = [62, 36, 12]
sat = [84, 42, 14]
ins = [24, 22, 24]

tentativas = np.array([exc,
                      sat,
                      ins,
                      [e + s + i for e, s, i in zip(exc, sat, ins)]])

index = ['Excelente', 'Satisfatório', 'Insatisfatório', 'Total']

colunas = [f'{i}ª tentativa' for i in range(1, 4)]

tabela = pd.DataFrame(tentativas, index=index, columns=colunas)

tabela['Total'] = [sum(tabela.iloc[i, :]) for i in range(4)]

total = tabela.iloc[tabela.shape[0]-1, tabela.shape[1]-1]

tent_esp = [[tabela.iloc[i, tabela.shape[0]-1] * \
           tabela.iloc[tabela.shape[0]-1, j] / total for j in range(3)]
            for i in range(3)]

tabela_esperado = pd.DataFrame(np.array(tent_esp),
                               index=['Excelente', 'Satisfatório', 
                                      'Insatisfatório'],
                               columns=colunas)

alpha = 0.05

va = chi2(4)

rc = [round(va.ppf(1-alpha), 3), '+Inf']

chi2_obs = sum([sum([((tabela.iloc[i, j] - tabela_esperado.iloc[i, j]) ** 2) / \
             tabela_esperado.iloc[i, j] for j in range(3)]) for i in range(3)])
    
p_valor = 1 - va.cdf(chi2_obs)
    
print('VALORES OBSERVADOS:')     
print(tabela)
print('-'*40)
print('VALORES ESPERADOS:')
print(tabela_esperado)
print('-'*40)
print(f'''Região Crítica: {rc}
Valor Observado: {round(chi2_obs, 3)}
P-Valor: {round(p_valor, 5)}''')
