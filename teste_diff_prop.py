#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 18:55:54 2021

Esse script é de um teste para diferença de proporções.

A hipótese testada é

        Ho: p1 - p2 = d
        Ha: p1 - p2 > d

Esse teste foi feito baseando-se no calculo de uma região crítica a partir
de um valor para P(Erro I) e depois o cálculo da estatística do teste, em 
contrapartida com o cálculo do p-valor.

Também é cálculado um intervalo de confiança de 95%.

@author: vinicius
"""
# Importando módulos necessários
import pandas as pd
from scipy.stats import norm

# Criando um dicionário para a tabela
tabela = {'A': [170, 230], 
          'B': [194, 431]}

# Criando a tabela como um DataFrame pandas
df = pd.DataFrame(tabela, index=['Sucesso    (p)', 'Fracasso (1 - p)'])

# Definido a diferença esperada
d_pop = 0.1

# Definindo nível de significância
alpha = 0.05

# Calculando a região crítica
rc = norm.ppf(1 - alpha)

# Calculando a diferença das amostras e seu desvio padrão
d_amostra = p1 - p2
dp_diff = (d_amostra * (1 - d_amostra) / (n1 + n2)) ** 0.5

# Calculando um intervalo de confiança de nível 95%
ic = [d_amostra + z * dp_diff for z in norm.ppf([0.025, 0.975])]

# Calculando as somas
n1 = df.iloc[:, 0].sum()
n2 = df.iloc[:, 1].sum()

# Calculando as probabilidades amostrais
p1 = df.iloc[0, 0] / n1
p2 = df.iloc[0, 1] / n2

# Calculando a estatística do teste
zo = ((p1 - p2) - d_pop) / (((p1 * (1 - p1)) / n1 + (p2 * (1 - p2)) / n2) ** 0.5)

# Imprimindo os resultados
print(
f"""{df}
{'-'*40}
Hipótese nula: A diferença das proporções é {d_pop}
Hipótese alternativa: A diferença das proporções é maior que {d_pop}
{'-'*40}
Nível de Significância: {alpha*100}%

Região Crítica: ]{round(rc, 4)}; +Inf[
Valor observado: {round(zo, 4)}

Como o valor observado{' não' if zo <= rc else ''} pertence à região crítica,
a hipótese nula {'não foi' if zo <= rc else 'foi'} rejeitada.
{'-'*40}
Intervalo de Confiança 95%: ]{round(ic[0], 4)}; {round(ic[1], 4)}[
{'-'*40}
""")
