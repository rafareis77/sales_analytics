# app.py
# Mini-Projeto - Data App Para Dashboard Interativo de Sales Analytics
# Ponto de entrada principal — orquestra os módulos do pacote 'modules/'.

from datetime import date
import streamlit as st

from modules import (
    carrega_dados,
    filtros_sidebar,
    gera_pdf_report,
    renderiza_cards_kpis,
    renderiza_graficos,
    set_custom_theme
)

# ---------------------------------------------------------------------------
# Configuração da página — DEVE ser a primeira chamada Streamlit do script
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Dashboard Interativo Sales Analytics",
    page_icon=":computer:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Função principal
# ---------------------------------------------------------------------------


def funcao_principal() -> None:
    """
    Função principal que orquestra todo o dashboard:
    1. Aplica tema CSS customizado.
    2. Carrega os dados do banco SQLite.
    3. Renderiza a sidebar com filtros e obtém o DataFrame filtrado.
    4. Exibe títulos, KPIs, abas de gráficos, tabela e exportação.
    """

    # 1. Tema
    set_custom_theme()

    # 2. Dados 
    df = carrega_dados()

    # 3. Sidebar + filtros 
    df_filtrado = filtros_sidebar(df)

    # 4. Cabeçalho da pagina principal 
    st.title("Sales Analytics")
    st.title("📊 Data App Para Dashboard Interativo de Sales Analytics")
    st.subheader("Com Banco de Dados SQLite e Streamlit")
    st.write(
        "Navegue pelo dashboard e use os filtros na barra lateral para diferentes visualizações. "
        "Os dados podem ser exportados para formato CSV e PDF."
    )
    st.markdown("---")
    st.markdown("Visão Consolidada de Vendas com KPIs.")

    # Guarda execução se o DataFrame filtrado estiver vazio
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
        
        return
    
    # 5. KPIs
    total_faturamento, total_qty, avg_ticket = renderiza_cards_kpis(df_filtrado)
    st.markdown("---")

    # 6. Abas
    tab1, tab2 = st.tabs(["📈 Visão Gráfica", "📄 Dados Detalhados & Exportação (CSV e PDF)"])

    with tab1:
        renderiza_graficos(df_filtrado)

    with tab2:
        _renderiza_aba_exportacao(df_filtrado, total_faturamento, total_qty, avg_ticket)

    # 7. Rodapé 
    _renderiza_rodape()


# ---------------------------------------------------------------------------
# Helpers de layout
# ---------------------------------------------------------------------------

def _renderiza_aba_exportacao(
        df_filtrado,
        total_faturamento: float,
        total_qty: int,
        avg_ticket: float
) -> None:
    
    """Renderiza a aba de visualização tabular e botões de exportação (CSV / PDF)."""

    st.subheader("Visualização Tabular")
    st.dataframe(df_filtrado, width="stretch", height=400)

    st.markdown("### 📥 Área de Exportação")
    c_exp1, c_exp2 = st.columns(2)

    with c_exp1:
        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="💾 Baixar CSV (Excel)",
            data=csv,
            file_name="dados_filtrados.csv",
            mime="text/csv",
            width="stretch",
        )

    with c_exp2:
        if st.button("📄 Gerar Relatório PDF", use_container_width=True):
            with st.spinner("Renderizando PDF..."):
                pdf_bytes = gera_pdf_report(df_filtrado, total_faturamento, total_qty, avg_ticket)
                st.download_button(
                    label="⬇️ Clique aqui para Salvar PDF",
                    data=pdf_bytes,                          
                    file_name=f"Relatorio_Vendas_{date.today()}.pdf",
                    mime="application/pdf",
                    key="pdf-download-final",
        )


def _renderiza_rodape() -> None:
    """Exibe o rodapé com informações sobre o app."""

    st.markdown("---")
    with st.expander("ℹ️ Sobre Esta Data App", expanded=False):
        st.info("Este dashboard combina as melhores práticas de visualização e manipulação de dados.")
        st.markdown("""
        **Recursos Integrados:**
        - **Engine:** Python + Streamlit + SQLite.
        - **Visualização:** Plotly Express e tema Dark no Streamlit.
        - **Relatórios:** Geração de PDF com FPDF (compatível com Latin-1).
        - **Performance:** Cache de dados (`@st.cache_data`).
        """)


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    funcao_principal()
