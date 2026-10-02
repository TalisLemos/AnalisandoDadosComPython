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

#Passo 2: Visualizar a base de dados
planilha = planilha.drop(columns="CustomerID") #retirar coluna CustomerID
st.dataframe(planilha)


#Passo 3: Corrigir os problemas da base de dados (tratamento de dados)
planilha.info() #verificar formato dos valores
planilha = planilha.dropna() #excluir  infos vazias



planilha["cancelou"] = planilha["cancelou"].replace({0: "Não", 1: "Sim"}) # Transformar 0 e 1 em Não e Sim

planilha.info() #verificar resultado

#Passo 4: Analise Inicial (entender quantos clientes cancelaram)

st.write(planilha["cancelou"].value_counts()) #contar quantidade de clientes que calcularam

st.write(planilha["cancelou"].value_counts(normalize=True).map("{:.2%}".format)) #calcular porcentagem

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
# =========================================================

st.write("## Insights e recomendações")

st.write("### 1. Tipo de contrato")


# Contratos diferentes do mensal

contratos_nao_mensais = planilha[
    planilha["duracao_contrato"] != "Monthly"
]

resultado_nao_mensais = (
    contratos_nao_mensais["cancelou"]
    .value_counts(normalize=True)
    .map("{:.2%}".format)
)

st.write("**Contratos de maior duração:**")

st.write(resultado_nao_mensais)


# Contratos mensais

contratos_mensais = planilha[
    planilha["duracao_contrato"] == "Monthly"
]

resultado_mensais = (
    contratos_mensais["cancelou"]
    .value_counts(normalize=True)
    .map("{:.2%}".format)
)

st.write("**Contratos mensais:**")

st.write(resultado_mensais)


# Interpretação do resultado

st.write("### O que os dados indicam?")

st.write(
    "Clientes com contrato mensal apresentam uma taxa de cancelamento de "
    "100%, enquanto entre os clientes com contratos de maior duração a taxa "
    "de cancelamento é de 46,14%."
)

st.write(
    "Esse resultado indica uma forte associação entre contratos mensais "
    "e maior ocorrência de cancelamentos."
)


# Recomendação

st.write("### Recomendação")

st.write(
    "Criar estratégias para incentivar clientes com contrato mensal a "
    "migrarem para contratos de maior duração, como contratos trimestrais "
    "ou anuais."
)
