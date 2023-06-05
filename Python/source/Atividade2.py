# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 14:24:11 2023

@author: Ana Becker
"""

import pandas as pd
from matplotlib import pyplot as plt

'''
Atividade Prática 2 - Dataset notas

Agora vamos obter informações sobre o desempenho geral de estudantes do curso 
de computação. O dataset do arquivo historico-alg1_SIE_ANONIMIZADO.csv contém a
situação de 424 estudantes entre 2011 e 2020 em várias disciplinas. Cada 
estudante é representado por um número inteiro na primeira coluna (MATR_ALUNO).

Atenção: algumas matérias (códigos) "deixam" de existir, enquanto outras "surgem",
pois houve modificação curricular no período abrangido pelo dataset.
 
Analise o dataset e responda as seguintes perguntas:
'''
df = pd.read_csv("../datasets/historico-alg1_SIE_ANONIMIZADO.csv", sep = ",", decimal = ".")

df.columns

'''
['MATR_ALUNO', 'ANO', 'MEDIA_FINAL', 'SITUACAO', 'COD_ATIV_CURRIC',
       'FREQUENCIA', 'SIGLA']
      
1. Quais as top 5 disciplinas que mais geram cancelamentos por parte dos 
estudantes ao longo dos anos (plote a resposta em um gráfico);
'''
df.SITUACAO.unique()
cancelamentos = df[df.SITUACAO=='Cancelado'].groupby('COD_ATIV_CURRIC').SITUACAO.count().sort_values(ascending=False)[0:5].to_frame()

plt.bar(cancelamentos.index,cancelamentos.SITUACAO,  width=0.4, color = 'grey', label='Número de cancelamentos')
plt.xlabel('Disciplina')
plt.ylabel('Numero de cancelamentos')
for i, v in enumerate(cancelamentos.SITUACAO):
    plt.text(i, v, str(v), ha='center', va='bottom', fontsize=6)
plt.savefig('../img/Atividade2/top_5_cancelamentos.png', dpi=300, format='png', bbox_inches='tight', transparent=False)


'''
2. Quais as top 5 disciplinas que possuem aprovações em geral?
'''
aprovacoes_top = df[df.SITUACAO=='Aprovado'].groupby('COD_ATIV_CURRIC').COD_ATIV_CURRIC.count().sort_values(ascending=False)[0:5].to_frame()

plt.bar(aprovacoes_top.index,aprovacoes_top.COD_ATIV_CURRIC,  width=0.4, color = 'grey', label='Número de cancelamentos')
plt.xlabel('Disciplina')
plt.ylabel('Numero de aprovações')
for i, v in enumerate(aprovacoes_top.COD_ATIV_CURRIC):
    plt.text(i, v, str(v), ha='center', va='bottom', fontsize=6)
plt.savefig('../img/Atividade2/top_5_aprovacoes.png', dpi=300, format='png', bbox_inches='tight', transparent=False)


'''
3. Quais disciplinas possuem taxa de aprovação maior que 70% durante o todo 
o período?
'''
aprovados = df[df.SITUACAO=='Aprovado'].groupby('COD_ATIV_CURRIC').COD_ATIV_CURRIC.count()
total = df.groupby('COD_ATIV_CURRIC').COD_ATIV_CURRIC.count()
taxa_aprov = (aprovados/total).sort_values(ascending=False)

aprovados = aprovados.to_frame().rename(columns={"COD_ATIV_CURRIC": "Aprovados"})
total = total.to_frame().rename(columns={"COD_ATIV_CURRIC": "Total"})
taxa_aprov = taxa_aprov.to_frame().rename(columns={"COD_ATIV_CURRIC": "Taxa"})
tabela_aprov = pd.concat([aprovados, total, taxa_aprov], axis = 1)
#tabela = tabela[tabela.Total!=1]
tabela_aprov = tabela_aprov[tabela_aprov.Taxa>0.7].Taxa.sort_values(ascending=False)
tabela_aprov.index

'''
4. Quais disciplinas possuem taxa de reprovação maior que 70% a cada vez que 
são oferecidas (ex.: DiscXYZ teve 75% de reprovação em 2012; DiscABC teve 99% 
de reprovação em 2019, etc.)?
'''

reprovados = pd.concat([df[df.SITUACAO=='R-nota'],df[df.SITUACAO=='Reprov Conhecimento'],df[df.SITUACAO=='Reprovado por Frequencia']]).groupby(['COD_ATIV_CURRIC','ANO']).COD_ATIV_CURRIC.count().to_frame().rename(columns={"COD_ATIV_CURRIC": "Reprovados"})
total = df.groupby(['COD_ATIV_CURRIC','ANO']).COD_ATIV_CURRIC.count().to_frame().rename(columns={"COD_ATIV_CURRIC": "Total"})
tabela_rep = pd.concat([reprovados, total], axis = 1)
tabela_rep['Taxa'] = tabela_rep.Reprovados/tabela_rep.Total

tabela_rep = tabela_rep[tabela_rep.Taxa>0.7].Taxa.sort_values(ascending=False)
tabela_rep.reset_index().COD_ATIV_CURRIC

'''
5. Das disciplinas com reprovações, qual o máximo de vezes que um estudante 
teve que se matricular, excluindo cancelamentos, para ser aprovado?
'''
df_aprov_reprov = pd.concat([df[df.SITUACAO=='Aprovado'],df[df.SITUACAO=='R-nota'],df[df.SITUACAO=='Reprov Conhecimento'],df[df.SITUACAO=='Reprovado por Frequencia']])
matriculas_necessarias = df_aprov_reprov.groupby(['MATR_ALUNO','COD_ATIV_CURRIC']).count().SITUACAO
matriculas_necessarias.max()

aprovacao = df[df.SITUACAO=='Aprovado'].groupby(['MATR_ALUNO','COD_ATIV_CURRIC']).count().SITUACAO

resultado = matriculas_necessarias.to_frame().rename(columns={"SITUACAO": "n"}).join(aprovacao.to_frame())
resultado = resultado[resultado.SITUACAO==1]
resultado.n.max()

df_aprov_reprov[df_aprov_reprov.COD_ATIV_CURRIC=='CI055'][df_aprov_reprov.MATR_ALUNO==1]

'''
6. Como evoluem as taxas aprovados/reprovados nas disciplinas ao longo do tempo?
'''
aprovados = df[df.SITUACAO=='Aprovado'].groupby('ANO').COD_ATIV_CURRIC.count().to_frame().rename(columns={"COD_ATIV_CURRIC": "Aprovados"})
reprovados = pd.concat([df[df.SITUACAO=='R-nota'],df[df.SITUACAO=='Reprov Conhecimento'],df[df.SITUACAO=='Reprovado por Frequencia']]).groupby('ANO').COD_ATIV_CURRIC.count().to_frame().rename(columns={"COD_ATIV_CURRIC": "Reprovados"})
total = df.groupby('ANO').COD_ATIV_CURRIC.count().to_frame().rename(columns={"COD_ATIV_CURRIC": "Total"})
tabela = pd.concat([aprovados, reprovados, total], axis=1)
tabela['Taxa_apr'] = tabela.Aprovados/tabela.Total*100
tabela['Taxa_rep'] = tabela.Reprovados/tabela.Total*100
tabela['Outros'] = 100-tabela.Taxa_apr-tabela.Taxa_rep



dic={'Taxa_apr': "Taxa de aprovação (%)",
     'Taxa_rep': "Taxa de reprovação (%)",
     'Aprovados': "Número de aprovações",
     'Reprovados': "Número de reprovações", 
     'Total': "Total"}
#'COD_ATIV_CURRIC', 'ANO', 'Aprovados', 'Reprovados', 'Total','Taxa_apr', 'Taxa_rep', 'Outros'
plt.close()
for col in ['Taxa_apr', 'Taxa_rep', 'Aprovados', 'Reprovados', 'Total']:
    variavel = tabela[col]
    plt.bar(tabela.index, variavel, width=0.4, color='grey', label='Notas aprovadas')
    plt.xlabel('Ano')
    plt.ylabel(dic[col])
    plt.xlim([tabela.index.min() - 1, tabela.index.max() + 1])
    plt.ylim([0, tabela[col].max() * 1.05])
    for i in range(len(tabela[col])):
        ano = tabela.reset_index().ANO[i]
        v = tabela[col][ano]
        plt.text(ano, v, f'{v:.0f}', ha='center', va='bottom', fontsize=6)
    plt.savefig(f'../img/Atividade2/{col}.png', dpi=300, format='png', bbox_inches='tight', transparent=False)
    plt.close()
    
    
tabela.Taxa_apr.mean()
tabela.Taxa_rep.mean()

tabela.to_csv("../tabela/Resultados Atividade 2.csv", sep=';', decimal=',', index= False)