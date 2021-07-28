#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 10:53:02 2021

@author: vinicius
"""
import pandas as pd
from scipy.stats import t

dados = {'A': [8, 6, 7, 5, 8],
         'B': [4, -2, 0, -2, 3],
         'C': [1, 2, 0, -1, -3],
         'D': [4, 6, 5, 5, 4],
         'E': [10, 8, 7, 4, 9]}

medidas = {}

medias = []
sqs = []
variancias = []

for i in dados.keys():
    
    media = sum(dados[i]) / len(dados[i])
    
    sq = sum([(xi - media) ** 2 for xi in dados[i]])

    var = sq / (len(dados[i]) - 1)
    
    medias.append((i, media))
    sqs.append((i, sq))
    variancias.append((i, var))
    
medidas['Média'] = medias
medidas['SQ'] = sqs
medidas['Variância'] = variancias

pares = []
diffs = []

for i in range(len(medidas['Média']) - 1):
    
    for j in range(1, len(medidas['Média'])):    
    
        par = medidas['Média'][i][0] + medidas['Média'][j][0]
        
        if (not (len(set(par)) == 1)) & (not (set(par) in pares)):
            
            diff = medidas['Média'][i][1] - medidas['Média'][j][1]

            pares.append(set(par))
            
            diffs.append((par, round(diff, 3)))

tabela = pd.DataFrame([diffs[i][1] for i in range(len(diffs))],
                      index=[diffs[i][0] for i in range(len(diffs))],
                      columns=['Diferenças entre médias'])

alpha = 0.05

alpha_estrela = 0.05 / len(diffs)

va = t(int(sum([len(i) for i in dados.values()]) - len(dados.keys())))

se = (sum([medidas['Variância'][i][1] \
           for i in range(len(medidas['Variância']))]) \
      / sum([len(i) - 1 for i in dados.values()])) ** 0.5

me = va.ppf(1 - (alpha_estrela / 2)) * se \
    * ((sum([1/(len(i) - 1) for i in dados.values()])) ** 0.5)

sig = ['Diferente' if abs(i) > me else 'Igual' \
       for i in tabela['Diferenças entre médias']]

tabela[f'Margem de Erro ({round(me, 3)})'] = sig

print(tabela)
