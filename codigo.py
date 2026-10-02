#Passo a passo do projeto
#Passo 1: Abri a base de dados (importar)
#Passo 2: Visualizar a base de dados
    #Entender as informacoes disponiveis
    #Possiveis problemas/erros na base de dados // entender as infos disponiveis // informacoes que nao te ajudam, te atrapalham
#Passo 3: Corrigir os problemas da base de dados (tratamento de dados)
    #Valores em formatos errados
    #Informaçoes vazias
#Passo 4: Analise Inicial (entender quantos clientes cancelaram)
#Passo 5: Analise detalhada (causa do cancelamento dos clientes, como cada coluna impacta no cancelamento)


#Passo 1: Abri a base de dados (importar)
import pandas as pd
import streamlit as st
import plotly.express as px

planilha = pd.read_csv("cancelamentos.csv")


# APRESENTAÇÃO DO PROJETO
# =========================================================

st.markdown(
    """
    <h1 style="line-height: 1.1;">
        Python Insights:<br>
        Analisando Dados com Python
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("## Case: Cancelamento de Clientes")

st.write(
    """
    Uma empresa com mais de 45 mil clientes identificou que grande parte
    da sua base é composta por clientes inativos, ou seja, clientes que
    já cancelaram o serviço.

    Diante desse cenário, o objetivo deste projeto é analisar os dados
    disponíveis para entender o comportamento dos cancelamentos e identificar
    oportunidades que possam contribuir para a redução da taxa de churn.
    """
)

st.write("## Base de dados")

#Passo 2: Visualizar a base de dados

planilha = planilha.drop(columns="CustomerID") #retirar coluna CustomerID
st.dataframe(planilha)


#Passo 3: Corrigir os problemas da base de dados (tratamento de dados)
planilha.info() #verificar formato dos valores
planilha = planilha.dropna() #excluir  infos vazias



planilha["cancelou"] = planilha["cancelou"].replace({0: "Não", 1: "Sim"}) # Transformar 0 e 1 em Não e Sim

planilha.info() #verificar resultado

#Passo 4: Analise Inicial (entender quantos clientes cancelaram)

st.write("## Análise geral dos cancelamentos")

st.write(
    """
    Nesta etapa, analisamos a quantidade de clientes que cancelaram o
    serviço e a proporção de cancelamentos em relação ao total da base.
    """
)

st.write("### Quantidade de clientes por situação de cancelamento")

st.write(
    planilha["cancelou"].value_counts()
)

st.write("### Percentual de clientes por situação de cancelamento")

st.write(
    planilha["cancelou"]
    .value_counts(normalize=True)
    .map("{:.2%}".format)
)


# ANÁLISE DOS FATORES ASSOCIADOS AO CANCELAMENTO
# =========================================================

st.write("## Análise dos fatores associados ao cancelamento")

st.write(
    """
    Nesta etapa, analisamos diferentes características dos clientes
    para identificar padrões associados ao cancelamento.
    
    Os gráficos abaixo permitem comparar o comportamento dos clientes
    que cancelaram o serviço com aqueles que permaneceram ativos.
    """
)

#Passo 5: Analise detalhada (causa do cancelamento dos clientes, como cada coluna impacta no cancelamento)

for coluna in planilha.columns:
    grafico = px.histogram(planilha, x=coluna, color="cancelou", text_auto=True)
    st.plotly_chart(grafico)
#Todo mundo do contrato mensal, cancelou o serviço
    #Criar politica: Vamos dar desconto para migração para contrato anual e trimestral

#Ligacoes_callcenter acima de 4 ligações, todo mundo cancelou
    #Tem algum problema que não estamos conseguindo resolver
    #Criar politica: se o cliente ligar 3x para o callcenter, alerta vermelho

#Atraso no pagamento acuma de 20 dias, o cliente cancela
    #Criar politica: se o cliente atrasar 15 dias no pagamento, alerta vermelho

# INSIGHT 1: TIPO DE CONTRATO
st.write("## Insights e recomendações")

st.write("### 1. Tipo de contrato")


# Análise de cada tipo de contrato

contratos = (
    planilha
    .groupby("duracao_contrato")["cancelou"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
)

# Taxa de cancelamento de cada contrato

cancelamento_mensal = contratos.loc["Monthly", "Sim"] * 100
cancelamento_trimestral = contratos.loc["Quarterly", "Sim"] * 100
cancelamento_anual = contratos.loc["Annual", "Sim"] * 100


# Mostrar os resultados

st.write("### Taxa de cancelamento por tipo de contrato")

st.write(f"**Mensal:** {cancelamento_mensal:.2f}%")
st.write(f"**Trimestral:** {cancelamento_trimestral:.2f}%")
st.write(f"**Anual:** {cancelamento_anual:.2f}%")


# Gráfico

dados_contratos = pd.DataFrame({
    "Tipo de contrato": ["Mensal", "Trimestral", "Anual"],
    "Taxa de cancelamento": [
        cancelamento_mensal,
        cancelamento_trimestral,
        cancelamento_anual
    ]
})

grafico_contratos = px.bar(
    dados_contratos,
    x="Tipo de contrato",
    y="Taxa de cancelamento",
    text="Taxa de cancelamento",
    title="Taxa de cancelamento por tipo de contrato"
)

grafico_contratos.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

grafico_contratos.update_layout(
    yaxis_title="Taxa de cancelamento (%)",
    xaxis_title="Tipo de contrato"
)

st.plotly_chart(grafico_contratos)


# Interpretação

st.write("### O que os dados indicam?")

st.write(
    f"Clientes com contrato mensal apresentam uma taxa de cancelamento "
    f"de {cancelamento_mensal:.2f}%, enquanto os contratos trimestrais "
    f"apresentam {cancelamento_trimestral:.2f}% e os contratos anuais "
    f"apresentam {cancelamento_anual:.2f}%."
)

st.write(
    "Os dados permitem comparar diretamente a ocorrência de cancelamentos "
    "entre os diferentes formatos de contrato."
)


# Recomendação

st.write("### Recomendação")

st.write(
    "Avaliar estratégias de incentivo à migração do contrato mensal para "
    "formatos trimestrais ou anuais, considerando as diferenças observadas "
    "nas taxas de cancelamento."
)
