import streamlit as st
import pandas as pd
# pip install plottly
import plotly.express as px
import plotly.graph_objects as go
# pip install streamlit-option-menu
from streamlit_option_menu import option_menu # Para trabalhar com meno
from query2 import conexao2 # Consulta no bando de dados


# *************** PRIMEIRA CONSULTA E ARTUALIZAÇÃO ***********************8

#CONSULTA
query = "SELECT l.*, c.nome_centro FROM tb_leituras as l INNER JOIN tb_centros AS c ON l.centro_id = c.centro_id;"

# CARREGAR OS DADOS PARA A VARIÁVEL df
df = conexao2(query)

# ATUALIZAÇÃO - BOTÃO
if st.button("Atualizar Dados"):
    df = conexao2(query)

# *************** ESTRUTURA DE FILTRO LATERAL ******************
# SIDEBAR - BARRA LATERAL

#CENTRO_ID
centro = st.sidebar.multiselect(
    "Centros",
    options=df["nome_centro"].unique(),
    default=df["nome_centro"].unique()
)


# ******************** VERIFICAÇÃO DA APLICAÇÃO DOS FILTROS ***************************

df_selecionado = df[
    (df["nome_centro"].isin(centro))
]


# ******************* DASHBOAD **********************

def PaginaInicial():

    # GRAFICOS
    df_co2 = df.groupby("nome_centro", as_index=False)["co2"].mean()

    # Barras 1 (CO2)
    fig = px.bar(
        df_co2,
        x="nome_centro",
        y="co2",
        title="Média de CO₂ por Cidade",
        labels={"nome_centro": "Cidade", "co2": "CO₂"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    
    # Barras 2 (umidade)
    df_umidade = df_selecionado.groupby("nome_centro", as_index=False)["umidade"].mean()

    fig_umidade = px.bar(
        df_umidade,
        x="nome_centro",
        y="umidade",
        title="Média de Umidade por Cidade",
        labels={"nome_centro": "Cidade", "umidade": "Umidade (%)"}
    )
    st.plotly_chart(fig_umidade, use_container_width=True)

    #Linha 1
    df_selecionado["dia_hora"] = pd.to_datetime(df_selecionado["dia_hora"], errors="coerce")

    fig_linhas = px.line(
        df_selecionado,
        x="dia_hora",
        y=["poeira_1", "co2", "umidade"],
        title="Poeira, CO₂ e Umidade ao longo do tempo",
        labels={"value": "Medição", "variable": "Indicador", "dia_hora": "Data/Hora"}
    )
    st.plotly_chart(fig_linhas, use_container_width=True)
PaginaInicial()