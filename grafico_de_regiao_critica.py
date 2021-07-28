#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 18:15:12 2021

@author: vinicius
"""
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style('dark')
 
def regiao_critica(va=scipy.stats.norm(0, 1), alpha=0.05, alt='!=',
                   titulo=None):
    
    if type(va) != scipy.stats._distn_infrastructure.rv_frozen:
        
        return print('Essa função só admite VAs do Scipy.')
    
    if type(alt) is not str:
        
        return print('Passe um argumento do tipo string em alt.')
    
    if type(alpha) is not float:
        
        return print('Passe um argumento do tipo float em alpha')
    
    q_min = 0.01
    q_max = 0.99
    
    x = np.linspace(va.ppf(q_min), va.ppf(q_max), 100)
    y = [va.pdf(xi) for xi in x]
    
    n = 100
    
    prob_x = np.linspace(va.ppf(q_min), va.ppf(alpha), n) if alt == '<' \
        else np.linspace(va.ppf(1-alpha), va.ppf(q_max), n) if alt == '>' \
            else np.concatenate([np.linspace(va.ppf(q_min), va.ppf(alpha/2), n),
                           np.linspace(va.ppf(1-(alpha/2)), va.ppf(q_max), n)]) 

    for prob_xi in prob_x:
        
        plt.plot([prob_xi, prob_xi], 
                 [min(y), va.pdf(prob_xi)], 
                 color='purple',
                 alpha=0.8)        
                    
    sns.lineplot(x=x, 
                 y=y, 
                 color='black')
    
    if titulo == None:
        
        plt.title(f'Região Crítica de {round(alpha*100, 2)}% ' + 
                  f'com {"Cauda Dupla" if alt == "!=" else "Cauda Única"}')

    else:
        
        plt.title(titulo)
        
# MAIN
regiao_critica(va=scipy.stats.f(25, 47), 
               alpha=0.05, 
               alt='>')
