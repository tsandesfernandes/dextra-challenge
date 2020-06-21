#!/usr/bin/env python
# coding: utf-8

#Read an CSV file with the assets;
#Calculate the IRR(You must create your own algorithm (don't use any python mathematical function for that) we want to test your logical thinking here
#Consume a public web service that return the Selic rate of the day;
#Show the IRR calculated and the Selic rate in console;
#Store the information of the CSV file, the calculated IRR and Selic rate in a in memory database - Feel free to use structure or framework you like.
#Create a Docker image with the application ready to use;

import requests
import re
import pandas as pd
import numpy as np
from datetime import datetime
from utils import *
from dbutils import *

#leitura direta do git da cinq em formato raw
print("\nCarregando CSV de ativos do github...")
df = pd.read_csv("https://raw.githubusercontent.com/cinqtechnologies/big-data-python/master/Ativos.csv", delimiter=";")
#data do dia para passar como parametro do investimento
hoje =datetime.today()
#investimento de 300k com data atual
print("\nCriando operação de investimento...")
investimento = pd.DataFrame({'Ativo':['Investimento'],'preco':[-300000],
                             'vencimento':[datetime(hoje.year, hoje.month, hoje.day)]})

print("\nCriando db em memória...")
conn = memoryDB()

print("\nExcluindo colunas desnecessárias...")
df = df.drop(columns=['Unnamed: 3','Unnamed: 4', 'Unnamed: 5'])

print("\nEstruturando os tipos das colunas...")
#tratamento das colunas
df.Ativo = df.Ativo.astype(str)
df.vencimento = pd.to_datetime(pd.Series(df.vencimento), format="%d/%m/%Y")
#replace R escape cifrao mais o ponto para remover dos milhares e o espaco entre cifrao e numero
df.preco = df.preco.replace('[R\$. ]', '', regex=True).replace(",", ".",regex=True)
df.preco = df.preco.astype('float')


print("\nInserindo a operação de investimento no dataframe...")
# Insere investimento com data atual como primeira linha, resetando o indice
df = pd.concat([investimento, df]).reset_index(drop = True)


#pega as colunas de vencimento e preco como entrada para calcular o indice irr com 'uneven cashflow'
print("\nCalculando o IRR...")
fluxoCaixa = df[['vencimento','preco']].values.tolist()
irrIndice = xirr(fluxoCaixa)

print("\nInserindo o IRR no dataframe...")
df['irr'] = irrIndice


print("\nBuscando a ultima taxa selic do api.bcb.gov.br")
selic = parseSelic()

print("\nInserindo a taxa do dia no dataframe...")
df['selic_dia'] = selic.data
df['selic_dia'] = selic.valor


print('\nindice IRR {} e indice SELIC ano {}'.format(round(irrIndice,4), round(float(selic.valor)*12,4) ))
print("\nInserindo o dataframe em memoria...")
insertSql(df,conn)

print("\nBuscando as informações do db em memoria...")
resultado = selectSQL(querySQL, conn)

print(resultado)

print("\nFinalizando...")
conn.close()
