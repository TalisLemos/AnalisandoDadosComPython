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

planilha = pd.read_csv("cancelamentos.csv")

#Passo 2: Visualizar a base de dados
planilha = planilha.drop(columns="CustomerID") #retirar coluna CustomerID
display(planilha)

#Passo 3: Corrigir os problemas da base de dados (tratamento de dados)
display(planilha.info()) #verificar formato dos valores
planilha = planilha.dropna() #excluir  infos vazias



planilha["cancelou"] = planilha["cancelou"].replace({0: "Não", 1: "Sim"}) # Transformar 0 e 1 em Não e Sim

display(planilha.info()) #verificar resultado

#Passo 4: Analise Inicial (entender quantos clientes cancelaram)

display(planilha["cancelou"].value_counts()) #contar quantidade de clientes que calcularam

display(planilha["cancelou"].value_counts(normalize=True).map("{:.2%}".format)) #calcular porcentagem

#Passo 5: Analise detalhada (causa do cancelamento dos clientes, como cada coluna impacta no cancelamento)

import plotly.express as px

for coluna in planilha.columns:
    grafico = px.histogram(planilha, x=coluna, color="cancelou", text_auto=True)
    grafico.show()

#Todo mundo do contrato mensal, cancelou o serviço
    #Criar politica: Vamos dar desconto para migração para contrato anual e trimestral

#Ligacoes_callcenter acima de 4 ligações, todo mundo cancelou
    #Tem algum problema que não estamos conseguindo resolver
    #Criar politica: se o cliente ligar 3x para o callcenter, alerta vermelho

#Atraso no pagamento acuma de 20 dias, o cliente cancela
    #Criar politica: se o cliente atrasar 15 dias no pagamento, alerta vermelho

#Fitrar a base de dados
#duracao_contrato -> diferente de monthly

condicao1 = planilha["duracao_contrato"] != "Monthly"
planilha = planilha[condicao1]
display(planilha["cancelou"].value_counts(normalize=True).map("{:.2%}".format)) #calcular porcentagem

#ligacao_callcenter -> menos ou iguais a 4
condicao2 = planilha["ligacoes_callcenter"] <= 4
planilha = planilha[condicao2]
display(planilha["cancelou"].value_counts(normalize=True).map("{:.2%}".format)) #calcular porcentagem

#dias_atraso -> menores ou iguais a 20
condicao3 = planilha["dias_atraso"] <= 20
planilha = planilha[condicao3]
display(planilha["cancelou"].value_counts(normalize=True).map("{:.2%}".format)) #calcular porcentagem
