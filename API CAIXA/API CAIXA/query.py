import mysql.connector
import pandas as pd


def conexao(query):
    conn = mysql.connector.connect(
        host = '127.0.0.1',
        port= '3306',
        user = 'root',
        password = 'Senai@134',
        db = 'db_analise'
    )


    dataframe = pd.read_sql(query, conn)
    # Executar o SQL e armazenar o resultado no dataframe

    conn.close()

    return dataframe