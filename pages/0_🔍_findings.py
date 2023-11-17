import streamlit as st

st.markdown(
    """
    Cada linha da base ITBI equivale a uma Declaração de Transações Imobiliárias - DTI 
    efetivamente paga no mês de referência da tabela, independente da data de preenchimento da declaração e 
    da data de transação (*).
    A análise desta base foi feita por dois pontos de vista: 
        
        1) Ciência dos Dados
        2) Econômico
        
    Ciência dos dados:
        
        * Nem todos os anos estão disponíveis. Por exemplo, os dados não estão disponíveis para os período de 2019 a 2022,
        o que prejudica muito os estudos de série temporal e outros.
        * Como esperado, existem variáveis (colunas) com valores incompatíveis com seu propósito ou não preenchidas.
        * Algumas colunas precisam ser repadronizadas, pois de ano para ano, seu formato é alterado.
    
    Econômico:
    
        * 
"""
)