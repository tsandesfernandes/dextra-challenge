import unittest
from unittest import TestCase
import pandas as pd
from datetime import datetime,date
from utils import xirr


class Teste(TestCase):



    def testTamanhaOriginal(self):
        
        df = pd.read_csv("https://raw.githubusercontent.com/cinqtechnologies/big-data-python/master/Ativos.csv", delimiter=";")

        
        self.assertEqual(len(df), 23)

    def testComInvestimento(self):
        df = pd.read_csv("https://raw.githubusercontent.com/cinqtechnologies/big-data-python/master/Ativos.csv", delimiter=";")
        hoje =datetime.today()
        investimento = pd.DataFrame({'Ativo':['Investimento'],'preco':[-300000],
                             'vencimento':[datetime(hoje.year, hoje.month, hoje.day)]})

        mdf = pd.concat([investimento, df]).reset_index(drop = True)

        self.assertEqual(len(mdf),24)

    def testxirr(self):
        tas = [ (date(2010, 12, 29), -10000),
        (date(2012, 1, 25), 20),
        (date(2012, 3, 8), 10100)]
        self.assertEqual(xirr(tas),0.010061264038086382)


if __name__ == '__main__':
    unittest.main()