import streamlit as st
import pandas as pd
# pip install plottly
import plotly.express as px
# pip install streamlit-option-menu
from steamlit_option_menu import option_menu # Para trabalhar com meno
from query import conexao # Consulta no bando de dados


# *************** PRIMEIRA CONSULTA E ARTUALIZAÇÃO ***********************8

#CONSULTA
query = "SELECT * FROM tb_leituras as l INNER JOIN tb_centros AS c ON l.centro_id = c.centro_id"

# CARREGAR OS DADOS PARA A VARIÁVEL df
df = conexao(query)

# ATUALIZAÇÃO - BOTÃO
if st.botton("Atualizar Dados"):
    df = conexao(query)

# *************** ESTRUTURA DE FILTRO LATERAL ******************
# SIDEBAR - BARRA LATERAL

#CENTRO_ID
centro = st.sidebar.multiselect("Centro",
                                options = df["centro"].unique(),
                                default = df["centro"].unique()
                                )


min_data = int (df["dia_hora"].min())
max_data = int (df["dia_hora"].max())

#DATA
data = st.sidebar.slider("Intervalo das Datas",
                          
                              min_value = min_data,
                              max_value = max_data,
                              value = (min_data, max_data) # Valor Inicial, Valor Final
                              )

# ******************** VERIFICAÇÃO DA APLICAÇÃO DOS FILTROS ***************************

df_selecionado = df[
    (df["centro"].isin(centro)) &
    (df["dia_hora"] >= data[0]) &
    (df["dia_hora"] <= data[1])
]


# ******************* DASHBOAD **********************
# CARDS DE VALORES

def PaginaInicial():
    #Expande para selecionar as opções
    with st.expander("Tabela de Leituras"):
        exibicao = st.multiselect("Filtro"
                                  df_selecionado.columns,
                                  default = [],
                                  key="Filtro_Exibicao"
                                  )
        
        if exibicao:
            st.writ(df_selecionado[exibicao])

    if not df_selecionado.empty:
        centro = df_selecionado["centro"].mean()
        data_hora = df_selecionado

