# 📊 Dashboard Interativo de Sales Analytics

> **Dashboard interativo de análise de vendas construído com **Python**, **Streamlit** e **SQLite**, com exportação para **CSV** e **PDF**.

---

## 🗂️ Estrutura do Projeto

```
Sales_Analytics/
│
├── app.py               # Ponto de entrada — orquestra todos os módulos
│
├── modules/                 # Pacote Python com a lógica modularizada
│   ├── __init__.py          # Expõe as funções públicas do pacote
│   ├── database.py          # Conexão, inicialização e carregamento de dados (SQLite)
│   ├── sidebar.py           # Barra lateral: banner, filtros e rodapé
│   ├── kpis.py              # Cálculo e renderização dos cards de KPI
│   ├── charts.py            # Todos os gráficos Plotly (linha, pizza, barra, scatter)
│   ├── pdf_report.py        # Geração do relatório executivo em PDF (FPDF)
│   └── theme.py             # Injeção do tema CSS customizado
│
├── database.db          # Banco de dados SQLite (criado automaticamente)
│
├── requirements.txt         # Dependências do projeto
└── README.md                # Este arquivo
```

---

## 📦 Responsabilidade de Cada Módulo

| Módulo | Responsabilidade |
|---|---|
| `app.py` | Orquestrador — configura a página e chama os módulos na ordem correta |
| `database.py` | Cria/conecta ao SQLite, popula dados fictícios e carrega o DataFrame com cache |
| `sidebar.py` | Renderiza o banner, os filtros (data, região, categoria, produto) e aplica a filtragem |
| `kpis.py` | Calcula e exibe os 4 cards de KPI (Receita, Qtd, Ticket Médio, Transações) |
| `charts.py` | Gera os 5 gráficos interativos (linha, pizza, barra regional, barra por dia, scatter) |
| `pdf_report.py` | Monta e exporta o relatório executivo PDF com KPIs e Top 15 vendas |
| `theme.py` | Injeta o CSS customizado (cards, multiselect, pílulas bege-ouro) |

---

## 🚀 Como Executar

### 1. Criar o ambiente virtual (Conda)

```bash
conda create --name miniprojeto python=3.11
```

### 2. Ativar o ambiente

```bash
conda activate miniprojeto 
# ou
source activate miniprojeto 
```

### 3. Instalar as dependências

```bash
conda install pip
pip install -r requirements.txt
```

### 4. Executar o app

```bash
streamlit run app.py
```

---

## 🛑 Desativar / Remover o Ambiente (opcional)

```bash
conda deactivate
conda remove --name miniprojeto --all
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **Python 3.11** | Linguagem principal |
| **Streamlit** | Framework de Data Apps web |
| **SQLite** | Banco de dados local embutido |
| **Pandas** | Manipulação e análise de dados |
| **NumPy** | Geração de dados aleatórios reprodutíveis |
| **Plotly Express** | Gráficos interativos com tema Dark |
| **FPDF2** | Geração de relatórios PDF |

---

## 📊 Funcionalidades do Dashboard

- **Filtros dinâmicos** por período, região, categoria e produto
- **4 Cards de KPI**: Receita Total, Qtd Vendida, Ticket Médio e Nº de Transações
- **5 Gráficos interativos**: Evolução diária, Mix de categorias, Performance regional, Análise por dia da semana e Dispersão
- **Exportação CSV** dos dados filtrados
- **Exportação PDF** com relatório executivo (KPIs + Top 15 vendas)
- **Cache de 10 minutos** para carregamento eficiente dos dados

