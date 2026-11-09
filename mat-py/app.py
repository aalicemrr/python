import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Afazeres Domésticos",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────────────────────
ANOS = [2016, 2017, 2018, 2019, 2022]
REGIOES = ["Brasil", "Norte", "Nordeste", "Sudeste", "Sul", "Centro-Oeste"]
FAIXAS = ["14 a 29 anos", "30 a 49 anos", "50 a 59 anos", "60 anos ou mais"]

# ──────────────────────────────────────────────────────────────
# Paleta inspirada nas pinturas de Leonardo da Vinci
#   Pergaminho dos cadernos de esboço, tinta sépia, sanguínea (giz vermelho),
#   o céu azul-acinzentado da Mona Lisa, o ocre e o verde-oliva do sfumato.
# ──────────────────────────────────────────────────────────────
PERGAMINHO = "#F4ECDF"      # fundo
PERGAMINHO_CLARO = "#FBF7F0"  # cartões
PERGAMINHO_ESCURO = "#EDE2CF"  # barra lateral
BORDA = "#E3D6C1"
SEPIA = "#3E2F23"            # texto principal
SEPIA_SUAVE = "#7A6957"      # texto secundário
SANGUINEA = "#A4533A"        # mulheres
AZUL_MONA_LISA = "#4F6D7A"   # homens
OCRE = "#C0913F"             # destaque
OLIVA = "#6E7B4E"
UMBRA = "#5A4632"

CORES_SEXO = {"Homens": AZUL_MONA_LISA, "Mulheres": SANGUINEA}
CORES_GRUPO = {
    "Homem branco": "#93A9B1",
    "Homem preto/pardo": "#3E5864",
    "Mulher branca": "#D7A07C",
    "Mulher preta/parda": "#8A3A25",
}
CORES_COMPARACAO = {"Todas as pessoas": "#CFC0A6", "Trabalham fora": OLIVA}
CORES_LINHAS = [SANGUINEA, AZUL_MONA_LISA, OCRE, OLIVA, "#7D5C76", "#A67B5B",
                "#2F4A3A", "#B5704A", "#6A7F95", "#8C7A3A"]

# ──────────────────────────────────────────────────────────────
# Estilo (fontes, cores e layout)
# ──────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Nunito+Sans:wght@400;600;700&display=swap');

    html, body, .stApp, p, li, label, input, textarea, .stMarkdown, .stCaption {{
        font-family: 'Nunito Sans', sans-serif;
        color: {SEPIA};
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Cormorant Garamond', serif !important;
        color: {SEPIA} !important;
        font-weight: 700 !important;
        letter-spacing: .005em;
    }}
    .stApp {{
        background:
            radial-gradient(circle at 15% 0%, rgba(192,145,63,.08), transparent 45%),
            radial-gradient(circle at 100% 100%, rgba(79,109,122,.07), transparent 40%),
            {PERGAMINHO};
    }}
    .block-container {{ padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1320px; }}

    /* Barra lateral */
    [data-testid="stSidebar"] {{
        background: {PERGAMINHO_ESCURO};
        border-right: 1px solid {BORDA};
    }}
    [data-testid="stSidebar"] h3 {{ font-size: 1.4rem; margin-top: .4rem; }}
    .sidebar-marca {{
        font-family: 'Cormorant Garamond', serif; font-weight: 700; font-size: 1.7rem;
        color: {SEPIA}; line-height: 1.1;
    }}
    .sidebar-sub {{ color: {SEPIA_SUAVE}; font-size: .85rem; margin: .2rem 0 1.2rem 0;
                    font-style: italic; }}

    /* Campos de seleção mais suaves */
    [data-baseweb="select"] > div, [data-testid="stFileUploaderDropzone"] {{
        background: {PERGAMINHO_CLARO} !important;
        border-color: {BORDA} !important;
        border-radius: 12px !important;
    }}
    [data-baseweb="tag"] {{ background: {SANGUINEA} !important; border-radius: 8px !important; }}

    /* Cabeçalho */
    .hero {{
        position: relative; overflow: hidden;
        background:
            radial-gradient(ellipse at 85% 20%, rgba(192,145,63,.35), transparent 55%),
            radial-gradient(ellipse at 10% 110%, rgba(110,123,78,.35), transparent 50%),
            linear-gradient(135deg, #3E2F23 0%, #5A4632 50%, #7A5A3E 100%);
        border-radius: 26px; padding: 2.6rem 2.8rem; color: {PERGAMINHO_CLARO};
        box-shadow: 0 14px 40px rgba(62, 47, 35, .18); margin-bottom: 1.8rem;
    }}
    .hero h1 {{
        color: {PERGAMINHO_CLARO} !important; font-size: 2.9rem; line-height: 1.1;
        margin: 0 0 .6rem 0; padding: 0;
    }}
    .hero p {{ color: rgba(251,247,240,.86); font-size: 1.05rem; line-height: 1.6;
               margin: 0; max-width: 780px; }}
    .hero .frase {{
        font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 1.3rem;
        color: #E9CF9C; margin-top: 1.1rem;
    }}
    .pill {{
        display: inline-block; background: rgba(251,247,240,.12); border: 1px solid rgba(251,247,240,.3);
        padding: .3rem .9rem; border-radius: 999px; font-size: .78rem; font-weight: 700;
        letter-spacing: .08em; text-transform: uppercase; margin-bottom: 1rem; color: #F1DFBC;
    }}

    /* Cartões de indicadores */
    .kpi {{
        background: {PERGAMINHO_CLARO}; border-radius: 20px; padding: 1.3rem 1.5rem;
        border: 1px solid {BORDA}; box-shadow: 0 6px 18px rgba(62, 47, 35, .06);
        height: 100%; position: relative;
    }}
    .kpi::before {{
        content: ""; position: absolute; left: 1.5rem; top: 0; width: 48px; height: 4px;
        border-radius: 0 0 6px 6px; background: var(--cor);
    }}
    .kpi-rotulo {{ color: {SEPIA_SUAVE}; font-size: .8rem; font-weight: 700;
                   text-transform: uppercase; letter-spacing: .07em; margin-top: .3rem; }}
    .kpi-valor {{ font-family: 'Cormorant Garamond', serif; font-size: 2.7rem; font-weight: 700;
                  color: var(--cor); line-height: 1.1; margin-top: .3rem; }}
    .kpi-valor span {{ font-family: 'Nunito Sans', sans-serif; font-size: .9rem;
                       color: {SEPIA_SUAVE}; font-weight: 600; margin-left: .3rem; }}
    .kpi-nota {{ color: {SEPIA_SUAVE}; font-size: .85rem; margin-top: .3rem; }}

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {{
        gap: .3rem; background: {PERGAMINHO_CLARO}; padding: .45rem; border-radius: 18px;
        border: 1px solid {BORDA}; margin-top: 1.6rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 44px; padding: 0 1.3rem; border-radius: 13px;
        font-weight: 600; color: {SEPIA_SUAVE};
    }}
    .stTabs [data-baseweb="tab"] p {{ font-size: .95rem; }}
    .stTabs [aria-selected="true"] {{ background: {SEPIA}; }}
    .stTabs [aria-selected="true"] p {{ color: {PERGAMINHO_CLARO} !important; }}
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] {{ display: none; }}

    /* Títulos de seção */
    .secao {{ margin: 1.8rem 0 .6rem 0; }}
    .secao h3 {{ font-size: 1.75rem; margin: 0; padding: 0; }}
    .secao p {{ color: {SEPIA_SUAVE}; font-size: .95rem; margin: .1rem 0 0 0; }}

    /* Gráficos e cartões */
    [data-testid="stPlotlyChart"] {{
        background: {PERGAMINHO_CLARO}; border-radius: 20px; padding: .8rem 1rem;
        border: 1px solid {BORDA}; box-shadow: 0 6px 18px rgba(62, 47, 35, .05);
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {PERGAMINHO_CLARO}; border-radius: 20px; border-color: {BORDA} !important;
    }}
    [data-testid="stImage"] img {{ border-radius: 14px; filter: sepia(.12); }}
    [data-testid="stAlert"] {{ background: rgba(192,145,63,.12); border-radius: 14px; color: {SEPIA}; }}

    a {{ color: {SANGUINEA} !important; text-decoration: none; font-weight: 600; }}
    a:hover {{ text-decoration: underline; }}
    hr {{ border-color: {BORDA} !important; }}

    .rodape {{ text-align: center; color: {SEPIA_SUAVE}; font-size: .85rem;
               margin-top: 3rem; padding-top: 1.4rem; border-top: 1px solid {BORDA}; }}
    .rodape em {{ font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────
# Funções auxiliares de interface
# ──────────────────────────────────────────────────────────────
def titulo_secao(titulo, descricao=None):
    sub = f"<p>{descricao}</p>" if descricao else ""
    st.markdown(f'<div class="secao"><h3>{titulo}</h3>{sub}</div>', unsafe_allow_html=True)


def cartao(coluna, rotulo, valor, cor, nota=""):
    coluna.markdown(
        f"""
        <div class="kpi" style="--cor:{cor}">
            <div class="kpi-rotulo">{rotulo}</div>
            <div class="kpi-valor">{valor:.1f}<span>horas/semana</span></div>
            <div class="kpi-nota">{nota}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def estilizar(fig, altura=430):
    fig.update_layout(
        template="simple_white",
        height=altura,
        font=dict(family="Nunito Sans, sans-serif", size=13, color=SEPIA),
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title=None,
                    font=dict(color=SEPIA_SUAVE)),
        hoverlabel=dict(font_family="Nunito Sans, sans-serif", bgcolor=PERGAMINHO_CLARO,
                        bordercolor=BORDA, font_color=SEPIA),
        bargap=0.28,
        bargroupgap=0.06,
    )
    fig.update_xaxes(showgrid=False, linecolor=BORDA, ticks="", tickfont=dict(color=SEPIA_SUAVE),
                     title_font=dict(size=12, color=SEPIA_SUAVE))
    fig.update_yaxes(showgrid=True, gridcolor="#ECE3D4", showline=False, ticks="", zeroline=False,
                     tickfont=dict(color=SEPIA_SUAVE), title_font=dict(size=12, color=SEPIA_SUAVE))
    fig.update_traces(textfont=dict(size=11, color=SEPIA), textposition="outside", cliponaxis=False,
                      marker_line_width=0, opacity=0.92, selector=dict(type="bar"))
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1],
                                               font=dict(family="Cormorant Garamond, serif",
                                                         size=17, color=SEPIA)))
    return fig


# ──────────────────────────────────────────────────────────────
# Leitura dos dados
# ──────────────────────────────────────────────────────────────
@st.cache_data
def ler_tabela_raca(arquivo):
    planilha = pd.ExcelFile(arquivo)
    lista = []
    for ano in ANOS:
        df = pd.read_excel(planilha, sheet_name=str(ano), header=None)
        df = df.iloc[8:41, 0:8]
        df.columns = ["local", "total", "total_branca", "total_preta_parda",
                      "homem_branco", "homem_preto_pardo", "mulher_branca", "mulher_preta_parda"]
        df["ano"] = ano
        lista.append(df)
    dados = pd.concat(lista)
    dados["local"] = dados["local"].str.strip()
    dados["homens"] = (dados["homem_branco"] + dados["homem_preto_pardo"]) / 2
    dados["mulheres"] = (dados["mulher_branca"] + dados["mulher_preta_parda"]) / 2
    dados["diferenca"] = dados["mulheres"] - dados["homens"]
    return dados


@st.cache_data
def ler_tabela_idade(arquivo):
    planilha = pd.ExcelFile(arquivo)
    lista = []
    for ano in ANOS:
        df = pd.read_excel(planilha, sheet_name=str(ano), header=None)
        df = df.iloc[7:40]
        for i in range(len(FAIXAS)):
            coluna = 4 + i * 3
            parte = pd.DataFrame({
                "local": df[0].str.strip(),
                "faixa": FAIXAS[i],
                "homens": df[coluna + 1],
                "mulheres": df[coluna + 2],
                "ano": ano,
            })
            lista.append(parte)
    return pd.concat(lista)


# ──────────────────────────────────────────────────────────────
# Barra lateral
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-marca">Quem cuida<br>de quem cuida?</div>'
                '<div class="sidebar-sub">Um olhar sobre o trabalho invisível no Brasil</div>',
                unsafe_allow_html=True)

    with st.expander("📂 Carregar planilhas", expanded=False):
        upload_111 = st.file_uploader("Tabela 1.1.1 (todas as pessoas)", type=["xls"])
        upload_112 = st.file_uploader("Tabela 1.1.2 (ocupadas por idade)", type=["xls"])
        upload_113 = st.file_uploader("Tabela 1.1.3 (ocupadas por raça)", type=["xls"])

todos = ler_tabela_raca(upload_111 or r"H:\python\3-Etapa\mat-py\tabela_1_1_1.xls")
idade = ler_tabela_idade(upload_112 or r"H:\python\3-Etapa\mat-py\tabela_1_1_2.xls")
ocupados = ler_tabela_raca(upload_113 or r"H:\python\3-Etapa\mat-py\tabela_1_1_3.xls")

lista_estados = sorted([x for x in todos["local"].unique() if x not in REGIOES])

with st.sidebar:
    st.markdown("### Escolha o que ver")
    ano = st.selectbox("Ano da pesquisa", ANOS[::-1])
    estados = st.multiselect("Estados", lista_estados,
                             default=["Amazonas", "Bahia", "Ceará", "Pernambuco"])
    faixa = st.selectbox("Faixa etária", ["Todas"] + FAIXAS)
    st.divider()
    st.caption("Pessoas de 14 anos ou mais. Valores em horas por semana. "
               "Fonte: IBGE, PNAD Contínua.")

if not estados:
    st.info("Escolha pelo menos um estado na barra lateral para começar.", icon="👈")
    st.stop()

dados_ano = todos[todos["ano"] == ano]
filtrado = dados_ano[dados_ano["local"].isin(estados)]
brasil = dados_ano[dados_ano["local"] == "Brasil"].iloc[0]

# ──────────────────────────────────────────────────────────────
# Cabeçalho e indicadores
# ──────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="hero">
        <div class="pill">PNAD Contínua · {ano}</div>
        <h1>Afazeres Domésticos<br>e Cuidado de Pessoas</h1>
        <p>Lavar, cozinhar, organizar, cuidar das crianças e dos mais velhos. Este painel mostra
        quantas horas por semana homens e mulheres de 14 anos ou mais dedicam a esse trabalho
        que sustenta as famílias, mas raramente é visto ou pago.</p>
        <div class="frase">Por trás de cada número, existem horas de cuidado que ninguém vê.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4, gap="medium")
cartao(col1, "Homens · Brasil", brasil["homens"], AZUL_MONA_LISA, "Média nacional")
cartao(col2, "Mulheres · Brasil", brasil["mulheres"], SANGUINEA, "Média nacional")
cartao(col3, "Diferença · Brasil", brasil["diferenca"], OCRE,
       f"≈ {brasil['diferenca'] * 52 / 24:.0f} dias inteiros a mais por ano")
cartao(col4, "Diferença · Estados", filtrado["diferenca"].mean(), OLIVA,
       f"Média dos {len(filtrado)} estados escolhidos")

aba1, aba2, aba3, aba4, aba5 = st.tabs(
    ["Sexo", "Sexo e raça", "Evolução", "Trabalho fora", "Para ler"]
)

# ──────────────────────────────────────────────────────────────
# Aba 1 – Sexo
# ──────────────────────────────────────────────────────────────
with aba1:
    esq, direita = st.columns([3, 2], gap="large")

    with esq:
        titulo_secao("Horas semanais por sexo e estado", "Comparação direta entre homens e mulheres.")
        grafico = filtrado.melt(id_vars="local", value_vars=["homens", "mulheres"],
                                var_name="Sexo", value_name="Horas")
        grafico["Sexo"] = grafico["Sexo"].replace({"homens": "Homens", "mulheres": "Mulheres"})
        fig = px.bar(grafico, x="local", y="Horas", color="Sexo", barmode="group", text_auto=".1f",
                     labels={"local": "Estado"}, color_discrete_map=CORES_SEXO)
        st.plotly_chart(estilizar(fig), width="stretch")

    with direita:
        titulo_secao("Quantas horas a mais as mulheres fazem", "A linha tracejada marca a média do Brasil.")
        fig = px.bar(filtrado.sort_values("diferenca"), x="diferenca", y="local", orientation="h",
                     text_auto=".1f", labels={"diferenca": "Horas a mais por semana", "local": ""},
                     color_discrete_sequence=[SANGUINEA])
        fig.add_vline(x=brasil["diferenca"], line_dash="dash", line_color=OCRE, line_width=2,
                      annotation_text="Brasil", annotation_font_color=UMBRA)
        fig = estilizar(fig)
        fig.update_xaxes(showgrid=True, gridcolor="#ECE3D4")
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig, width="stretch")

# ──────────────────────────────────────────────────────────────
# Aba 2 – Sexo e raça
# ──────────────────────────────────────────────────────────────
with aba2:
    nomes = {
        "homem_branco": "Homem branco",
        "homem_preto_pardo": "Homem preto/pardo",
        "mulher_branca": "Mulher branca",
        "mulher_preta_parda": "Mulher preta/parda",
    }
    grafico = filtrado.melt(id_vars="local", value_vars=list(nomes), var_name="Grupo", value_name="Horas")
    grafico["Grupo"] = grafico["Grupo"].replace(nomes)

    titulo_secao("Horas semanais por sexo e raça", "Nos estados que você escolheu.")
    fig = px.bar(grafico, x="local", y="Horas", color="Grupo", barmode="group", text_auto=".1f",
                 labels={"local": "Estado"}, color_discrete_map=CORES_GRUPO)
    st.plotly_chart(estilizar(fig), width="stretch")

    titulo_secao("Distribuição das horas em todos os estados",
                 "Cada ponto é um estado. Passe o mouse para ver qual.")
    todos_estados = dados_ano[~dados_ano["local"].isin(REGIOES)]
    box = todos_estados.melt(id_vars="local", value_vars=list(nomes), var_name="Grupo", value_name="Horas")
    box["Grupo"] = box["Grupo"].replace(nomes)
    fig = px.box(box, x="Grupo", y="Horas", color="Grupo", points="all", hover_name="local",
                 color_discrete_map=CORES_GRUPO, labels={"Grupo": ""})
    fig = estilizar(fig, altura=460)
    fig.update_traces(marker=dict(size=6, opacity=.75), line_width=1.6)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width="stretch")

# ──────────────────────────────────────────────────────────────
# Aba 3 – Evolução
# ──────────────────────────────────────────────────────────────
with aba3:
    titulo_secao("Evolução da diferença entre mulheres e homens",
                 "Horas semanais a mais dedicadas pelas mulheres, ano a ano.")
    evolucao = todos[todos["local"].isin(estados + ["Brasil"])]
    fig = px.line(evolucao, x="ano", y="diferenca", color="local", markers=True,
                  labels={"ano": "Ano", "diferenca": "Horas a mais (mulheres)", "local": "Local"},
                  color_discrete_sequence=CORES_LINHAS, line_shape="spline")
    fig.update_traces(line_width=2.6, marker=dict(size=9, line=dict(width=2, color=PERGAMINHO_CLARO)))
    fig.for_each_trace(lambda t: t.update(line=dict(color=SEPIA, dash="dot", width=3),
                                          marker=dict(color=SEPIA))
                       if t.name == "Brasil" else ())
    fig = estilizar(fig, altura=480)
    fig.update_xaxes(tickvals=ANOS)
    st.plotly_chart(fig, width="stretch")
    st.info("Não houve pesquisa desse tema em 2020 e 2021 por causa da pandemia.", icon="🕯️")

# ──────────────────────────────────────────────────────────────
# Aba 4 – Trabalho fora
# ──────────────────────────────────────────────────────────────
with aba4:
    topo_esq, topo_dir = st.columns([3, 1], vertical_alignment="bottom")
    with topo_esq:
        titulo_secao("Todas as pessoas x pessoas que trabalham fora",
                     "Mesmo com um emprego, a jornada em casa continua.")
    with topo_dir:
        escolha = st.radio("Mostrar", ["Mulheres", "Homens"], horizontal=True,
                           label_visibility="collapsed")

    ocupados_ano = ocupados[(ocupados["ano"] == ano) & (ocupados["local"].isin(estados))]
    comparacao = pd.DataFrame({
        "Estado": list(filtrado["local"]) * 2,
        "Grupo": ["Todas as pessoas"] * len(filtrado) + ["Trabalham fora"] * len(ocupados_ano),
        "Mulheres": list(filtrado["mulheres"]) + list(ocupados_ano["mulheres"]),
        "Homens": list(filtrado["homens"]) + list(ocupados_ano["homens"]),
    })
    fig = px.bar(comparacao, x="Estado", y=escolha, color="Grupo", barmode="group", text_auto=".1f",
                 labels={escolha: "Horas por semana"}, color_discrete_map=CORES_COMPARACAO)
    st.plotly_chart(estilizar(fig), width="stretch")

    titulo_secao("Quem trabalha fora, por faixa etária",
                 f"Faixa selecionada: {faixa.lower()}.")
    idade_ano = idade[(idade["ano"] == ano) & (idade["local"].isin(estados))]
    if faixa != "Todas":
        idade_ano = idade_ano[idade_ano["faixa"] == faixa]
    grafico = idade_ano.melt(id_vars=["local", "faixa"], value_vars=["homens", "mulheres"],
                             var_name="Sexo", value_name="Horas")
    grafico["Sexo"] = grafico["Sexo"].replace({"homens": "Homens", "mulheres": "Mulheres"})
    fig = px.bar(grafico, x="faixa", y="Horas", color="Sexo", barmode="group", facet_col="local",
                 text_auto=".1f", labels={"faixa": ""}, color_discrete_map=CORES_SEXO)
    fig = estilizar(fig, altura=470)
    fig.update_xaxes(tickangle=-30)
    st.plotly_chart(fig, width="stretch")

# ──────────────────────────────────────────────────────────────
# Aba 5 – Para ler
# ──────────────────────────────────────────────────────────────
with aba5:
    titulo_secao("Para ir além dos números", "Reportagens e análises sobre o trabalho invisível.")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            st.markdown("#### Carga Mental Feminina")
            st.image(r"H:\python\3-Etapa\mat-py\carga_mental.jpg", width="stretch")
            st.write("Além das tarefas em si, as mulheres costumam ficar responsáveis por planejar e lembrar de tudo "
                     "que a casa e a família precisam. Esse trabalho invisível pesa na saúde mental.")
            st.markdown("**Leia mais**")
            st.markdown("- [Le Monde Diplomatique: Você poderia ter me pedido - o trabalho invisível das mulheres](https://diplomatique.org.br/voce-poderia-ter-me-pedido-o-trabalho-invisivel-das-mulheres/)")
            st.markdown("- [Folha de Pernambuco: Saúde mental e a sobrecarga feminina](https://www.folhape.com.br/noticias/opiniao/saude-mental-e-a-sobrecarga-feminina-quem-cuida-de-quem-cuida/320078/)")
            st.markdown("- [O Povo: Protagonizado por mulheres, trabalho de cuidado segue invisível](https://www.opovo.com.br/noticias/enem/2023/11/05/amp/protagonizado-por-mulheres-trabalho-de-cuidado-segue-invisivel-entenda.html)")

    with col2:
        with st.container(border=True):
            st.markdown("#### Economia do Cuidado")
            st.image(r"H:\python\3-Etapa\mat-py\grafico_transporte.png", width="stretch")
            st.write("Cuidar de crianças, idosos e da casa é um trabalho que movimenta a economia, mas não é pago "
                     "e quase sempre fica com as mulheres, principalmente as mulheres negras.")
            st.markdown("**Leia mais**")
            st.markdown("- [O Povo+: Economia do cuidado, um trabalho invisível e não remunerado](https://mais.opovo.com.br/reportagens-especiais/mulheres-e-cuidado-economia-sociedade/2024/06/25/economia-do-cuidado-um-trabalho-invisivel-e-nao-remunerado-das-mulheres.html)")
            st.markdown("- [Forbes: Mulheres são responsáveis por mais de 75% do trabalho não remunerado](https://forbes.com.br/forbes-mulher/2023/11/economia-do-cuidado-mulheres-sao-responsaveis-por-mais-de-75-do-trabalho-nao-remunerado/)")
            st.markdown("- [Politize: O que é economia do cuidado](https://www.politize.com.br/economia-do-cuidado/)")

    st.caption("Imagens: Wikimedia Commons.")