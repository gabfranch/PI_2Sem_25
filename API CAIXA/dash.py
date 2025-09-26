import streamlit as st
import pandas as pd
# pip install plottly
import plotly.express as px
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

df_selecionado = df[
    (df["nome_centro"].isin(centro)) &
    (df["dia_hora"] >= data[0]) &
    (df["dia_hora"] <= data[1])
]


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

