import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu


def saiba():
    # CSS
    try:
        with open("home/style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Arquivo CSS não encontrado. Rodando sem estilo.")

    # Título e subtítulo
    st.markdown('<h1 class="animado">Ar em Foco</h1>', unsafe_allow_html=True)
    st.markdown('<h4 class="sub">Análise da Qualidade do Ar nos Centros Urbanos</h4>', unsafe_allow_html=True)

    # Conteúdo principal
    st.markdown("""
    <section class="conteudo">
    <h5 class="paragrafo">
    ⚠️ <b>ALERTA DE QUALIDADE DO AR</b><br><br>
   O Material Particulado (MP) em suspensão são partículas sólidas e líquidas microscópicas na atmosfera, como poeira e fumaça. 
 As partículas <b>MP10</b> têm diâmetro menor que 10 µm, enquanto as <b>MP2,5</b> são menores que 2,5 µm e mais perigosas, pois penetram nos pulmões e na corrente sanguínea, podendo causar doenças respiratórias e cardíacas.<br><br>
        Segundo a OMS, o Índice de Qualidade do Ar (IQA) varia de 0 a 500 e classifica o ar em seis categorias de qualidade. São elas:

    </h5>

    <h5 class="paragrafo"><b>Qualidade do Ar – MP10</b></h5>
 <ul class="paragrafo">
    <li><b> 😊 51 a 100 – Moderada</b>: aceitável; pessoas sensíveis podem sentir tosse e cansaço.</li>
    <li><b> 😐 101 a 150 – Insalubre para grupos sensíveis</b>: afeta crianças, idosos e pessoas com problemas respiratórios/cardiácos; sintomas leves.</li>
    <li><b> 😷151 a 200 – Insalubre</b>: afeta a população em geral; tosse, ardor nos olhos, nariz e garganta.</li>
    <li><b> ⚠️201 a 300 – Muito insalubre</b>: toda a população pode ter sintomas; pessoas sensíveis com sintomas graves, como falta de ar.</li>
    <li><b> ☠️Acima de 300 – Perigoso</b>: sério risco à saúde; aumento de mortes prematuras e má formação fetal.</li>
 </ul>

 <h5 class="paragrafo"><b>Qualidade do Ar – MP2,5</b></h5>
 <ul class="paragrafo">
    <li><b>😄0 a 25 – Boa</b>: sem riscos significativos à saúde.</li>
    <li><b>🤧26 a 50 – Moderada</b>: aceitável; pessoas sensíveis podem ter tosse e cansaço.</li>
    <li><b>😣 51 a 75 – Ruim</b>: afeta a população; sintomas leves a moderados, mais graves em grupos sensíveis.</li>
    <li><b>😰76 a 125 – Muito ruim</b>: toda a população pode apresentar sintomas; grupos sensíveis com risco maior.</li>
    <li><b>😵Acima de 200 – Péssima</b>: risco sério para todos; aumento de doenças respiratórias/cardiovasculares e mortes prematuras.</li>
 </ul>


    <hr>
                <h5 class="paragrafo">
    💧 <b>UMIDADE RELATIVA DO AR</b><br><br>
    Refere-se à quantidade de água em forma de vapor na atmosfera em relação ao máximo possível na temperatura observada. 
    A umidade tende a ser mais baixa no final do inverno e início da primavera, entre 12h e 16h. 
    Tanto a umidade muito alta quanto muito baixa podem afetar a saúde, principalmente respiratória e cardiovascular.
    </h5>

    <h5 class="paragrafo"><b>Problemas da alta umidade 💦:</b></h5>
    <ul class="paragrafo">
        <li>Proliferação de fungos e ácaros, causando rinite, asma, bronquite, sinusite e alergias;</li>
        <li>Sensação térmica aumentada, insolação, desidratação, desconforto térmico, pressão vascular elevada;</li>
        <li>Problemas dermatológicos: irritações, brotoejas, infecções em áreas úmidas;</li>
        <li>Olhos irritados, ardor e conjuntivite.</li>
    </ul>

    <h5 class="paragrafo"><b>Problemas da baixa umidade 🌵:</b></h5>
    <ul class="paragrafo">
        <li>Ressecamento das mucosas e complicações respiratórias;</li>
        <li>Sangramento pelo nariz;</li>
        <li>Ressecamento da pele;</li>
        <li>Irritação nos olhos.</li>
    </ul>

    <h5 class="paragrafo"><b>Estados de Criticidade ⚠️</b></h5>
    <ul class="paragrafo">
        <li><b>21-30% – Atenção:</b> Evitar exercícios ao ar livre (11h-15h), umidificar ambientes, manter-se protegido do Sol, beber água.</li>
        <li><b>12-20% – Alerta:</b> Suspender atividades externas (10h-16h), evitar aglomerações, usar soro fisiológico para olhos e narinas.</li>
        <li><b>Abaixo de 12% – Emergência:</b> Interromper atividades externas (10h-16h), suspender aglomerações em ambientes fechados, manter umidade em quartos, hospitais, etc.</li>
    </ul>
    



    <p class="rodape">
    Desenvolvido por Davi, Gabryell, Gustavo, Iara e Julio. <br>
    © 2025 - Uso educativo.
    </p>
    </section>
    """, unsafe_allow_html=True)


# 🔹 Rodar a função quando abrir o app
if __name__ == "__main__":
    saiba()
