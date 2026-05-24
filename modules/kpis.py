# modules/kpis.py
# Módulo repsonsável pelo cálculo e renderização dos cards de KPIs

import numpy as np
import pandas as pd
import streamlit as st


def renderiza_cards_kpis(df: pd.DataFrame) -> tuple[float, int, float]:
    
    """
    Calccula os 4 principais KPIs e os exibe em cards estilizados.

    Parâmetros:
        df (pd.DataFrame): DataFrame já filtrado pela sidebar.

    Retorna:
        tuple: (total_faturamento, total_qty, avg_ticket)
               Valores reutilizados na geração do relatório PDF.
    """

    total_faturamento, total_qty, avg_ticket, transactions = _calcula_kpis(df)
    _renderiza_layout_cards(total_faturamento, total_qty, avg_ticket, transactions)

    return total_faturamento, total_qty, avg_ticket


# ----------------------------------------------------------------------------
# Funções internas
# ----------------------------------------------------------------------------


def _calcula_kpis(df: pd.DataFrame) -> tuple:

    """Calcula os valores numéricos dos KPIs a partir do Dataframe"""

    total_faturamento = df["faturamento"].sum()
    total_qty = df["quantidade"].sum()
    avg_ticket = total_faturamento / total_qty if total_qty > 0 else 0
    transactions = df.shape[0]

    return total_faturamento, total_qty, avg_ticket, transactions


def _renderiza_layout_cards(
        total_faturamento: float,
        total_qty: int,
        avg_ticket: float,
        transactions: int
) -> None:
    
    """Renderiza os 4 cards usando o streamlit"""

    delta_rev = np.random.uniform(-5, 15)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>Receita Total</h3>
                <h2>R$ {total_faturamento:,.0f}</h2>
                <div class="delta" style=color: {'#4CAF50' if delta_rev > 0 else '#FF5252'}>
                    {delta_rev:+.1f}% vs meta
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>Vendas (Qtd)</h3>
                <h2>{total_qty:,.0f}</h2>
                <div class="delta">Unidades Vendidas</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>Ticket Médio</h3>
                <h2>R$ {avg_ticket:,.2f}</h2>
                <div class="delta">Por transação</div> 
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>Transações</h3>
                <h2>{transactions}</h2>
                <div class="delta">Volume Total</div>
            </div>
            """,
            unsafe_allow_html=True
        )