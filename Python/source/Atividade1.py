# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 20:46:05 2023

@author: Ana Becker
"""

import pandas as pd
from matplotlib import pyplot as plt

'''
Vamos obter informações sobre o rendimento de alunos de um curso em algumas 
disciplinas ao longo dos anos.

O primeiro arquivo contido no Dataset Notas, historico-alg1_SIGA_ANONIMIZADO.csv,
refere-se ao aproveitamento de estudantes na disciplina ALGORITMOS 1 entre os 
anos de 2011 e 2022.

A primeira coluna ("matricula") é composta por números inteiros, onde cada 
número representa um indivíduo. Assim, repetições nessa coluna indicam que
 o estudante fez mais de uma vez a mesma matéria.

Atenção: R-nota indica REPROVAÇÃO POR NOTA e R-freq REPROVAÇÃO POR FALTA.
Se houver outro "status" para  representar reprovação, este dever ser trocado
para o rótulo adequado (R-nota ou R-freq). Frequências < 75 causam reprovação 
por falta; Médias abaixo de 50 causam reprovação por nota.

Analise o dataset do referido arquivo para responder as seguintes perguntas:
    
'''    

df = pd.read_csv("../datasets/historico-alg1_SIGA_ANONIMIZADO.csv", sep = ",", decimal = ".")
df = df[df.tipo!='EQUIVALENCIA']
df.columns
 
'''
Tratamento de caso específico
Foi considerado que a reprovação do aluno que realizou prova de aproveitamento de conhecimento foi por motivo de nota.
'''
df.status.unique()
e = df[df.status=='Reprovado']
df.loc[ df.status=='Reprovado', 'status'] = 'R-nota'

'''
1. Qual é a média de nota dos aprovados (no período total e por ano)?
'''
df[df.status=="Aprovado"].nota.mean()
notas_aprov = df[df.status=="Aprovado"].groupby(['ano','periodo']).nota.mean()

'''
2. Qual é a média de nota dos reprovados por nota (período total e ano)?
'''
df[df.status=='R-nota'].nota.mean()
notas_rep_notas = df[df.status=='R-nota'].groupby(['ano','periodo']).nota.mean()

'''
3. Qual é a frequência dos reprovados por nota (período total e por ano)?
'''
df[df.status=='R-nota'].frequencia.mean()
freq_rep_notas = df[df.status=='R-nota'].groupby(['ano','periodo']).frequencia.mean()

'''
4. Qual a porcentagem de evasões (total e anual)?
'''
df[df.status=="Cancelado"].status.count()/df.status.count()*100


n_evasao = df[df.status=="Cancelado"].groupby(['ano','periodo']).status.count()
n_total = df.groupby(['ano','periodo']).status.count()
evasao_perc = n_evasao/n_total*100

'''
5. Como os anos de pandemia impactaram no rendimento dos estudantes em relação
aos anos anteriores, considerando o rendimento dos aprovados, a taxa de 
cancelamento e as reprovações? Considere como anos de pandemia os anos de 
2020 e 2021.

6. Compare a volta às aulas híbrida (2022 período 1) com os anos de pandemia e
os anos anteriores.


7. Compare a volta às aulas presencial (2022 período 2) com a volta híbrida do 
item anterior.

Resposta das três perguntas anteriores a seguir:
'''
rep_freq = df[df.status=="R-freq"].groupby(['ano','periodo']).status.count()
rep_nota = df[df.status=="R-nota"].groupby(['ano','periodo']).status.count()
rep = rep_freq + rep_nota
rep_perc = rep/n_total*100
# Tabela com os resultados das perguntas
stats = pd.concat([notas_aprov,notas_rep_notas, freq_rep_notas, n_evasao, evasao_perc, rep_freq, rep_nota, rep, rep_perc, n_total], axis = 1)
stats.columns = columns=['notas_aprov','notas_rep_notas', 'freq_rep_notas', 'n_evasao', 'evasao_perc', 'rep_freq', 'rep_nota','rep', 'rep_perc','n_total']
stats.reset_index(inplace=True)

# Criando uma coluna tempo para aparecer no gráfico
stats.loc[stats.periodo == '1','tempo']= stats.ano
stats.loc[stats.periodo == '2','tempo']= stats.ano +0.5
stats.loc[stats.periodo == 'Anual','tempo']= stats.ano

stats.to_csv("../tabela/Resultados Atividade 1.csv", sep=';', decimal=',', index= False)

dic={'notas_aprov': "Notas dos aprovados",
     'notas_rep_notas': "Notas dos reprovados por nota",
     'freq_rep_notas': "Frequência dos reprovados por nota",
     'n_evasao': "Número de evasões", 
     'evasao_perc': "Percentual de evasões",
     'rep_freq': "Número de reprovados por frequência",
     'rep_nota': "Número de reprovados por nota",
     'rep' : "Número de reprovações", 
     'rep_perc': "Percentual de reprovações",
     'n_total': 'Número total de alunos'}

stats = stats[stats.periodo!='Anual'].reset_index(drop=True)


for col in ['notas_aprov','notas_rep_notas','freq_rep_notas','n_evasao', 'evasao_perc', 'rep_freq', 'rep_nota','rep', 'rep_perc','n_total']:
    variavel = stats[col].reset_index(drop=True)
    plt.bar(stats.tempo, variavel, width=0.4, color = 'grey', label='Notas aprovadas')
    plt.xlabel('Ano')
    plt.ylabel(dic[col])
    plt.xlim([stats.ano.min()-1, stats.ano.max()+1])
    plt.ylim([0, stats[col].max()*1.05])
    plt.axvline(x=2019.75, color='red', linestyle='--')
    plt.axvline(x=2021.75, color='red', linestyle='--')
    for i in range(len(stats[col])):
        v = stats[col][i]
        if pd.isna(v):
            v = 0
            a = ""
        else:
            a = f'{v:.0f}'
        x = stats.tempo[i]
        plt.text(x, v, a, ha='center', va='bottom', fontsize=6)
    plt.savefig(f'../img/Atividade1/{col}.png', dpi=300, format='png', bbox_inches='tight', transparent=False)
    plt.close()
    
    
    
   

    
'''
Conforme pode ser visto nas figuras, a pandemia contribuiu para o aumento do número de evasões,
especialmente no primeiro semestre de 2020 e de 2021, nos quais ocorreram 17 e 12 evasões, respectivamente.
O número de reprovados por falta e por nota aumentou no início de 2021, chegando a um total de 34
reprovações no ano de 2021.

Conforme figuras geradas no exercício anterior, as reprovações no primeiro período de 2022 foram 
na mesma ordem de grandeza do primeiro semestre de 2021, indicando que o retorno às aulas híbridas 
também causaram alterações nos rendimentos dos alunos. Entretanto, o percentual de evasão diminuiu 
em relação aos anos de 2020 e 2021.

No dataset fornecido não há dados relativos ao rendimento dos alunos no segundo período de 2022. 
Entretanto, podemos notar que o número total de alunos seguiu o mesmo padrão dos anos anteriores,
com diminuição das matriculas no segundo semestre.
'''