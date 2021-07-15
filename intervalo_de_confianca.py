#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 22:36:54 2021

Esse script é para a visualização do conceito de intervalos de confiança, bus-
cando trazer uma maior intuíção à ideia.

O produto final são dois gráficos, o primeiro com valores gamma - proporção
em que a média esteve contida nos intervalos gerados -, e o segundo com os
intervalos plotados junto com a média populacional.

Note que para valores maiores que 50 o segundo gráfico não é mostrado. Decidi
assim porque achei que a visualização ficou ruim para esses valores. Mas isso
pode ser mudado na última parte da função graficos_ic.

Quanto maior o valor de n (tamanho da amostra) melhor é o spread do intervalo,
confirmando o teorema do limite central.

@author: vinicius
"""
# Importando módulos necessários
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Definindo estilo dos gráficos
sns.set_style('whitegrid')

# Definindo uma função para gerar os intervalos de confiança
def ic(z=1.96, mu=0, sigma=1, tamanho_da_amostra=100, n_de_sims=30, 
       seed=123, mostrar=False):
    
    '''Essa função retorna uma lista de intervalos de confiança e um valor
    gamma que corresponde a porcentagem de vezes em que a media populacional
    ficou dentro dos intervalos gerados.
    
    Em chamada padrão retorna intervalos sobre uma distribuição Z.
    ------------------------------------------
    PARÂMETROS:
        
        z (float, não negativo): valor crítico de Z para definir gamma. Em cha-
        mada padrão chama-se com Z para gamma=0.95 (ou um intervalo de 95% de
        confiabilidade) (padrão=1.96)
        
        mu (float): média populacional (padrão=0)
        
        sigma (float, não-negativo): desvio padrão populacional (padrão=0)
        
        tamanho_da_amostra (int, não-negativo): tamanho da amostra retirada 
        da população (padrão=100)
        
        n_de_sims (int, não-negativo): quantidade de simulações (padrão=30)
        
        seed (int): valor para geração de número aleatório. Importa para 
        replicação de resultados (padrão=123)
        
        mostrar (bool): informa sobre o status das iterações (padrão=False)'''
        
    # Definindo o gerador de número aleatório
    np.random.seed(seed)
    
    # Inicializando uma lista para os intervalos
    lista_de_intervalos = []

    # Inicializando uma lista para os resultados do teste de continência da 
    # media populacional em um dado intervalo
    lista_res = []
    
    # Iteração para geração dos intervalos e dos resultados
    for i in range(n_de_sims):
        
        # Selecionando a amostra aleatória
        amostra = np.random.normal(mu, sigma, size=tamanho_da_amostra)
        
        # Calculando as métricas da amostra
        media_amostral = np.mean(amostra)
        sigma_amostral = sigma / (tamanho_da_amostra ** 0.5)
        
        # Definindo o intervalo
        intervalo = [media_amostral - z*sigma_amostral,
                     media_amostral + z*sigma_amostral]
        
        # Adicionando o intervalo à lista de intervalos
        lista_de_intervalos.append(intervalo)
        
        # Testando se a média está ou não no intervalos
        res = (mu > intervalo[0]) and (mu < intervalo[1])
        
        # Adicionando o resultado na lista de resultados
        lista_res.append(res)
        
        # Checando se é preciso mostrar as iterações
        if mostrar:
        
            # Calculando para mostrar as iterações em intervalos 
            # com 10 valores
            if (i+1) % (n_de_sims / 10) == 0:
                
                # Imprimindo a mensagem informando sobre a iteração
                print(f'Iteração nº {i+1} de {n_de_sims}')
            
    # Calculando a proporção de vezes em que a média populacional esteve
    # dentro de um intervalo gerado
    gamma = sum(lista_res) / n_de_sims    
    
    # Retornando a lista de intervalos e o valor gamma
    return lista_de_intervalos, gamma
    
def graficos_ic(z=1.96, m=1, mu=0, sigma=1, n=100, 
             sim=30, info=False):
    
    '''Essa função plota gráficos para valores gamma e um intervalo de 
    confiança (para ilustração do conceito) retornados pela função ic.
    
    Em chamada padrão, retorna valores sobre uma distribuíção Z.
    ----------------------------------------
    PARÂMETROS:
        
        z (float, não negativo): valor crítico de Z para definir gamma. Em cha-
        mada padrão chama-se com Z para gamma=0.95 (ou um intervalo de 95% de
        confiabilidade) (padrão=1.96)
        
        m (int, não negativo): multiplicador para os valores de seed da função
        de números aleatórios. Importa para replicabilidade dos resultados.
        (padrão=1)
        
        mu (float): média populacional (padrão=0)
        
        sigma (float, não-negativo): desvio padrão populacional (padrão=0)
        
        n (int, não-negativo): tamanho da amostra retirada 
        da população (padrão=100)
        
        sim (int, não-negativo): quantidade de simulações (padrão=30)
        
        info (bool): informa sobre o status das iterações da função
        ic (padrão=False)'''

    # Forçando os tipos de Z, m, mu, sigma, n e sim
        
    z = abs(float(z))
    m = abs(int(m))
    mu = float(mu)
    sigma = abs(float(sigma))
    n = abs(int(n))
    sim = abs(int(sim))

    # Inicializando uma lista para os valores gamma
    lista_gamma = []
    
    # Inicializando uma lista para os valores dos seeds
    x = []
    
    # Looping para geração de valores gamma e uma lista de intervalos
    for i in range(1*m, 31*m, 1*m):
        
        # Informando a iteração em que o programa está
        print(f'{int((i+1)/m)} / {int((31*m)/m - 1)}')
                
        # Gerando uma lista de intervalos e um valor gamma a partir da função 
        # ic definida anteriormente
        lista_de_intervalos, gamma = ic(mu=mu,
                      sigma=sigma,
                      tamanho_da_amostra=n,
                      n_de_sims=sim,
                      seed=i,
                      mostrar=info)
        
        # Adicionando o valor gamma encontrado à lista de valores gamma
        lista_gamma.append(gamma)
        
        # Adicionando o valor do seed na lista de seeds
        x.append(i)
        
        # Informando sobre o nível de confiança observado
        print('-'*40)
        print(f'O nível de confiança observado foi {np.round(gamma*100, 2)}%')

    # Plotando os valores gamma
    sns.scatterplot(x, lista_gamma, 
             label='Gamma', 
             color='orange',
             alpha=0.7)

    # Plotando a média dos valores gamma
    sns.lineplot(x, [np.mean(lista_gamma) for i in x], 
             label='Media Gamma', 
             color='black', 
             linestyle='--')
    
    # Definindo a escala do eixo y
    plt.yticks(np.linspace(min(lista_gamma), max(lista_gamma), 10))
    
    # Adicionando título e descrição dos eixos
    plt.title('Gamma por intervalo de confiança', fontsize=18)
    plt.xlabel('Seed', fontsize=14)
    plt.ylabel('Gamma', fontsize=14)
    
    # Forçando a legenda a aparecer
    plt.legend()
    
    # Mostrando o gráfico
    plt.show()
    
    # Checando se o número de intervalos é igual ou menor que 50. Caso for
    # maior, o gráfico não oferece uma boa visualização
    if sim <= 50:
        
        # Definindo um novo valor para a lista dos valores do eixo x, desta
        # vez com o spread da lista de intervalos
        x = np.linspace(0, len(lista_de_intervalos), len(lista_de_intervalos))
        
        # Plotando a média populacional
        sns.lineplot(x, [mu for i in x],
                     label='Média Populacional',
                     color='darkgreen',
                     ls='--')
        
        # Looping para plotar os intervalos
        for i in range(len(lista_de_intervalos)):
            
            # Plotando cada um dos intervalos na lista de intervalos
            plt.plot([i, i], 
                     [lista_de_intervalos[i][0], lista_de_intervalos[i][1]],
                     color='black',
                     alpha=0.8,
                     marker='_')
                  
        # Definindo um título e descrições para os eixos
        plt.title('Intervalos de confiança', fontsize=18)
        plt.xlabel('Nº do intervalo', fontsize=12)
        plt.ylabel('Intervalo da média amostral', fontsize=12)
        
        # Forçando a legenda a aparecer
        plt.legend()
        
        # Mostrando o gráfico
        plt.show()
      

# MAIN
# Chamada da função graficos_ic com os valores padrões
graficos_ic(z=1.96, 
            m=5, 
            mu=0, 
            sigma=1, 
            n=500, 
             sim=30, 
             info=False)
