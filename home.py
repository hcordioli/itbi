""" ITBI Home Page 

Página inicial do Dashboard do dataset ITBI.

ITBI é o Imposto sobre Transferência de Bens Imóveis
A Prefeitura de São Paulo disponibiliza em planilhas, o registro de cada transação em 
    https://www.prefeitura.sp.gov.br/cidade/secretarias/fazenda/acesso_a_informacao/index.php?p=31501
    
Este Dashboard pretende elucidar estes dados.
"""

import streamlit as st

st.set_page_config(
    page_title="Dashboard ITBI",
    page_icon="🔍",
)

st.write("# Bem vindo ao Dashboard ITBI 🔍")

st.markdown(
    """
    Página inicial do Dashboard do dataset ITBI
    
    ITBI é o Imposto sobre Transferência de Bens Imóveis
    A Prefeitura de São Paulo disponibiliza em planilhas, o registro de cada transação em 
        https://www.prefeitura.sp.gov.br/cidade/secretarias/fazenda/acesso_a_informacao/index.php?p=31501
    
    Este Dashboard pretende elucidar estes dados.
    
    OBSERVAÇÃO IMPORTANTE:
    
    * Idealmente, um período contínuo de 3 anos seria necessário para este trabalho.
    Com isso, poderíamos incluir até uma previsão de arrecadação usando série temporal (ARIMA).
    Infelizmente, como podem notar no site da Prefeitura de São Paulo, os arquivos entre os anos de 
    2019 a 2022 ainda não estão disponíveis.
    O impacto neste trabalho é:
        * "Buracos" ou falta de dados durante estes anos, em alguns charts 
        * Análises restritas ao ano de 2023, em alguns charts
        * Falta da previsão de recadação do imposto ITBI
"""
)
