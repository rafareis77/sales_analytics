# modules/pdf_report.py
# Módulo responsável pela geração do relatório executivo em PDF

from datetime import datetime
import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos


def gera_pdf_report(
        df_filtrado: pd.DataFrame,
        total_faturamento: float,
        total_quantidade: int,
        avg_ticket: float
) -> bytes:
    """
    Gera um relatório executivo de vendas em formato PDF.

    Parâmetros:
        df_dsa_filtrado  (pd.DataFrame): DataFrame filtrado com os dados de vendas.
        total_faturamento (float):        KPI de receita total.
        total_quantidade  (int):          KPI de quantidade total de vendas.
        avg_ticket        (float):        KPI de ticket médio.

    Retorna:
        bytes: Conteúdo bruto do PDF, pronto para o botão de download do Streamlit.
    """

    pdf = _cria_pdf_base()
    _adciona_titulo(pdf)
    _adciona_bloco_kpis(pdf, total_faturamento, total_quantidade, avg_ticket)
    _adciona_tabela_top15(pdf, df_filtrado)

    return _exporta_pdf(pdf)

# ---------------------------------------------------------------------------
# Funções internas
# ---------------------------------------------------------------------------


def _cria_pdf_base() -> FPDF:
    """Inicializa e configura o objeto FPDF com quebra de página automática"""

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    return pdf


def _adciona_titulo(pdf: FPDF) -> None:
    """Adciona título e carimbo de data e hora no topo do pdf"""

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(
        0, 10, "Relatório Executivo de Vendas",
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(
        0, 8, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT,
    )


def _adciona_bloco_kpis(
        pdf: FPDF, 
        total_faturamento: float, 
        total_quantidade: int, 
        avg_ticket: float) -> None:
    
    """Desenha o bloco cinza com os 3 KPIs principais"""

    pdf.set_fill_color(240, 240, 240)
    pdf.rect(10, 35, 190, 25, "F")
    pdf.set_y(40)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 8, "Receita Total", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, "Quantidade", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, "Ticket Médio", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(60, 8, f"R$ {total_faturamento:,.2f}", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, f"R$ {total_quantidade:,}", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, f"R$ {avg_ticket:,.2f}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(15)


def _adciona_tabela_top15(pdf: FPDF, df: pd.DataFrame) -> None:
    """Adiciona a tabela com as top 15 vendas por receita ao PDF."""

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Top 15 Vendas por Receita", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    col_widths = [30, 30, 30, 40, 25, 30]
    headers = ["Data", "Regiao", "Categoria", "Produto", "Qtd", "Receita"]

    # Cabeçalho da tabela
    pdf.set_font("Helvetica", "B", 9)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, 1, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.ln()

    # Linhas de dados
    pdf.set_font("Helvetica", "", 9)
    df_top = df.sort_values("faturamento", ascending=False).head(15)
    for _, row in df_top.iterrows():
        data = [
            str(row["date"].date()),
            row["regiao"],
            row["categoria"],
            row["produto"][:20],
            str(row["quantidade"]),
            f"R$ {row['faturamento']:,.2f}",
        ]

        for i, d in enumerate(data):
            safe_txt = str(d).encode("latin-1", "replace").decode("latin-1")
            align = "C" if i == 4 else "L"
            pdf.cell(col_widths[i], 7, safe_txt, 1, align=align, new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.ln()


def _exporta_pdf(pdf: FPDF) -> bytes:
    """Converte o objeto FPDF para bytes e retorna."""

    result = pdf.output()

    return result.encode("latin-1") if isinstance(result, str) else bytes(result)