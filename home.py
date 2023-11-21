""" ITBI Home Page 

Página inicial do Dashboard do dataset ITBI

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
"""
)
