"""
@author: Paulo Henrique Sousa Camargo
"""

# Para gerenciar as tabelas xlsx.
import pandas as pd
# Para fazer as analises de dados.
import numpy as np 
# Para facilitar todos os acessos ao diretorio.
import os 
# Para plotar graficos.
import plotly.express as px 
# Para plotar graficos.
import plotly.graph_objects as go
# Para montar os dashboards interativos.
import streamlit as st
# Para pegar a datas e tempos exatos.
from datetime import datetime, timedelta

st.set_page_config(page_title="Dash Black Bird investimentos", 
                   page_icon=":two:", 
                   layout="wide")

hide_st_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Captação do mês de Maio:")
st.caption("Made by: Paulo Henrique Sousa Camargo")
st.markdown('#')

########################### Pegando o caminho dos arquivos ###########################
path = os.getcwd()

########################### Lendo a segunda tabela ###########################
'''
Lendo a segunda tabela, organizando e transformando para certos padrões utilizados no Brasil. Facilitando a visualização para algo mais cômodo.
'''
tabela2 = pd.read_excel(path+r"\\PS - Base de dados 2 (correta).xlsx")
tabela2['Data'] =  pd.to_datetime(tabela2['Data'], format='%d%b%Y')
tabela2["Data Mês"] = tabela2['Data'].dt.to_period('M')
tabela2.sort_values(by=["Data"]).reset_index()
########################### Lendo a segunda tabela ###########################

########################### Apresentando as metricas ###########################
'''
Métricas gerais de total de credito, debito e captação total (Credito - Debito).
'''
metrica1, metrica2, metrica3 = st.columns(3)
captacao_total_credito = tabela2.loc[(tabela2['Aux'] == 'C')]
captacao_total_credito = captacao_total_credito['Captação'].sum()

captacao_total_debito = tabela2.loc[(tabela2['Aux'] == 'D')]
captacao_total_debito = captacao_total_debito['Captação'].sum()
total = captacao_total_credito - captacao_total_debito

metrica1.metric(label = "Captação de crédito total:", value = captacao_total_credito)
metrica2.metric(label = "Captação de débito total:", value = captacao_total_debito)
metrica3.metric(label = "Captação total:", value = total)
########################### Apresentando as metricas ###########################

st.markdown('#')

metrica_selected_employee1, metrica_selected_employee2 = st.columns(2)


col1, col2 = st.columns(2)
with col1:
    '''
    Gráfico de linha para apresentar a evolução da captação de crédito de cada banker, no mês de Maio.
    '''
    st.subheader("Crédito:")

    ListaBankers_C = tabela2['Banker'].to_list()
    ListaBankers_C = list(dict.fromkeys(ListaBankers_C))
    ListaBankers_C.sort()
    ListaBankers_C = ["Todos"] + ListaBankers_C
    
    selectedBanker_C = st.selectbox("Selecione o employee para visualizar o Crédito:", ListaBankers_C, disabled = False)
    
    if selectedBanker_C == "Todos": 
        captacao_perBanker_C = tabela2.loc[(tabela2['Aux'] == "C")]
        captacao_perBanker_C = captacao_perBanker_C.groupby(["Data" ,"Banker", "Aux"], as_index=False).agg({'Captação': 'mean'})
    else:
        captacao_perBanker_C = tabela2.loc[(tabela2['Banker'] == selectedBanker_C) & (tabela2['Aux'] == "C")]
        captacao_perBanker_C = captacao_perBanker_C.groupby(["Data" ,"Banker", "Aux"], as_index=False).agg({'Captação': 'mean'})
        captacaoSelectedEmployee_C = captacao_perBanker_C['Captação'].sum()
        
        metrica_selected_employee1.metric(label = f"Captação de Crédito do {selectedBanker_C}:", value = captacaoSelectedEmployee_C)
    
    captacao_perBanker_C_fig = px.line(captacao_perBanker_C, 
                             x="Data",
                             y="Captação", 
                             color="Aux", 
                             hover_data=['Banker'],
    )
    st.plotly_chart(captacao_perBanker_C_fig)

with col2:
    '''
    Gráfico de linha para apresentar a evolução da captação de débito de cada banker, no mês de Maio.
    Por exemplo:
        Após uma breve analise com o dashboard foi possível concluir que o "employee C" não tem nenhum debito presente.
        Porém ele tem uma carta de crédito.
        Logo posso presumir que ele é um banker novo no mercado, e a sua carteira começara a apresentar lucro no futuro.
    '''
    st.subheader("Débito:")
    ListaBankers_D = tabela2['Banker'].to_list()
    ListaBankers_D = list(dict.fromkeys(ListaBankers_D))
    ListaBankers_D.sort()
    ListaBankers_D = ["Todos"] + ListaBankers_D
    
    selectedBanker_D = st.selectbox("Selecione o employee para visualizar o Débito:", ListaBankers_D, disabled = False)
    
    if selectedBanker_D == "Todos":
        captacao_perBanker_D = tabela2.loc[(tabela2['Aux'] == "D")]
        captacao_perBanker_D = captacao_perBanker_D.groupby(["Data" ,"Banker", "Aux"], as_index=False).agg({'Captação': 'mean'})
    else:
        captacao_perBanker_D = tabela2.loc[(tabela2['Banker'] == selectedBanker_D) & (tabela2['Aux'] == "D")]
        captacao_perBanker_D = captacao_perBanker_D.groupby(["Data" ,"Banker", "Aux"], as_index=False).agg({'Captação': 'mean'})
        
        captacaoSelectedEmployee_D = captacao_perBanker_D['Captação'].sum()
        metrica_selected_employee2.metric(label = f"Captação de Débito do {selectedBanker_D}:", value = captacaoSelectedEmployee_D)
    
    
    
    captacao_perBanker_D_fig = px.line(captacao_perBanker_D, 
                             x="Data",
                             y="Captação", 
                             color="Aux", 
                             hover_data=['Banker'],
    )
    captacao_perBanker_D_fig.update_traces(line_color='Red')

    st.plotly_chart(captacao_perBanker_D_fig)
