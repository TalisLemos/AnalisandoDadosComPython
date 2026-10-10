import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Churn: sinais que antecipam o cancelamento", layout="wide",
                   initial_sidebar_state="collapsed")

# =========================================================
# CONFIGURAÇÃO (ajuste aqui os cortes e as políticas)
# =========================================================
LIMITE_LIGACOES = 4    # a partir daqui o cancelamento dispara
LIMITE_ATRASO = 21     # dias de atraso em que o cancelamento dispara
LIMITE_IDADE = 51      # idade a partir da qual o cancelamento dispara

ALERTA_LIGACOES = 3    # gatilho de alerta (antes do corte)
ALERTA_ATRASO = 15     # gatilho de alerta (antes do corte)

MOSTRAR_ORIGEM = True  # linha "origem do projeto" no rodapé

AUTORA = "Talita Lemos"
APRESENTACAO_AUTORA = "Publicitária com mais de 10 anos de experiência em CRM, growth e experiência do cliente"
LINKEDIN_URL = "www.linkedin.com/in/talitalemos"

MAPA_CONTRATO = {"Monthly": "Mensal", "Quarterly": "Trimestral", "Annual": "Anual"}
ORDEM_CONTRATO = ["Mensal", "Trimestral", "Anual"]
NOMES_QUARTIS = ["1º quartil (menor gasto)", "2º quartil", "3º quartil",
                 "4º quartil (maior gasto)"]

COR_RISCO = "#E4572E"
COR_OK = "#2E86AB"
CORES = {"Ficou": COR_OK, "Cancelou": COR_RISCO}

ROT_IDADE_BAIXO = f"Até {LIMITE_IDADE - 1} anos"
ROT_IDADE_ALTO = f"{LIMITE_IDADE} anos ou mais"

NOMES_COLUNAS = {
    "idade": "Idade",
    "sexo": "Sexo",
    "tempo_como_cliente": "Tempo como cliente",
    "frequencia_uso": "Frequência de uso",
    "ligacoes_callcenter": "Ligações ao call center",
    "dias_atraso": "Dias de atraso no pagamento",
    "assinatura": "Tipo de assinatura",
    "duracao_contrato": "Duração do contrato",
    "total_gasto": "Total gasto",
    "meses_ultima_interacao": "Meses desde a última interação",
}


# =========================================================
# FUNÇÕES
# =========================================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("cancelamentos.csv")
    antes = len(df)
    df = df.dropna().copy()
    removidos = antes - len(df)

    df["cancelou"] = df["cancelou"].astype(int)  # 0/1 para calcular taxas
    df["situacao"] = df["cancelou"].map({0: "Ficou", 1: "Cancelou"})
    df["contrato"] = df["duracao_contrato"].map(MAPA_CONTRATO).fillna(df["duracao_contrato"])
    df["faixa_idade"] = df["idade"].apply(
        lambda x: ROT_IDADE_BAIXO if x < LIMITE_IDADE else ROT_IDADE_ALTO
    )

    # Quartis (o rank evita erro quando há muitos valores repetidos)
    df["faixa_gasto"] = pd.qcut(
        df["total_gasto"].rank(method="first"), q=4, labels=NOMES_QUARTIS
    )
    # Gasto médio por período como cliente: separa "gasta pouco" de "é cliente novo"
    df["gasto_medio"] = df["total_gasto"] / df["tempo_como_cliente"].clip(lower=1)
    df["faixa_gasto_medio"] = pd.qcut(
        df["gasto_medio"].rank(method="first"), q=4, labels=NOMES_QUARTIS
    )
    return df, removidos


def fmt_int(n):
    return f"{int(n):,}".replace(",", ".")


def pct(x):
    return "n/d" if pd.isna(x) else f"{x:.1f}%"


def taxa_por_grupo(df, coluna):
    """Taxa de cancelamento, volume e peso de cada grupo no total de saídas."""
    tabela = (
        df.groupby(coluna, observed=True)["cancelou"]
        .agg(clientes="count", cancelados="sum", taxa="mean")
        .reset_index()
    )
    tabela["taxa"] = tabela["taxa"] * 100
    tabela["peso_no_churn"] = tabela["cancelados"] / df["cancelou"].sum() * 100
    return tabela


def valor(tabela, coluna, grupo, campo="taxa"):
    linha = tabela.loc[tabela[coluna] == grupo, campo]
    return float(linha.iloc[0]) if len(linha) else float("nan")


def tabela_segmentos(df):
    """Segmentos de risco (contrato, idade, gasto médio) numa tabela única."""
    partes = []
    for grupo, coluna in [("Contrato", "contrato"), ("Idade", "faixa_idade"),
                          ("Gasto médio", "faixa_gasto_medio")]:
        t = taxa_por_grupo(df, coluna)
        t["segmento"] = grupo + ": " + t[coluna].astype(str)
        t["grupo"] = grupo
        partes.append(t[["grupo", "segmento", "clientes", "cancelados",
                         "taxa", "peso_no_churn"]])
    return pd.concat(partes, ignore_index=True)


def grafico_linha(tabela, x, rotulo_x, marcas):
    fig = px.line(
        tabela, x=x, y="taxa", markers=True,
        hover_data={"clientes": True, "cancelados": True, "taxa": ":.1f"},
    )
    fig.update_traces(line_color=COR_RISCO, marker_color=COR_RISCO)
    for pos, texto, cor, lado in marcas:
        fig.add_vline(x=pos, line_dash="dash", line_color=cor,
                      annotation_text=texto, annotation_position=lado)
    fig.update_layout(
        xaxis_title=rotulo_x, yaxis_title="Taxa de cancelamento (%)",
        yaxis_range=[0, 108], height=340, margin=dict(t=30, b=10),
    )
    return fig


def regra_alerta(df, lim_lig, lim_atr):
    return (df["ligacoes_callcenter"] >= lim_lig) | (df["dias_atraso"] >= lim_atr)


# =========================================================
# DADOS E FILTROS
# =========================================================
df, removidos = carregar_dados()

st.sidebar.header("Filtrar por perfil")
st.sidebar.caption(
    "Opcional. Quer ver a análise de um grupo específico de clientes "
    "(por exemplo, só contratos mensais)? Escolha aqui e a página inteira "
    "se atualiza. Sem filtros, você vê a base completa."
)
opcoes_contrato = sorted(
    df["contrato"].unique(),
    key=lambda c: ORDEM_CONTRATO.index(c) if c in ORDEM_CONTRATO else 99,
)
f_contrato = st.sidebar.multiselect("Tipo de contrato", opcoes_contrato,
                                    default=opcoes_contrato)
opcoes_sexo = sorted(df["sexo"].unique())
f_sexo = st.sidebar.multiselect("Sexo", opcoes_sexo, default=opcoes_sexo)
idade_min, idade_max = int(df["idade"].min()), int(df["idade"].max())
f_idade = st.sidebar.slider("Idade", idade_min, idade_max, (idade_min, idade_max))

dff = df[
    df["contrato"].isin(f_contrato)
    & df["sexo"].isin(f_sexo)
    & df["idade"].between(f_idade[0], f_idade[1])
]

if dff.empty:
    st.warning("Nenhum cliente com esses filtros. Ajuste a barra lateral.")
    st.stop()
if dff["cancelou"].sum() == 0:
    st.info("Não há cancelamentos neste recorte. Ajuste os filtros na barra lateral.")
    st.stop()

if len(dff) < len(df):
    st.sidebar.success(f"Mostrando {fmt_int(len(dff))} de {fmt_int(len(df))} clientes")

total = len(dff)
cancelados = int(dff["cancelou"].sum())
taxa_geral = cancelados / total * 100
ativos = dff[dff["cancelou"] == 0]
em_alerta_padrao = int(
    (regra_alerta(ativos, ALERTA_LIGACOES, ALERTA_ATRASO)).sum()
)

# =========================================================
# TOPO: RESUMO EM 30 SEGUNDOS
# =========================================================
st.title("Dá para antecipar o cancelamento: 3 sinais concentram a saída de clientes")
st.caption("Análise de churn com Python · Case de CRM e retenção")

autoria = f"Por **{AUTORA}** · {APRESENTACAO_AUTORA}"
if LINKEDIN_URL:
    autoria += f" · [LinkedIn]({LINKEDIN_URL})"
st.markdown(autoria)

with st.container(border=True):
    st.markdown("#### Sobre este projeto")
    st.markdown(
        f"- **O que é:** um case de análise de dados sobre cancelamento de clientes "
        f"(churn) em uma empresa de serviço por assinatura, com {fmt_int(len(df))} "
        f"clientes na base.\n"
        "- **A pergunta:** quem cancela, o que acontece antes disso e dá para agir "
        "a tempo de reter?\n"
        "- **O que você vai ver, em cerca de 2 minutos:** os perfis de maior risco, "
        "os sinais que antecedem o cancelamento e uma régua de alerta com plano de ação.\n"
        "- **Como usar:** role a página. Os gráficos mostram detalhes ao passar o "
        "mouse, e o simulador da seção 3 permite testar regras de alerta."
    )

if len(dff) < len(df):
    st.warning(
        f"Filtro ativo: mostrando {fmt_int(len(dff))} de {fmt_int(len(df))} clientes. "
        "Para ver a base completa, limpe os filtros na barra lateral."
    )

k1, k2, k3, k4 = st.columns([1, 1, 1, 1])
k1.metric("Clientes analisados", fmt_int(total))
k2.metric("Já cancelaram", f"{taxa_geral:.1f}%", help=f"{fmt_int(cancelados)} clientes")
k3.metric("Ativos já em zona de alerta", fmt_int(em_alerta_padrao),
          help=f"{ALERTA_LIGACOES}+ ligações ou {ALERTA_ATRASO}+ dias de atraso")
with k4:
    fig_rosca = px.pie(dff, names="situacao", hole=0.68, color="situacao",
                       color_discrete_map=CORES)
    fig_rosca.update_traces(textinfo="none",
                            hovertemplate="%{label}: %{value} (%{percent})")
    fig_rosca.update_layout(
        showlegend=False, height=150, margin=dict(l=0, r=0, t=0, b=0),
        annotations=[dict(text=f"{taxa_geral:.0f}%", x=0.5, y=0.5,
                          font_size=24, showarrow=False)],
    )
    st.plotly_chart(fig_rosca, use_container_width=True)

st.info(
    "**O cancelamento não acontece de surpresa.** Contrato mensal, excesso de "
    "contatos com o call center e atraso no pagamento concentram a saída, e uma "
    "régua de alerta simples identifica esses clientes antes de eles irem embora."
)

# =========================================================
# 1. QUEM SAI
# =========================================================
st.header("1. O risco se concentra em poucos perfis")

seg = tabela_segmentos(dff)
seg["posicao"] = seg["taxa"].apply(
    lambda t: "Acima da média" if t > taxa_geral else "Abaixo da média"
)
seg["rotulo"] = seg.apply(
    lambda r: f"{r['taxa']:.0f}% · {fmt_int(r['clientes'])} clientes", axis=1
)
seg_plot = seg.sort_values("taxa")

fig_seg = px.bar(
    seg_plot, x="taxa", y="segmento", orientation="h", color="posicao", text="rotulo",
    color_discrete_map={"Acima da média": COR_RISCO, "Abaixo da média": COR_OK},
    hover_data={"rotulo": False, "posicao": False, "taxa": ":.1f", "clientes": True,
                "cancelados": True, "peso_no_churn": ":.1f"},
    labels={"taxa": "Taxa de cancelamento (%)", "segmento": "", "clientes": "Clientes",
            "cancelados": "Cancelados", "peso_no_churn": "% das saídas"},
)
fig_seg.update_traces(textposition="outside", cliponaxis=False)
fig_seg.add_vline(x=taxa_geral, line_dash="dot", line_color="gray",
                  annotation_text=f"média geral ({taxa_geral:.0f}%)",
                  annotation_position="top")
fig_seg.update_layout(
    xaxis_range=[0, 128], legend_title_text="", height=max(320, 42 * len(seg_plot)),
    margin=dict(t=40),
)
st.plotly_chart(fig_seg, use_container_width=True)

topo = seg.loc[seg["peso_no_churn"].idxmax()]
st.markdown(
    f"Cada barra compara um perfil de clientes com a média geral. "
    f"**{topo['segmento']}** é o que mais pesa: {pct(topo['taxa'])} cancelam e "
    f"esse perfil responde por {pct(topo['peso_no_churn'])} das saídas. "
    f"*(Um mesmo cliente pode aparecer em mais de um perfil.)*"
)

# =========================================================
# 2. SINAIS
# =========================================================
st.header("2. Os sinais aparecem antes do cancelamento")

c_lig, c_atr = st.columns(2)

with c_lig:
    st.subheader("Ligações ao call center")
    t_lig = taxa_por_grupo(dff, "ligacoes_callcenter").sort_values("ligacoes_callcenter")
    st.plotly_chart(
        grafico_linha(
            t_lig, "ligacoes_callcenter", "Número de ligações",
            [(ALERTA_LIGACOES, "alerta", "gray", "top left"),
             (LIMITE_LIGACOES, "dispara", COR_RISCO, "top right")],
        ),
        use_container_width=True,
    )
    t_lig_faixa = taxa_por_grupo(
        dff.assign(f=dff["ligacoes_callcenter"].ge(LIMITE_LIGACOES)), "f"
    )
    alto = valor(t_lig_faixa, "f", True)
    baixo = valor(t_lig_faixa, "f", False)
    st.markdown(
        f"Com **{LIMITE_LIGACOES} ligações ou mais**, {pct(alto)} cancelam. "
        f"Abaixo disso, {pct(baixo)}."
    )

with c_atr:
    st.subheader("Atraso no pagamento")
    t_atr = taxa_por_grupo(
        dff.assign(inicio=(dff["dias_atraso"] // 5) * 5), "inicio"
    ).sort_values("inicio")
    st.plotly_chart(
        grafico_linha(
            t_atr, "inicio", "Dias de atraso (faixas de 5 dias)",
            [(ALERTA_ATRASO, "alerta", "gray", "top left"),
             (LIMITE_ATRASO, "dispara", COR_RISCO, "top right")],
        ),
        use_container_width=True,
    )
    t_atr_faixa = taxa_por_grupo(
        dff.assign(f=dff["dias_atraso"].ge(LIMITE_ATRASO)), "f"
    )
    alto = valor(t_atr_faixa, "f", True)
    baixo = valor(t_atr_faixa, "f", False)
    st.markdown(
        f"Com **{LIMITE_ATRASO} dias ou mais** de atraso, {pct(alto)} cancelam. "
        f"Abaixo disso, {pct(baixo)}."
    )

st.markdown(
    "São sinais que a empresa já registra e pode monitorar. O ponto de virada "
    "vem antes do corte: no alerta ainda há tempo de agir."
)

# =========================================================
# 3. PLANO: SIMULADOR DA RÉGUA
# =========================================================
st.header("3. Uma régua de alerta simples para agir antes")
st.write(
    "Mova os controles para testar a regra: o painel mostra quantas saídas ela "
    "teria captado e quantos clientes ativos exigiriam ação."
)

max_lig = int(max(dff["ligacoes_callcenter"].max(), 2))
max_atr = int(max(dff["dias_atraso"].max(), 2))
s1, s2 = st.columns(2)
lim_lig = s1.slider("Alertar a partir de quantas ligações", 1, max_lig,
                    min(ALERTA_LIGACOES, max_lig))
lim_atr = s2.slider("Alertar a partir de quantos dias de atraso", 1, max_atr,
                    min(ALERTA_ATRASO, max_atr))

flag = regra_alerta(dff, lim_lig, lim_atr)
sinalizados = int(flag.sum())
capturados = int(dff.loc[flag, "cancelou"].sum())
cobertura = capturados / cancelados * 100
precisao = capturados / sinalizados * 100 if sinalizados else float("nan")
ativos_alerta = dff[flag & (dff["cancelou"] == 0)]

m1, m2, m3 = st.columns(3)
m1.metric("Saídas que a regra teria captado", f"{cobertura:.0f}%",
          help="% dos clientes que cancelaram e teriam disparado o alerta")
m2.metric("Precisão do alerta", pct(precisao),
          help="% dos clientes sinalizados que de fato cancelaram")
m3.metric("Clientes ativos para agir agora", fmt_int(len(ativos_alerta)))
st.caption(
    "Teste retroativo: usa o comportamento registrado na base, sem saber se o "
    "sinal veio antes da decisão de sair. Quanto mais sensível a regra, mais "
    "saídas capta e mais clientes a equipe precisa abordar."
)

plano = [
    {"Gatilho": "Contrato mensal",
     "Ação": "Oferta de migração para trimestral ou anual",
     "Canal": "E-mail e app",
     "Métrica de sucesso": "% de clientes que migram"},
    {"Gatilho": f"{lim_lig} ligações ao call center",
     "Ação": "Atendimento especializado de resolução",
     "Canal": "Telefone",
     "Métrica de sucesso": "Redução de novas ligações e de cancelamentos"},
    {"Gatilho": f"{lim_atr} dias de atraso",
     "Ação": "Cobrança preventiva e opções de regularização",
     "Canal": "WhatsApp e e-mail",
     "Métrica de sucesso": f"% que regulariza antes de {LIMITE_ATRASO} dias"},
]

t_gm = taxa_por_grupo(dff, "faixa_gasto_medio")
gm_baixo = valor(t_gm, "faixa_gasto_medio", NOMES_QUARTIS[0])
gm_alto = valor(t_gm, "faixa_gasto_medio", NOMES_QUARTIS[3])
if pd.notna(gm_baixo) and pd.notna(gm_alto) and gm_baixo > gm_alto:
    plano.append({
        "Gatilho": "Baixo gasto médio",
        "Ação": "Engajamento e ampliação de uso",
        "Canal": "E-mail e app",
        "Métrica de sucesso": "Aumento do gasto médio",
    })

st.table(pd.DataFrame(plano).set_index("Gatilho"))

st.markdown(
    "**Como medir o resultado:** comparar, em 90 dias, a retenção dos clientes em "
    "alerta que receberam a ação com um grupo semelhante que não recebeu (grupo "
    "de controle). O ganho só vale se superar o custo da ação."
)

colunas_lista = ["CustomerID", "ligacoes_callcenter", "dias_atraso",
                 "duracao_contrato", "total_gasto"]
lista = ativos_alerta[colunas_lista].sort_values("dias_atraso", ascending=False)
st.download_button(
    "Baixar lista de clientes ativos em alerta (CSV)",
    lista.to_csv(index=False).encode("utf-8"),
    file_name="clientes_em_alerta.csv",
    mime="text/csv",
)

# =========================================================
# CONCLUSÃO
# =========================================================
st.header("Conclusão")
st.write(
    "Os clientes avisam antes de sair. Com poucos gatilhos monitorados, é possível "
    "agir enquanto a relação ainda está ativa, priorizando quem tem mais risco e "
    "mais volume."
)

# =========================================================
# EXPLORE OS DADOS (opcional)
# =========================================================
with st.expander("Explore os dados"):
    st.write("Veja, em percentual, como quem ficou e quem cancelou se distribuem em cada variável.")
    coluna = st.selectbox("Variável", list(NOMES_COLUNAS),
                          format_func=lambda c: NOMES_COLUNAS[c])
    fig_exp = px.histogram(dff, x=coluna, color="situacao", barnorm="percent",
                           color_discrete_map=CORES)
    fig_exp.update_layout(yaxis_title="% dos clientes na faixa", legend_title="Situação")
    st.plotly_chart(fig_exp, use_container_width=True)

    st.markdown("**Esses fatores se sobrepõem?** Compare duas variáveis ao mesmo "
                "tempo. Se a diferença persiste dentro de cada grupo, o fator tem "
                "efeito próprio.")
    OPCOES = {
        "Tipo de contrato": "contrato",
        "Sexo": "sexo",
        "Faixa de idade": "faixa_idade",
        "Faixa de total gasto": "faixa_gasto",
    }
    ca, cb = st.columns(2)
    var_x = ca.selectbox("Agrupar por", list(OPCOES), index=0)
    var_cor = cb.selectbox("Comparar dentro de cada grupo", list(OPCOES), index=1)
    if var_x == var_cor:
        st.info("Escolha duas variáveis diferentes.")
    else:
        cruzada = (
            dff.groupby([OPCOES[var_x], OPCOES[var_cor]], observed=True)["cancelou"]
            .agg(clientes="count", taxa="mean")
            .reset_index()
        )
        cruzada["taxa"] = cruzada["taxa"] * 100
        fig_cruz = px.bar(cruzada, x=OPCOES[var_x], y="taxa", color=OPCOES[var_cor],
                          barmode="group", hover_data=["clientes"])
        fig_cruz.update_layout(yaxis_title="Taxa de cancelamento (%)",
                               xaxis_title=var_x, legend_title=var_cor,
                               yaxis_range=[0, 108])
        st.plotly_chart(fig_cruz, use_container_width=True)

    st.markdown("**Base de dados**")
    st.dataframe(dff.drop(columns=["CustomerID", "situacao", "contrato",
                                   "faixa_idade", "faixa_gasto", "gasto_medio",
                                   "faixa_gasto_medio"]))

# =========================================================
# SOBRE ESTA ANÁLISE
# =========================================================
with st.expander("Sobre esta análise"):
    texto = (
        f"- **Base:** {fmt_int(len(df))} clientes ({removidos} registros com dados "
        f"vazios foram removidos).\n"
        "- **Limitações:** a análise mostra associação, não causa. Atraso e ligações "
        "podem ser consequência da vontade de sair. Padrões muito extremos são raros "
        "em dados reais, o que sugere uma base com finalidade didática.\n"
        "- **Idade e sexo:** servem para entender o perfil de quem sai, não para "
        "tratar clientes de forma diferente.\n"
        "- **Total gasto:** é em parte consequência do cancelamento (quem sai cedo "
        "gasta menos), por isso o app usa o gasto médio por período como cliente.\n"
        "- **Ferramentas:** Python, Pandas, Plotly e Streamlit.\n"
    )
    if MOSTRAR_ORIGEM:
        texto += (
            "- **Origem:** projeto desenvolvido a partir da Jornada Python da "
            "Hashtag Treinamentos; a análise, a narrativa e o plano de retenção "
            "são autorais.\n"
        )
    st.markdown(texto)
