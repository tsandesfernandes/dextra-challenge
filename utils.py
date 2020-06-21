#!/usr/bin/env python
# coding: utf-8

import requests
import re
import json
from collections import namedtuple
from datetime import datetime
#fonte https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/10?formato=json
#https://conteudo.bcb.gov.br/api/feed/pt-br/PAINEL_INDICADORES/juros mas o selic nao é fechado 
selicUlimoDia = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"

#namedtuple cria uma subclasse de tupla com nome
selicFields = ('data', 'valor')
SelicConstruct = namedtuple('Selic', selicFields)

# internal rate of investiment com caixa irregular
def xirr(transactions):
    years = []
    for tr in transactions:
        years.append((tr[0] - transactions[0][0]).days / 365.0)

    residual = 1
    step = 0.05
    guess = 0.05
    epsilon = 0.0001
    limit = 10000
    while abs(residual) > epsilon and limit > 0:
        limit -= 1
        residual = 0.0
        for i, ta in enumerate(transactions):
            residual += ta[1] / pow(guess, years[i])
        if abs(residual) > epsilon:
            if residual > 0:
                guess += step
            else:
                guess -= step
                step /= 2.0
    return guess-1

# internal rate of investiment com caixa regular
def npv( taxa, serieValores):
    total = 0.0
    for i, valor in enumerate(serieValores):
        total += valor / (1 + taxa)**i
    return total
    #irr periodico
def irr(capital,serieValores, taxa=1.0, iteracoes=100):
    
    for i in range(1, iteracoes+1):
        taxa *= (1 - npv(taxa, serieValores) / capital)
    return taxa
    #nao periodico tem q subtrair data de hj

def parseSelic():
    output = None
    s = requests.Session()
    r = s.get(selicUlimoDia)
    listSelic = json.loads(r.text)
    selic = listSelic.pop()    
    output = SelicConstruct(datetime.strptime(selic['data'], "%d/%m/%Y").date(),  selic['valor'])
    s.close()
    return output