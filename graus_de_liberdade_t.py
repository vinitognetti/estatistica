#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 16:24:54 2021

Esse script calcula alguns valores para um teste-T com duas amostras

@author: vinicius
"""
import numpy as np

def media_amostral(dados):
    
    m = sum(dados) / len(dados)
    
    return np.round(m, 3)

def variancia_amostral(dados):
    
    m = media_amostral(dados)
    
    s = sum([(xi - m) ** 2 for xi in dados]) / (len(dados) - 1)
    
    return np.round(s, 3)

def graus_de_liberdade_t(dados1, dados2):
    
    n1 = len(dados1)
    n2 = len(dados2)
    
    v1 = variancia_amostral(dados1)
    v2 = variancia_amostral(dados2)
    
    A = v1 / n1
    
    B = v2 / n2
    
    v = (A + B)**2 / (A**2 / (n1 - 1) + B**2 / (n2 - 1))
                        
    return np.round(v)

def valor_observado_t(dados1, dados2):
    
    m1 = media_amostral(dados1)
    m2 = media_amostral(dados2)
    
    s1 = variancia_amostral(dados1)
    s2 = variancia_amostral(dados2)
    
    n1 = len(dados1)
    n2 = len(dados2)
    
    to = (m1 - m2) / (s1 / n1 + s2 / n2) ** 0.5
    
    return np.round(to, 3)

# MAIN

liberais = [6.6, 10.3, 10.8, 12.9, 9.2, 12.3, 7.0]
adms = [8.1, 9.8, 8.7, 10.0, 10.2, 8.2, 8.7, 10.1]

nl = len(liberais)
xl = media_amostral(liberais)
sl = variancia_amostral(liberais)

na = len(adms)
xa = media_amostral(adms)
sa = variancia_amostral(adms)

v = graus_de_liberdade_t(liberais, adms)

to = valor_observado_t(liberais, adms)

print(f'LIBERAIS:\nn: {nl}\nMédia Amostral: {xl}\nVariância Amostral: {sl}')
print('-'*40)
print(f'ADMINISTRADORES:\nn: {na}\nMédia Amostral: {xa}\nVariância Amostral: {sa}')
print('-'*40)
print(f'Graus de liberdade para Distribuíção-T: {v}')
print('-'*40)
print(f'Valor observado: to = {to}')
