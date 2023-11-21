import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import matplotlib.pyplot as plt
import locale

locale.setlocale( locale.LC_ALL, 'pt_BR.UTF-8' )

st.set_page_config(layout="wide")

if "first_display" not in st.session_state:
    st.session_state['first_display'] = True

@st.cache_data
def load_itbi_files():
    itbi_df = pd.read_csv("./data/itbi_files.zip",dtype = {'Cartório de Registro': 'object'})
    itbi_df['Descrição do uso'] = itbi_df['Descrição do uso'].map(lambda x: x[0:30])

    # Arquivo de Cartórios
    cart_tab_df = pd.read_csv("./data/cartorios_sp.csv",sep=';',dtype = {'Cartório de Registro': 'object'})

    return (itbi_df,cart_tab_df)
itbi_df,cart_tab_df = load_itbi_files()

# Divide a tela do Dashboard em Containers
# Visão 2023
col_2023_nat_uso = st.container()
cont_2023 = st.container()

# Transações
col_txs_sel_ym, col_txs_sel_tv, col_txs_sel_nu= st.columns([3,3,3])
cont_txs = st.container()

# Agrupamento por Cartórios de Valor de Transação e Contagem
cont_cart = st.container()
col_cart_display, col_cart_sel = st.columns(
    [8.5,1.5]
)

# Distribuições Tx ou Valor por Uso ou Natureza
cont_dist = st.container()
col_dist_sel, col_dist = st.columns(
    [1,9]
)

# Área do Terreno x Área Construída x Proporção
cont_area = st.container()
col_area_sel, col_area = st.columns(
    [1,9]
)

# Financiamento
cont_fin = st.container()

# Visão 2023
def plot_2023():
    df_2023 = itbi_df.loc[itbi_df['Ano da Transação'] == 2023]
    option = st.session_state['option_2023']
    if st.session_state['option_2023'] == "Natureza de Transação":
        df_2023_val = df_2023.groupby("Natureza de Transação")['Valor de Transação'].sum().reset_index()
        df_2023_val = df_2023_val.head(10)
        df_2023_val['Natureza de Transação'] = df_2023_val['Natureza de Transação'].map(lambda x: x[0:30])
        df_2023_val = df_2023_val.sort_values("Valor de Transação",ascending=True)
        df_2023_count = df_2023.groupby("Natureza de Transação")['Valor de Transação'].count().reset_index()
        df_2023_count = df_2023_count.head(10)
        df_2023_count['Natureza de Transação'] = df_2023_count['Natureza de Transação'].map(lambda x: x[0:30])
        df_2023_count.rename({"Valor de Transação":"Número de Transações"},axis=1,inplace=True)
        df_2023_count = df_2023_count.sort_values("Número de Transações",ascending=True)
    else:
        df_2023_val = df_2023.groupby("Descrição do uso")['Valor de Transação'].sum().reset_index()
        df_2023_val = df_2023_val.head(10)
        df_2023_val['Descrição do uso'] = df_2023_val['Descrição do uso'].map(lambda x: x[0:30])
        df_2023_val = df_2023_val.sort_values("Valor de Transação",ascending=True)        
        df_2023_count = df_2023.groupby("Descrição do uso")['Valor de Transação'].count().reset_index()
        df_2023_count.head(10)
        df_2023_count['Descrição do uso'] = df_2023_count['Descrição do uso'].map(lambda x: x[0:30])
        df_2023_count.rename({"Valor de Transação":"Número de Transações"},axis=1,inplace=True)
        df_2023_count = df_2023_count.sort_values("Número de Transações",ascending=True)

    fig_2023_val = px.bar(
        df_2023_val, 
        x= "Valor de Transação", 
        y= st.session_state['option_2023'],
#        color= option,
        orientation='h',
        title="Ano 2023"
    )
    fig_2023_count = px.bar(
        df_2023_count, 
        x= "Número de Transações", 
        y= st.session_state['option_2023'],
#        color= option,
        orientation='h',
        title="Ano 2023"
    )
    cont_2023.plotly_chart(fig_2023_val,use_container_width= True)
    cont_2023.plotly_chart(fig_2023_count,use_container_width= True)
    
option_2023 = col_2023_nat_uso.selectbox(
    'Natureza ou Uso',
    ["Natureza de Transação","Descrição do uso"],
    key="option_2023"
)


# Transações
def adjust_options():
    used_cols=[]
    
    legenda = st.session_state['option_n_u']
    eixo_x = st.session_state['option_y_m']
    eixo_y = st.session_state['option_t_v']

    if st.session_state['option_y_m'] == "Mes da Transação":
        used_cols.append("Mes da Transação")
    else:
        used_cols.append("Ano da Transação")

    if st.session_state['option_n_u'] == "Natureza de Transação":
        used_cols.append("Natureza de Transação")
    else:
        used_cols.append("Descrição do uso")

    if st.session_state['option_t_v'] == "Valor de Transação":
        filtered_df = itbi_df[used_cols + ["Valor de Transação"]].copy()
        filtered_df = filtered_df.groupby(used_cols).sum().reset_index()
    else:
        filtered_df = itbi_df[used_cols + ["Número do Cadastro"]].copy()
        filtered_df = filtered_df.groupby(used_cols).count().reset_index()
        filtered_df = filtered_df.rename({"Número do Cadastro":"Número de Transações"},axis=1)

    fig_txs = px.bar(
        filtered_df, 
        x= eixo_x, 
        y= eixo_y,
        color= legenda
    )
    cont_txs.plotly_chart(fig_txs,use_container_width= True)

option_y_m = col_txs_sel_ym.selectbox(
    'Eixo X',
    ["Ano da Transação","Mes da Transação"],
    key="option_y_m",
    #on_change=adjust_options
)
option_t_v = col_txs_sel_tv.selectbox(
    'Eixo Y',
    ["Número de Transações","Valor de Transação"],
    key="option_t_v",
    #on_change=adjust_options
)
option_n_u = col_txs_sel_nu.selectbox(
    'Legenda',
    ["Natureza de Transação","Descrição do uso"],
    key="option_n_u",
    #on_change=adjust_options
)

def reorder_cart():
    vt_cart_df = itbi_df[["Número do Cadastro","Valor de Transação","Cartório de Registro"]]
    vt_cart_df = vt_cart_df.groupby("Cartório de Registro")["Valor de Transação"].sum().reset_index().sort_values("Valor de Transação",ascending=False)
    vt_cart_df['Valor BRL'] = vt_cart_df['Valor de Transação'].map(lambda val: locale.currency(val, grouping=True, symbol='R$'))
    
    nt_cart_df = itbi_df[["Número do Cadastro","Cartório de Registro"]].copy()
    nt_cart_df.rename({"Número do Cadastro":"contagem"},axis=1,inplace=True)
    nt_cart_df = nt_cart_df.groupby("Cartório de Registro").count().reset_index().sort_values("contagem", ascending = False)

    cart_df = pd.merge(vt_cart_df,nt_cart_df,how='left', on='Cartório de Registro')
    cart_df = pd.merge(cart_df,cart_tab_df,how='left', on='Cartório de Registro')
    if st.session_state['cart_sort'] == "Valor":
        sort_key = "Valor de Transação"
    else:
        sort_key = "contagem"
    cart_df = cart_df.sort_values(
        sort_key,
        ascending=False)[['Cartório de Registro','Valor BRL','contagem','rua','abrangência']].head(18)
    
    col_cart_display.dataframe(cart_df.set_index(cart_df.columns[0]))
    
    return

# Visões por Cartório
with col_cart_sel:
    st.radio(
        "Modo de ordenação 👇",
        ["Valor", "Número"],
        key="cart_sort",
    #    on_change=reorder_cart
    )

# Visão de Financiamento
financ_df = itbi_df[["Valor Financiado","Tipo de Financiamento","Valor de Transação"]].copy()
financ_df['Tipo de Financiamento'] = financ_df['Tipo de Financiamento'].fillna("0.Não declarado")
# Proporção de Financiados
prop_financeiados = 100*(1 - (financ_df['Tipo de Financiamento'].value_counts()['0.Não declarado'] / financ_df['Tipo de Financiamento'].value_counts().sum()))
cont_fin.write (f"Proporção de financiados: {prop_financeiados:.2f}%")
financ_df = financ_df.loc[financ_df['Tipo de Financiamento'] != "0.Não declarado"]
financ_df = financ_df.groupby(["Tipo de Financiamento"]).agg(["sum"]).reset_index()
df_fin = financ_df[[('Tipo de Financiamento',     ''),
                    (     'Valor Financiado',  'sum'),
                    (   'Valor de Transação',  'sum')]].set_axis(['tipo', 'total_financiado', 'total_transacionado'], axis=1)

df_fin = pd.melt(
    df_fin, 
    id_vars=["tipo"],
    value_vars=['total_financiado','total_transacionado'])
df_fin['formatted_value'] = df_fin['value'].map(lambda val: locale.currency(val, grouping=True, symbol='R$'))
fig_fin = px.bar(df_fin, x='tipo', y='value',
             color='variable',barmode='group')
cont_fin.plotly_chart(fig_fin,use_container_width= True)


#if st.session_state['first_display'] == True:
plot_2023()
adjust_options()
reorder_cart()
#    st.session_state['first_display'] = False