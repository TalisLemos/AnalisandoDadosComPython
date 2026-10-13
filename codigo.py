#Passo a passo do projeto
#Passo 1: Abrir a base de dados (importar)
#Passo 2: Visualizar a base de dados
#Passo 3: Corrigir os problemas da base de dados (tratamento de dados)
#Passo 4: Abertura da pagina (apresentar o case)
#Passo 5: O problema (entender quantos clientes cancelaram)
#Passo 6: Quem esta indo embora (perfil)
#Passo 7: O que acontece antes da saida (comportamento)
#Passo 8: A proposta (agir antes de o cliente sair)
#Passo 9: Simulador da regua (opcional, so depois que o resto estiver pronto)
#Passo 10: Conclusao e proximos passos
#Passo 11: Sobre a analise (rodape)

########################################33333

#Passo a passo do projeto
#Passo 1: Abrir a base de dados (importar)
    #import pandas, streamlit e plotly.express
import pandas as pd
import streamlit as st
import plotly.express as px

    #pd.read_csv("cancelamentos.csv")
planilha = pd.read_csv("cancelamentos.csv")

st.set_page_config(page_title= "Análise de churn", layout="wide") #Configuração da pagina // nome e largura


st.info(
    "**Projeto em desenvolvimento**\n\n"
    "Este projeto está disponível para consulta como parte do meu portfólio, "
    "embora ainda não esteja na versão final. As análises e visualizações "
    "estão sendo aprimoradas, e as recomendações serão incluídas após "
    "a conclusão e validação do diagnóstico."
)


planilha["duracao_contrato"] = planilha["duracao_contrato"].replace({
    "Monthly": "Mensal",
    "Quarterly": "Trimestral",
    "Annual": "Anual"
})

planilha["sexo"] = planilha["sexo"].replace({
    "Female": "Feminino",
    "Male": "Masculino"
})



#Passo 2: Visualizar a base de dados


#Passo 3: Corrigir os problemas da base de dados (tratamento de dados)
    #Remover linhas duplicadas (.drop_duplicates())
    #Remover informacoes vazias (.dropna())

linhas_original = len(planilha) #Guardar quantas linhas a base tinha no inicio

duplicados = planilha["CustomerID"].duplicated().sum() #Verificar quantos clientes aparecem repetidos (pelo ID)
print(duplicados)

planilha = planilha.drop_duplicates(subset="CustomerID", keep="first") #Remover os repetidos, mantendo a primeira ocorrencia de cada ID

linhas_antes_vazios = len(planilha) #Remover as informacoes vazias e guardar quantas foram
planilha = planilha.dropna()
vazios = linhas_antes_vazios - len(planilha)


planilha = planilha.drop(columns="CustomerID") #retirar a coluna que nao ajuda na analise

#3.6 Conferir o resultado
print(linhas_original, duplicados, vazios, len(planilha))

    #Transformar cancelou de 0 e 1 em Nao e Sim (para os graficos)
planilha["cancelou"] = planilha["cancelou"].replace({0: "Não", 1: "Sim"}) # Transformar 0 e 1 em Não e Sim

planilha["situacao"] = planilha["cancelou"].map({"Sim": "Cancelou", "Não": "Não cancelou"}) #Coluna com nomes mais claros para os graficos

planilha.info() #verificar resultado

#Passo 4: Abertura da pagina (apresentar o case)
    #Titulo com a pergunta do projeto (st.title)
    #Quem fez (st.markdown)
    #Sanfonas com st.expander: Sobre o case / Objetivo / Como ler a pagina / Resumo


st.title("Por que os clientes cancelaram? Daria para ter agido antes?")

st.caption("Análise de churn · Case de dados com Python ·  CRM e retenção")
st.markdown("Por **Talita Lemos** · Publicitária há mais de 10 anos com experiência em CRM, growth e automação · [Linkedin](https://www.linkedin.com/in/talitalemos)" )


with st.expander("Sobre o case"):
    st.write('''Uma empresa de serviços por assinatura tem 48.527 clientes na base, e 56,7% deles já cancelaram. 
    Este case analisa os dados para entender o que está por trás dos cancelamentos e propor ações de retenção. 
    Os dados têm finalidade didática: os padrões são mais extremos do que numa operação real, e servem para ilustrar o método de análise.
''')

with st.expander("Objetivo"):
    st.write('''Identificar os principais fatores relacionados ao cancelamento, analisando características, 
    perfil e comportamento dos clientes. A partir desses insights, propor ações de retenção que possam contribuir 
    para reduzir a taxa de churn.''')

with st.expander("Como ler esta página"):
    st.write('''A leitura leva cerca de 4 minutos. Taxa de cancelamento é a % de clientes de um grupo que cancelaram 
    até a data da base. Como a base não tem datas, a análise mostra associações, não a evolução no tempo.
''')


with st.expander("Só quer o resumo? Conclusões em poucas linhas"):
    st.markdown(
    "(em breve)")

#Passo 5: O problema (entender quantos clientes cancelaram)
    #Total de clientes, % que cancelou, quantos seguem ativos

total_clientes = len(planilha) #Total de clientes (numero de linhas da base)


cancelaram = (planilha["cancelou"] == "Sim").sum() #Quantos cancelaram (contar as linhas onde cancelou e "Sim")

ativos = (planilha["cancelou"] == "Não").sum() #Quantos seguem ativos (contar as linhas onde cancelou e "Nao")

percentual_cancelou = cancelaram / total_clientes * 100 #% que cancelou

percentual_gasto_cancelados = (planilha.loc[planilha['cancelou'] == "Sim", 'total_gasto'].sum() / planilha['total_gasto'].sum()) * 100

st.markdown(
    "<div style='margin-top: 70px;'></div>", #Espaçamento do inicio da sessão
    unsafe_allow_html=True
)

st.header("1. O problema: Mais da metade da base de clientes já cancelou")


st.markdown(
    f"Imagine uma empresa de serviço por assinatura com **{f"{total_clientes:,.0f}".replace(",", ".")} clientes**."
    " Ao olhar a base, o time percebe algo preocupante: "
    f"**{percentual_cancelou:.1f}% deles já cancelou.**  \n"
    "Esses clientes representam quase metade de tudo o que a base já gastou."
)

coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns(5) #Mostrar na pagina, com colunas lado a lado
coluna1.metric("Clientes na base", f"{total_clientes:,}".replace(",", "."))
coluna2.metric("Já cancelaram", f"{percentual_cancelou:.1f}%")
coluna3.metric("Seguem ativos", f"{ativos:,}".replace(",", "."))
coluna4.metric("% do gasto total dos cancelados:", f"{percentual_gasto_cancelados:.2f}%".replace(".", ","))

grafico_rosca = px.pie(planilha, names="situacao", hole=0.6, color="situacao", color_discrete_map={"Cancelou": "#E4572E", "Não cancelou": "#2E86AB"}) #Grafico de rosca na quarta coluna
grafico_rosca.update_traces(
    textinfo="none", #Tirar os textos de cima das fatias
    hovertemplate="%{label}: %{value} clientes (%{percent})<extra></extra>"
)

grafico_rosca.update_layout(
    height=150,
    margin=dict(l=0, r=0, t=0, b=0),
    annotations=[dict(text=f"{percentual_cancelou:.0f}%", x=0.5, y=0.5,
                      font_size=26, showarrow=False)],
)
coluna5.plotly_chart(grafico_rosca,use_container_width=True)

st.markdown(
    '''>  Antes de pensar em soluções, vale entender **qual é o perfil de quem esta indo embora**.'''
)

#Passo 6: Quem esta indo embora (perfil)
    #Achado 1: taxa de cancelamento por tipo de contrato
    #Achado 2: taxa de cancelamento por faixa de idade (18-30, 31-40, 41-50, 51 ou mais)
    #Achado 3: taxa de cancelamento por sexo

st.markdown(
    "<div style='margin-top: 70px;'></div>", #Espaçamento do inicio da sessão
    unsafe_allow_html=True
)

st.header("2. O perfil: Quem esta saindo?")

st.markdown(
    "Para identificar quais perfis apresentam maior propensão ao cancelamento, cruzei três variáveis: **faixa etária**, **sexo** e **tipo de contrato**.")



planilha["faixa_idade"] = pd.cut(planilha["idade"], bins=[17, 30, 40, 50, float("inf")], #Criar faixas de idade
                                 labels=["18 a 30", "31 a 40", "41 a 50", "51 ou mais"])



#6.5 Sexo dentro de cada faixa de idade
taxa_sexo_idade = (
    planilha.groupby(["faixa_idade", "sexo"], observed=True)
    .agg(
        total=("cancelou", "size"),
        cancelados=("cancelou", lambda x: (x == "Sim").sum())
    )
    .reset_index()
)

taxa_sexo_idade["taxa"] = (
    taxa_sexo_idade["cancelados"] / taxa_sexo_idade["total"] * 100
)

taxa_sexo_idade["resultado"] = (
    taxa_sexo_idade["taxa"].round(0).astype(int).astype(str)
    + "% ("
    + taxa_sexo_idade["cancelados"].astype(str)
    + ")"
)

grafico_sexo_idade = px.bar(
    taxa_sexo_idade,
    x="faixa_idade",
    y="taxa",
    title="% de cancelamento por Idade e Sexo",
    color="sexo",
    barmode="group",
    text=taxa_sexo_idade["taxa"].round(0).astype(int).astype(str) + "%",
    color_discrete_map={
    "Feminino": "#E4572E",
    "Masculino": "#2E86AB"
    },
    hover_data={
        "cancelados": True,
        "total": True,
        "taxa": False
    },
    labels={
        "faixa_idade": "Faixa de idade",
        "taxa": "% que cancelou",
        "sexo": "Sexo",
        "cancelados": "Clientes que cancelaram",
        "total": "Total de clientes"
    }
)

grafico_sexo_idade.update_layout(yaxis_range=[0, 110], height=300,)


taxa_contrato = (
    planilha.groupby("duracao_contrato", observed=True)
    .agg(
        total=("cancelou", "size"),
        cancelados=("cancelou", lambda x: (x == "Sim").sum())
    )
    .reset_index()
)

taxa_contrato["taxa"] = (
    taxa_contrato["cancelados"] / taxa_contrato["total"] * 100
)


grafico_contrato = px.bar(
    taxa_contrato,
    x="duracao_contrato",
    y="taxa",
    title="% de clientes que cancelaram por Tipo de Contrato",
    text=taxa_contrato["taxa"].round(0).astype(int).astype(str) + "%",
    color_discrete_sequence=["#2E86AB"],
    hover_data={
        "cancelados": True,
        "total": True,
        "taxa": False
    },
    category_orders={
        "duracao_contrato": ["Mensal", "Trimestral", "Anual"]
    },
    labels={
        "duracao_contrato": "Tipo de contrato",
        "taxa": "% que cancelou",
        "cancelados": "Clientes que cancelaram",
        "total": "Total de clientes"
    }
)

grafico_contrato.update_layout(yaxis_range=[0, 110], height=300)


col_sexo_idade, col_contrato = st.columns(2)

with col_sexo_idade:
    st.plotly_chart(grafico_sexo_idade, use_container_width=True)
    st.markdown(">**Clientes com 51 anos ou mais apresentam taxa de cancelamento de 100%**, " \
    "independentemente do sexo. Nas demais faixas etárias, as taxas variam entre homens e mulheres. Na base geral, " \
    "a taxa de cancelamento é de 67,06% entre mulheres e 48,82% entre homens, uma diferença de 18,24 pontos percentuais." \
    " ***A análise por sexo é exclusivamente analítica e não deve orientar tratamentos diferenciados entre clientes.***")

with col_contrato:
    st.plotly_chart(grafico_contrato, use_container_width=True)
    st.markdown(">**A taxa de cancelamento é de 100% entre clientes com contrato mensal**. " \
    "A diferença observada é expressiva, enquanto as taxas dos contratos trimestrais e anuais são próximas (46%)." \
    "Esses resultados descrevem o comportamento da base analisada, mas não permitem concluir que o tipo de contrato seja a causa dos cancelamentos.")

st.markdown(
    "<div style='margin-top: 50px;'></div>",
    unsafe_allow_html=True
)

st.markdown(
    "No mapa de calor, quanto mais vermelha a célula, maior a taxa de cancelamento.")

taxa_sexo_idade_contrato = (
    planilha.groupby(
        ["faixa_idade", "sexo", "duracao_contrato"],
        observed=True
    )["cancelou"]
    .agg(
        clientes="count",
        cancelaram=lambda x: (x == "Sim").sum(),
        taxa=lambda x: (x == "Sim").mean() * 100
    )
    .reset_index()
)


fig = px.density_heatmap(
    taxa_sexo_idade_contrato,
    x="duracao_contrato",
    y="faixa_idade",
    z="taxa",
    facet_col="sexo",
    histfunc="avg",
    color_continuous_scale="RdYlBu_r",
    range_color=[0, 100],
    text_auto=".0f",
    labels={
        "duracao_contrato": "Tipo de contrato",
        "faixa_idade": "Faixa etária",
        "taxa": "Cancelamento (%)",
        "sexo": "Sexo"},
    category_orders={
        "duracao_contrato": ["Mensal", "Trimestral", "Anual"],
        "faixa_idade": ["51 ou mais", "41 a 50", "31 a 40", "18 a 30"],
        "sexo": ["Feminino", "Masculino"]}
)

fig.update_layout(
    coloraxis_colorbar_title="Cancelamento (%)",
    height=300, #Altura do grafico
    margin=dict(t=15, b=10) #Espaçamento interno e externo do grafico
)

st.plotly_chart(fig, use_container_width=True)



st.markdown('''
    > O cancelamento chega a 100% entre clientes com 51 anos ou mais, independentemente do sexo e do tipo de contrato. Entre clientes de 18 a 50 anos, essa mesma taxa é observada nos contratos mensais. Na análise geral por sexo, as mulheres apresentam uma taxa de cancelamento superior à dos homens.

> Esses padrões evidenciam diferenças entre os grupos analisados, mas não permitem determinar, isoladamente, as causas dos cancelamentos. Para aprofundar o diagnóstico, **o próximo passo é investigar o comportamento dos clientes e identificar outras características associadas à saída.**
''')



#Passo 7: O que acontece antes da saida (comportamento)
    #Achado 3: taxa de cancelamento por numero de ligacoes ao call center
    #Achado 4: taxa de cancelamento por dias de atraso (faixas de 5 dias)
    #Em cada um: groupby + mean, grafico de linha (px.line) e uma frase com o resultado
    #Fechar o diagnostico em 3 ou 4 frases (so constatacoes, sem solucao ainda)

#Calculos: taxa de cancelamento por numero de ligacoes e por dias de atraso
taxa_ligacoes = (planilha.groupby("ligacoes_callcenter")["cancelou"]
                 .agg(clientes="count",
                      cancelaram=lambda x: (x == "Sim").sum(),
                      taxa=lambda x: (x == "Sim").mean() * 100)
                 .reset_index())

taxa_atraso = (planilha.groupby("dias_atraso")["cancelou"]
               .agg(clientes="count",
                    cancelaram=lambda x: (x == "Sim").sum(),
                    taxa=lambda x: (x == "Sim").mean() * 100)
               .reset_index())

#Grafico de linha: ligacoes ao call center
grafico_ligacoes = px.line(
    taxa_ligacoes, x="ligacoes_callcenter", y="taxa", markers=True,
    hover_data={"clientes": True, "cancelaram": True, "taxa": ":.1f"},
    title="Ligações ao call center",
    labels={"ligacoes_callcenter": "Número de ligações", "taxa": "% que cancelou",
            "clientes": "Clientes", "cancelaram": "Cancelaram"},
)
grafico_ligacoes.update_traces(line_color="#E4572E")
grafico_ligacoes.add_vline(x=6, line_dash="dash", line_color="gray",
                           annotation_text="100% cancelam", annotation_position="top left")
grafico_ligacoes.add_vrect(x0=3, x1=5, fillcolor="lightgray",
    opacity=0.3,
    line_width=0,
    annotation_text="zona de atenção",
    annotation_position="bottom"
)
grafico_ligacoes.update_layout(yaxis_range=[0, 110], height=340)

#Grafico de linha: dias de atraso
grafico_atraso = px.line(
    taxa_atraso, x="dias_atraso", y="taxa", markers=True,
    hover_data={"clientes": True, "cancelaram": True, "taxa": ":.1f"},
    title="Atraso no pagamento",
    labels={"dias_atraso": "Dias de atraso", "taxa": "% que cancelou",
            "clientes": "Clientes", "cancelaram": "Cancelaram"},
)
grafico_atraso.update_traces(line_color="#E4572E")
grafico_atraso.add_vline(x=21, line_dash="dash", line_color="gray",
                         annotation_text="21 dias: 100% cancelam", annotation_position="top left")
grafico_atraso.add_vrect(
    x0=15,
    x1=20,
    fillcolor="lightgray",
    opacity=0.3,
    line_width=0,
    annotation_text="janela de ação",
    annotation_position="bottom"
)
grafico_atraso.update_layout(yaxis_range=[0, 110], height=340)


st.markdown(
    "<div style='margin-top: 70px;'></div>", #Espaçamento do inicio da sessão
    unsafe_allow_html=True
)

st.header("3. Comportamento: O que acontece antes da saida?")

st.write(
    '''Olhei dois comportamentos que a empresa já registra: quantas vezes o cliente liga para o call center 
    e quantos dias ele atrasa o pagamento. Cada ponto do gráfico é um grupo de clientes com aquele nível 
    de ligações ou de atraso, e mostra a % deles que cancelou.''')


planilha["grupo_ligacoes"] = planilha["ligacoes_callcenter"].apply(
    lambda x: "Até 3 ligações" if x <= 3 else "4 ligações ou mais"
)

taxa_ligacoes = (
    planilha.groupby("grupo_ligacoes", observed=True)["cancelou"]
    .agg(
        total_clientes="count",
        cancelamentos=lambda x: (x == "Sim").sum(),
        taxa_cancelamento=lambda x: (x == "Sim").mean() * 100
    )
    .reset_index()
)

ordem = ["Até 3 ligações", "4 ligações ou mais"]

col_lig, col_atr = st.columns(2)

with col_lig:
    st.plotly_chart(grafico_ligacoes, use_container_width=True)
    st.write("O cancelamento sobe depressa a partir da 3ª ligação")
    st.write(">Com até 2 ligações, cerca de 30% cancelam.  \nA taxa sobe para 41% com 3 ligações, 59% com 4 e 94% com 5.  \nA partir de **6 ligações**, todos cancelaram.")

with col_atr:
    st.plotly_chart(grafico_atraso, use_container_width=True)
    st.write("O risco não sobe aos poucos: ele salta no dia 21")
    st.write(">Até 20 dias de atraso, a taxa de cancelamento fica em torno de 46% (igual à de quem não atrasa). No dia 21, passa a 100%. Os dias anteriores são uma janela para agir, não um sinal de risco maior.")


st.write("Esses dados mostram associação: a base não tem datas, então não dá para provar que as ligações e os atrasos vieram antes da decisão de cancelar. Essa é a hipótese que a proposta precisa validar.")

#Fechando o diagnostico

taxa_idade = planilha.groupby("faixa_idade")["cancelou"].apply(lambda x: (x == "Sim").mean() * 100) # Taxa de cancelamento por faixa de idade


#Calculos (os numeros que entram nas frases)
taxa_contrato = planilha.groupby("duracao_contrato")["cancelou"].apply(lambda x: (x == "Sim").mean() * 100)
taxa_mensal = taxa_contrato["Mensal"]
taxa_anual = taxa_contrato["Anual"]

taxa_51 = taxa_idade["51 ou mais"]

st.markdown(
    "<div style='margin-top: 70px;'></div>", #Espaçamento do inicio da sessão
    unsafe_allow_html=True
)
