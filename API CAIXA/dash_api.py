import streamlit as st
import pandas as pd
# pip install plottly
import plotly.express as px
# pip install streamlit-option-menu
from streamlit_option_menu import option_menu # Para trabalhar com meno
from query2 import conexao2 # Consulta no bando de dados

import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from sqlalchemy import create_engine
# *************** PRIMEIRA CONSULTA E ARTUALIZAÇÃO ***********************8

#CONSULTA
# query = "SELECT l.*, c.nome_centro FROM tb_leituras as l INNER JOIN tb_centros AS c ON l.centro_id = c.centro_id;"

# # CARREGAR OS DADOS PARA A VARIÁVEL df
# df = conexao2(query)

# # ATUALIZAÇÃO - BOTÃO
# if st.button("Atualizar Dados"):
#     df = conexao2(query)

engine = create_engine("mysql+mysqlconnector://groupo5:senai%40134@projetointegrador-grupo-5.mysql.database.azure.com:3306/db_analise")

df = pd.read_sql("SELECT * FROM tb_leituras;", engine)

# Autenticação com Service Account


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=8080)

service = build("gmail", "v1", credentials=creds)

# Criar email
def criar_mensagem(destinatario, assunto, conteudo):
    mensagem = MIMEText(conteudo)
    mensagem["to"] = destinatario
    mensagem["subject"] = assunto
    return {"raw": base64.urlsafe_b64encode(mensagem.as_bytes()).decode()}

# Enviar
def enviar_email(usuario, mensagem):
    print('foi?')
    return service.users().messages().send(userId=usuario, body=mensagem).execute()

if not df['umidade'].empty:
    msg = criar_mensagem(
        "gabryellfrancesco@gmail.com, pataquinig12@gmail.com",
        "🚨 Alerta de Qualidade do Ar",
        "Os níveis de poluição subiram no centro de SP."
    )
    enviar_email("me", msg)



# *************** ESTRUTURA DE FILTRO LATERAL ******************
# SIDEBAR - BARRA LATERAL

#CENTRO_ID
centro = st.sidebar.multiselect(
    "Centros",
    options=df["nome_centro"].unique(),
    default=df["nome_centro"].unique()
)


# Converter para datetime
df["dia_hora"] = pd.to_datetime(df["dia_hora"], errors="coerce")

# Remover linhas sem data
df = df.dropna(subset=["dia_hora"])

# Se depois de limpar o dataframe ficar vazio, previne erro no slider
if not df.empty:
    min_data = df["dia_hora"].min()
    max_data = df["dia_hora"].max()

    data = st.sidebar.slider(
        "Intervalo das Datas",
        min_value=min_data,
        max_value=max_data,
        value=(min_data, max_data),
        format="YYYY-MM-DD"
    )
else:
    st.warning("⚠️ Nenhum dado válido encontrado na coluna 'dia_hora'.")
    data = (None, None)


# ******************** VERIFICAÇÃO DA APLICAÇÃO DOS FILTROS ***************************

df_selecionado = df
# df[
#     (df["nome_centro"].isin(centro)) &
#     (df["dia_hora"] >= data[0]) &
#     (df["dia_hora"] <= data[1])
# ]


# ******************* DASHBOAD **********************
# CARDS DE VALORES

def PaginaInicial():
    #Expande para selecionar as opções
    with st.expander("Tabela de Leituras"):
        exibicao = st.multiselect("Filtro",
                                  df_selecionado.columns,
                                  default = [],
                                  key="Filtro_Exibicao"
                                  )
        
        if exibicao:
            st.write(df_selecionado[exibicao])

    if not df_selecionado.empty:
        centro = df_selecionado["centro"].mean()
        data_hora = df_selecionado

