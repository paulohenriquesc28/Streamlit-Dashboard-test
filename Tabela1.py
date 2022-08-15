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
                   page_icon=":one:", 
                   layout="wide")

hide_st_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Atividade dos Bankers com os clientes:")
st.caption("Made by: Paulo Henrique Sousa Camargo")
st.markdown('#')

########################### Pegando o caminho dos arquivos ###########################
path = os.getcwd()

########################### Lendo a primeira tabela ###########################
tabela1 = pd.read_excel(path+r"\\PS - Base de dados 1 (correta).xlsx")
# Transformando os dados para o padrão brasileiro
tabela1['Atividade - Data adicionada'] =  pd.to_datetime(tabela1['Atividade - Data adicionada'], format='%d%m%Y')
tabela1['Atividade - Data de conclusão'] =  pd.to_datetime(tabela1['Atividade - Data de conclusão'], format='%d%m%Y')

# Organizando os dados por Data de adição e de conclusão
tabela1.sort_values(by=["Atividade - Data adicionada", "Atividade - Data de conclusão"]).reset_index()
# Renomeando as colunas para facilitar o plot
tabela1.rename(
    columns={"Atividade - Tipo":"Atividade(Tipo)",
             "Atividade - Data adicionada":"Atividade(Data adicionada)",
             "Atividade - Data de conclusão":"Atividade(Data de conclusão)"},
             inplace=True)
tabela1["Atividade(Tipo)-Descrição"] = tabela1["Atividade(Tipo)"]
########################### Lendo a primeira tabela ###########################

########################### Apresentando as metricas ###########################
m1, m2 = st.columns(2)
all_clients = tabela1['Banker'].value_counts(ascending=True).sum()
employee_w_most_clients = tabela1['Banker'].value_counts(ascending=True).max()

m1.metric(label="Total de clientes, todos Bankers:", value=round(all_clients))
m2.metric(label="O Banker com mais clientes, tem:", value=round(employee_w_most_clients))
########################### Apresentando as metricas ###########################

st.markdown('#')

col1, col2 = st.columns(2)
with col1:
    ########################### Grafico de barras apresentando os numeros de clientes ###########################
    st.subheader("Contagem total das atividades dos Bankers com os clientes.")
    A = tabela1.loc[tabela1['Banker'] == "employee A"]
    B = tabela1.loc[tabela1['Banker'] == "employee B"]
    C = tabela1.loc[tabela1['Banker'] == "employee C"]
    D = tabela1.loc[tabela1['Banker'] == "employee D"]
    E = tabela1.loc[tabela1['Banker'] == "employee E"]
    F = tabela1.loc[tabela1['Banker'] == "employee F"]
    G = tabela1.loc[tabela1['Banker'] == "employee G"]
    
    
    count_all_clients = go.Figure(data=[
                                go.Bar(name='employee A', x=A["Banker"], y=A['Atividade(Tipo)'].value_counts()),
                                go.Bar(name='employee B', x=B["Banker"], y=B['Atividade(Tipo)'].value_counts()),
                                go.Bar(name='employee C', x=C["Banker"], y=C['Atividade(Tipo)'].value_counts()),
                                go.Bar(name='employee D', x=D["Banker"], y=D['Atividade(Tipo)'].value_counts()),
                                go.Bar(name='employee E', x=E["Banker"], y=E['Atividade(Tipo)'].value_counts()),
                                go.Bar(name='employee F', x=F["Banker"], y=F['Atividade(Tipo)'].value_counts()),
                                go.Bar(name='employee G', x=G["Banker"], y=G['Atividade(Tipo)'].value_counts()),
                                ])
    count_all_clients.update_layout(barmode='group')
    st.plotly_chart(count_all_clients)
    ########################### Grafico de barras apresentando os numeros de clientes ###########################
    
with col2:
    st.subheader("Atividade dos Bankers com os respectivos clientes:")

    ListaBankers_t1 = tabela1['Banker'].to_list()
    ListaBankers_t1 = list(dict.fromkeys(ListaBankers_t1))
    ListaBankers_t1 = ["Todos"] + ListaBankers_t1

    selected_employee_t1 = st.selectbox("Selecione o banker:", ListaBankers_t1)
    
    if selected_employee_t1 == "Todos":
        
        pieChartGeral = tabela1.groupby(['Banker', "Atividade(Tipo)-Descrição"], as_index=False).agg({'Atividade(Tipo)': 'count'})
        pieChartGeral.rename(columns = {'Atividade(Tipo)':'Atividade(Tipo)-Contagem'}, inplace = True)
        pieChartGeral_Fig = px.pie(pieChartGeral, 
                                   values='Atividade(Tipo)-Contagem', 
                                   names='Atividade(Tipo)-Descrição',
                                   )
        
        pieChartGeral_Fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(pieChartGeral_Fig)
    else:
        
        pieChartOption = tabela1.loc[tabela1['Banker'] == selected_employee_t1]
        pieChartOption = pieChartOption.groupby(['Banker', "Atividade(Tipo)-Descrição"], as_index=False).agg({'Atividade(Tipo)': 'count'})
        pieChartOption.rename(columns = {'Atividade(Tipo)':'Atividade(Tipo)-Contagem'}, inplace = True)
        
        pieChartOption_fig = px.pie(pieChartOption, 
                                    values='Atividade(Tipo)-Contagem', 
                                    names='Atividade(Tipo)-Descrição',
                                    hover_data=['Banker'],)
        
        pieChartOption_fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(pieChartOption_fig)
