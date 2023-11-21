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
        * O mapa Choropleth foi simplificado por conta da nomenclatura de bairros não ser precisa.
        Além disso, o agrupamento por Cartório parece fazer mais sentido do ponto de vista prático, o que pode ser 
        alterado quando com o geo-referenciamento de cartórios.
        * Da mesma maneira, o mapa de Clusters foi simplificado, para efeito de performance, limitando o número de transações mostradas
    
    Econômico/Tributário:
    
        * O valor máximo da Base de Cálculo adotada é menor que o máximo do Valor Venal de Referência.
        Dada a sua definição (Calculado automaticamente pelo sistema, que verifica o maior valor entre o Valor de Transação
        e o Valor Venal de Referência), parece haver uma inconsistência.
        * Existem casos, onde o Valor Financiado é Maior que o Valor de Transação
        * Há valor negativo em em Valor Fnanciado, o que pode indicar erro.
"""
)