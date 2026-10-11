#Passo a passo do projeto
#Passo 1: Abrir a base de dados (importar)
    #import pandas, streamlit e plotly.express
    #pd.read_csv("cancelamentos.csv")
#Passo 2: Visualizar a base de dados
    #Entender as informacoes disponiveis (colunas, tipos, valores)
    #Possiveis problemas: linhas repetidas, valores vazios, coluna que nao ajuda (CustomerID)
#Passo 3: Corrigir os problemas da base de dados (tratamento de dados)
    #Remover linhas duplicadas (.drop_duplicates())
    #Remover informacoes vazias (.dropna())
    #Transformar cancelou de 0 e 1 em Nao e Sim (para os graficos)
    #Guardar quantas linhas foram removidas, para citar no final da pagina
#Passo 4: Abertura da pagina (apresentar o case)
    #Titulo com a pergunta do projeto (st.title)
    #Quem fez (st.markdown)
    #Sanfonas com st.expander: Sobre o case / Objetivo / Como ler a pagina / Resumo
#Passo 5: O problema (entender quantos clientes cancelaram)
    #Total de clientes, % que cancelou, quantos seguem ativos
    #Mostrar com st.metric
    #Frase de ligacao para a proxima parte
#Passo 6: Quem esta indo embora (perfil)
    #Achado 1: taxa de cancelamento por tipo de contrato
    #Achado 2: taxa de cancelamento por faixa de idade (ate 50 anos x 51 ou mais)
    #Em cada um: calcular com groupby + mean, grafico de barras (px.bar) e uma frase com o resultado
#Passo 7: O que acontece antes da saida (comportamento)
    #Achado 3: taxa de cancelamento por numero de ligacoes ao call center
    #Achado 4: taxa de cancelamento por dias de atraso (faixas de 5 dias)
    #Em cada um: groupby + mean, grafico de linha (px.line) e uma frase com o resultado
    #Fechar o diagnostico em 3 ou 4 frases (so constatacoes, sem solucao ainda)
#Passo 8: A proposta (agir antes de o cliente sair)
    #Frente 1: evitar o contrato mensal na venda
    #Frente 2: cuidar do publico de 51 anos ou mais
    #Frente 3: regua de alerta (ligacoes e atraso)
    #Tabela com gatilho, acao, quem executa, canal e metrica de sucesso
    #Como medir o resultado (grupo de controle, 90 dias)
#Passo 9: Simulador da regua (opcional, so depois que o resto estiver pronto)
    #Dois controles com st.slider: ligacoes e dias de atraso
    #Filtrar os clientes que batem na regra e contar quantos sao
    #Mostrar com st.metric
#Passo 10: Conclusao e proximos passos
    #Resumir em 3 frases + 3 proximos passos
#Passo 11: Sobre a analise (rodape)
    #Quantas linhas foram removidas, limitacoes, ferramentas, data da atualizacao


#Passo a passo do projeto
#Passo 1: Abrir a base de dados (importar)
    #import pandas, streamlit e plotly.express
import pandas as pd
import streamlit as st
import plotly.express as px

    #pd.read_csv("cancelamentos.csv")
planilha = pd
#Passo 2: Visualizar a base de dados
    #Entender as informacoes disponiveis (colunas, tipos, valores)
    #Possiveis problemas: linhas repetidas, valores vazios, coluna que nao ajuda (CustomerID)
#Passo 3: Corrigir os problemas da base de dados (tratamento de dados)
    #Remover linhas duplicadas (.drop_duplicates())
    #Remover informacoes vazias (.dropna())
    #Transformar cancelou de 0 e 1 em Nao e Sim (para os graficos)
    #Guardar quantas linhas foram removidas, para citar no final da pagina
#Passo 4: Abertura da pagina (apresentar o case)
    #Titulo com a pergunta do projeto (st.title)
    #Quem fez (st.markdown)
    #Sanfonas com st.expander: Sobre o case / Objetivo / Como ler a pagina / Resumo
#Passo 5: O problema (entender quantos clientes cancelaram)
    #Total de clientes, % que cancelou, quantos seguem ativos
    #Mostrar com st.metric
    #Frase de ligacao para a proxima parte
#Passo 6: Quem esta indo embora (perfil)
    #Achado 1: taxa de cancelamento por tipo de contrato
    #Achado 2: taxa de cancelamento por faixa de idade (ate 50 anos x 51 ou mais)
    #Em cada um: calcular com groupby + mean, grafico de barras (px.bar) e uma frase com o resultado
#Passo 7: O que acontece antes da saida (comportamento)
    #Achado 3: taxa de cancelamento por numero de ligacoes ao call center
    #Achado 4: taxa de cancelamento por dias de atraso (faixas de 5 dias)
    #Em cada um: groupby + mean, grafico de linha (px.line) e uma frase com o resultado
    #Fechar o diagnostico em 3 ou 4 frases (so constatacoes, sem solucao ainda)
#Passo 8: A proposta (agir antes de o cliente sair)
    #Frente 1: evitar o contrato mensal na venda
    #Frente 2: cuidar do publico de 51 anos ou mais
    #Frente 3: regua de alerta (ligacoes e atraso)
    #Tabela com gatilho, acao, quem executa, canal e metrica de sucesso
    #Como medir o resultado (grupo de controle, 90 dias)
#Passo 9: Simulador da regua (opcional, so depois que o resto estiver pronto)
    #Dois controles com st.slider: ligacoes e dias de atraso
    #Filtrar os clientes que batem na regra e contar quantos sao
    #Mostrar com st.metric
#Passo 10: Conclusao e proximos passos
    #Resumir em 3 frases + 3 proximos passos
#Passo 11: Sobre a analise (rodape)
