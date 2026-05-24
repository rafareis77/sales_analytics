# modules/sidebar.py
# Módulo responsável por criar a barra lateral e aplicação de filtros

import pandas as pd
import streamlit as st
import numpy as np


def filtros_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Renderiza a sidebar com banner, filtros e rodapé.
    Aplica os filtros ao Dataframe recebido e retorna a versão filtrada.

    Parâmetros:
        df (pd.DataFrame): Dataframe original completo e sem filtros.
    
    Retorna: 
        pd.DataFrame: Dataframe filtrado conforme as seleções do usuário
    """

    _renderiza_banner_sidebar()
    date_range, selected_regioes, selected_categorias, selected_produtos = _renderiza_widgets_filtros(df)
    return _aplica_filtros(df, date_range, selected_regioes, selected_categorias, selected_produtos)


# ------------------------------------------------------------------------------
# Funções internas
# ------------------------------------------------------------------------------

def _renderiza_banner_sidebar() -> None:
    """
    Exibe o banner estilizado no sidebar
    """
    
    st.sidebar.header("🔍 Filtros")


def _renderiza_widgets_filtros(df: pd.DataFrame):
    """
    Cria os widgets de filtro (data, região, categoria e produto) na barra lateral

    Retorna:
        tuple: (date_range, selected_regioes, selected_categorias, selected_produtos)
    """

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    date_range = st.sidebar.date_input(
        "Período de Análise",
        (min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    all_regioes = sorted(df["regiao"].unique())
    all_categorias = sorted(df["categoria"].unique())
    all_produtos = sorted(df["produto"].unique())

    selected_regioes = st.sidebar.multiselect("Regiões", all_regioes, default=all_regioes)
    selected_categorias = st.sidebar.multiselect("Categorias", all_categorias, default=all_categorias)
    selected_produtos = st.sidebar.multiselect("Produtos", all_produtos, default=all_produtos)

    return date_range, selected_regioes, selected_categorias, selected_produtos


def _aplica_filtros(
        df: pd.DataFrame,
        date_range,
        selected_regioes: list,
        selected_categorias: list,
        selected_produtos: list
        ) -> pd.DataFrame:
    """
    Aplica os filtros ao Dataframe original.

    Retorna:
        pd.DataFrame: Subconjunto do DataFrame correspondente as seleções.
    """

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    return df[
        (df["date"].dt.date >= start_date)
        & (df["date"].dt.date <= end_date)
        & (df["regiao"].isin(selected_regioes))
        & (df["categoria"].isin(selected_categorias))
        & (df["produto"].isin(selected_produtos))
    ].copy()
