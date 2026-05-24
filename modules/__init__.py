# modules/__init__.py
# Torna o diretório 'modules' um pacote Python.
# Os imports abaixo expõem as funções públicas de cada módulo
# diretamente via 'from modules import <função>'.

from modules.database import carrega_dados
from modules.sidebar import filtros_sidebar
from modules.kpis import renderiza_cards_kpis
from modules.charts import renderiza_graficos
from modules.pdf_report import gera_pdf_report
from modules.theme import set_custom_theme


__all__ = [
    "carrega_dados",
    "filtros_sidebar",
    "renderiza_cards_kpis",
    "renderiza_graficos",
    "gera_pdf_report",
    "set_custom_theme"
]