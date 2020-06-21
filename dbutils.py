#!/usr/bin/env python
# coding: utf-8

import sqlite3
import pandas as pd

querySQL = """
    select *
    from investimento
    order by vencimento
"""
def memoryDB():
    conn = sqlite3.connect(":memory:")
    return conn

def executeSQL(sql, conn):
    cursor = conn.cursor()
    cursor.execute(sql) 

def insertSql(df, conn):
    df.to_sql('investimento', conn, if_exists='replace')

def selectSQL(sql, conn):
    return pd.read_sql_query(sql, conn)


