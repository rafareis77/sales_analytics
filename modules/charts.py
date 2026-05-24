# module/charts.py
# Módulo responsável pela renderização dos gráficos

import pandas as pd
import plotly.express as px
import streamlit as st


# Mapeamento e ordem dos dias das semanas em português
_DIAS_PT_MAP: dict[int, str] = {
    0: "Segunda-Feira", 1: "Terça-Feira", 2: "Quarta-Feira",
    3: "Quinta-Feira", 4: "Sexta-Feira", 5: "Sábado", 6: "Domingo"
}

_DIAS_PT_ORDEM: list[str] = list(_DIAS_PT_MAP.values())


def renderiza_graficos(df: pd.DataFrame) -> None:
    """
    Renderiza todos os gráficos da Aba 1 (Visão Gráfica).

    Layout:
        Linha 1 → Evolução da Receita Diária (2/3) | Mix de Categorias (1/3)
        Linha 2 → Performance Regional (1/2)       | Análise por Dia da Semana (1/2)
        Linha 3 → Dispersão: Quantidade x Faturamento

    Parâmetros:
        df (pd.DataFrame): DataFrame filtrado pela sidebar.
    """

    _grafico_receita_e_categorias(df)
    _grafico_regional_e_dia_semana(df)
    _grafico_dispersao(df)


# ---------------------------------------------------------------------------
# Funções internas — linha 1
# ---------------------------------------------------------------------------

def _grafico_receita_e_categorias(df: pd.DataFrame) -> None:
    """Linha 1: gráfico de linha (evolução) + gráfico de pizza (categorias)."""

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Evolução da Receita Diária")
        daily_rev = df.groupby("date")[["faturamento"]].sum().reset_index()
        fig_line = px.line(daily_rev, x="date", y="faturamento", template="plotly_dark", height=400)
        fig_line.update_traces(fill="tozeroy", line=dict(color="#00CC96", width=3))
        st.plotly_chart(fig_line, width="stretch")

    with col_right:
        st.subheader("Mix de Categorias")
        cat_rev = df.groupby("categoria")[["faturamento"]].sum().reset_index()
        fig_pie = px.pie(
            cat_rev, values="faturamento", names="categoria",
            hole=0.5, template="plotly_dark", height=400,
        )
        st.plotly_chart(fig_pie, width="stretch")


# ---------------------------------------------------------------------------
# Funções internas — linha 2
# ---------------------------------------------------------------------------

def _grafico_regional_e_dia_semana(df: pd.DataFrame) -> None:
    """Linha 2: barras por região + barras por dia da semana."""

    c_a, c_b = st.columns(2)

    with c_a:
        st.subheader("Perfomance Regional")
        fig_bar = px.bar(
            df.groupby("regiao")[["faturamento"]].sum().reset_index(),
            x="regiao", y="faturamento", color="regiao",
            template="plotly_dark", text_auto=".2s,"
        )
        st.plotly_chart(fig_bar, width="stretch")

    with c_b:
        st.subheader("Análise por Dia da Semana")
        df_wd = df.copy()
        df_wd["weekday_num"] = df_wd["date"].dt.dayofweek
        df_wd["dia_semana"] = df_wd["weekday_num"].map(_DIAS_PT_MAP)
        wd_rev = (
            df_wd.groupby("dia_semana")[["faturamento"]]
            .mean()
            .reindex(_DIAS_PT_ORDEM)
            .reset_index()
        )
        fig_heat = px.bar(
            wd_rev, x="dia_semana", y="faturamento",
            title="Receita Média x Dia", template="plotly_dark",
        )
        st.plotly_chart(fig_heat, width="stretch")


# ---------------------------------------------------------------------------
# Funções internas — linha 3
# ---------------------------------------------------------------------------

def _grafico_dispersao(df: pd.DataFrame) -> None:
    """Linha 3: scatter plot de quantidade x faturamento por categoria."""

    st.subheader("Dispersão: Quantidade x Faturamento x Produto")
    fig_scat = px.scatter(
        df, x="quantidade", y="faturamento",
        color="categoria", size="faturamento",
        hover_data=["produto"], template="plotly_dark",
        height=500
    )
    st.plotly_chart(fig_scat,width="stretch")