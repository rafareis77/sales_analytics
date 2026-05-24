# modules/theme.py
# Módulo responsável pela injeção do tema CSS customizado no app Streamlit.

import streamlit as st

# Paleta de cores do tema
_CARD_BG_COLOR = "#262730"  # Fundo cinza escuro dos cards de KPI
_TEXT_COLOR    = "#FAFAFA"  # Cor do texto principal (branco)
_GOLD_COLOR    = "#E1C16E"  # Bege-ouro para os itens selecionados nos filtros
_DARK_TEXT     = "#1E1E1E"  # Texto escuro sobre fundo bege-ouro


def set_custom_theme() -> None:
     """
    Injeta o bloco de CSS customizado na página Streamlit.

    Estiliza:
    - Cards de KPI (.metric-card)
    - Caixas de multiselect (altura mínima e scroll)
    - Pílulas de itens selecionados ([data-baseweb="tag"])
    """
     
     css = _build_css()
     st.markdown(css, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Função interna
# ---------------------------------------------------------------------------


def _build_css() -> str:
     """Constrói e retorna o bloco <style> como string."""

     return f"""
    <style>

        /* --- Multiselect: Altura mínima e scroll vertical --- */
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child {{
            min-height: 100px !important;
            overflow-y: auto !important;
        }}

        /* --- Cards de KPI --- */
        .metric-card {{
            background-color: {_CARD_BG_COLOR};
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #444;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            text-align: center;
            margin-bottom: 10px;
        }}

        .metric-card h3 {{
            margin: 0;
            font-size: 1.2rem;
            color: #AAA;
            font-weight: normal;
        }}

        .metric-card h2 {{
            margin: 10px 0 0 0;
            font-size: 2rem;
            color: {_TEXT_COLOR};
            font-weight: bold;
        }}

        .metric-card .delta {{
            font-size: 0.9rem;
            color: #4CAF50;
            margin-top: 5px;
        }}

        /* --- Pílulas de filtro selecionado (bege-ouro) --- */
        [data-baseweb="tag"] {{
            background-color: {_GOLD_COLOR} !important;
            color: {_DARK_TEXT} !important;
            border-radius: 4px !important;
        }}

        [data-baseweb="tag"] svg {{
            color: {_DARK_TEXT} !important;
        }}

        [data-baseweb="tag"] svg:hover {{
            color: #FF0000 !important;
        }}

    </style>
    """
