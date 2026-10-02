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

nomes_colunas = {
    "idade": "Cancelamentos por idade",
    "sexo": "Cancelamentos por sexo",
    "tempo_como_cliente": "Cancelamentos por tempo como cliente",
    "frequencia_uso": "Cancelamentos por frequência de uso",
    "ligacoes_callcenter": "Cancelamentos por número de ligações ao call center",
    "dias_atraso": "Cancelamentos por dias de atraso no pagamento",
    "assinatura": "Cancelamentos por tipo de assinatura",
    "duracao_contrato": "Cancelamentos por duração do contrato",
    "total_gasto": "Cancelamentos por total gasto",
    "meses_ultima_interacao": "Cancelamentos por meses desde a última interação"
}

for coluna in nomes_colunas:
    grafico = px.histogram(
        planilha,
        x=coluna,
        color="cancelou",
        text_auto=True,
        title=nomes_colunas[coluna]
    )

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


# Recomendação

st.write("### Recomendação")

st.write(
    "Avaliar estratégias de incentivo à migração do contrato mensal para "
    "formatos trimestrais ou anuais, considerando as diferenças observadas "
    "nas taxas de cancelamento."
)


# INSIGHT 2: DIAS DE ATRASO NO PAGAMENTO
# =========================================================

st.write("### 2. Dias de atraso no pagamento")

# Agrupar clientes por faixa de atraso

planilha["faixa_atraso"] = planilha["dias_atraso"].apply(
    lambda x: "Até 20 dias" if x <= 20 else "21 dias ou mais"
)

atrasos = (
    planilha
    .groupby("faixa_atraso")["cancelou"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
)

cancelamento_ate_20 = atrasos.loc["Até 20 dias", "Sim"] * 100
cancelamento_21_mais = atrasos.loc["21 dias ou mais", "Sim"] * 100

dados_atrasos = pd.DataFrame({
    "Faixa de atraso": ["Até 20 dias", "21 dias ou mais"],
    "Taxa de cancelamento": [
        cancelamento_ate_20,
        cancelamento_21_mais
    ]
})

grafico_atrasos = px.bar(
    dados_atrasos,
    x="Faixa de atraso",
    y="Taxa de cancelamento",
    text="Taxa de cancelamento",
    title="Taxa de cancelamento por faixa de atraso no pagamento"
)

grafico_atrasos.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

grafico_atrasos.update_layout(
    yaxis_title="Taxa de cancelamento (%)",
    xaxis_title="Faixa de atraso"
)

st.plotly_chart(grafico_atrasos)

st.write("### Recomendação")

st.write(
    "Criar ações preventivas de cobrança e relacionamento antes que o cliente "
    "atinja 21 dias de atraso, priorizando lembretes de pagamento, contatos "
    "proativos e alternativas para regularização da situação."
)
