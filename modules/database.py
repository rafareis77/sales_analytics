# modules/database.py
# Módulo responsável pela conexão, inicialização e carregamento so banco de dados SQLite

import sqlite3
from datetime import date, timedelta

import numpy as np
import pandas as pd
import streamlit as st


def cria_conexao(db_path: str="database.db") -> sqlite3.Connection:
    """
    Cria e retorna um objeto de conexão de banco de dados SQLite.

    Parâmetros: 
        db_path (str): Caminho e nome do arquivo .db a ser usado.
                       Padrão: "database.db". Criado automaticamente se inexistente.

    Retorna:
        sqlite3.Connection: Objeto de conexão.
    """

    conn = sqlite3.connect(db_path, check_same_thread=False)

    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """
    Inicializa o banco de dados:
    1. Cria a tabela 'tb_vendas' se não existir.
    2. Verifica se a tabela está vazia.
    3. Se vazia, popula com 180 dias de dados fictícios.

    Parâmetros:
        conn (sqlite3.Connection): Conexão ativa com o banco de dados.
    """

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_vendas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT,
            regiao      TEXT,
            categoria   TEXT,
            produto     TEXT,
            faturamento REAL,
            quantidade  INTEGER
    )
""")
    
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM tb_vendas")
    if cursor.fetchone()[0] == 0:
        _popula_dados_ficticios(conn, cursor)


def _popula_dados_ficticios(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    """
    Privada) Gera e insere 180 dias de dados fictícios de vendas no banco.

    Parâmetros:
        conn   (sqlite3.Connection): Conexão ativa (para commit).
        cursor (sqlite3.Cursor):     Cursor ativo (para executemany).
    """

    np.random.seed(42)
    start_date = date(2026, 1, 1)
    datas = [start_date + timedelta(days=i) for i in range(180)]

    regioes = ["norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"]
    categorias = ["Eletrônicos", "Roupas", "Alimentos", "Serviços"]

    dict_produtos = {
        "Eletrônicos": {"Smartphone": 1200, "Laptop": 3500, "Tablet": 800},
        "Roupas": {"Camiseta": 50, "Terno": 150, "Casaco": 300},
        "Alimentos": {"Congelados": 40, "Bebidas": 15, "Limpeza": 25},
        "Serviços": {"Consultoria": 1000, "Instalação": 400, "Suporte": 200},
    }

    rows = []
    for d in datas:
        vendas_diarias = np.random.randint(5, 15)
        for _ in range(vendas_diarias):
            r = np.random.choice(regioes)
            c = np.random.choice(categorias)
            p = np.random.choice(list(dict_produtos[c].keys()))
            preco_base = dict_produtos[c][p]
            quantidade = np.random.randint(1, 25)
            base_fat = preco_base * quantidade
            noise = np.random.uniform(-0.20, 0.20)
            faturamento = max(0, base_fat * (1 + noise))
            rows.append((d.isoformat(), r, c, p, round(faturamento, 2), quantidade))

    cursor.executemany(
        "INSERT INTO tb_vendas (date, regiao, categoria, produto, faturamento, quantidade)"
        "VALUES (?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()


@st.cache_data(ttl=600)
def carrega_dados() -> pd.DataFrame:
    """
    Carrega todos os dados de vendas em um DataFrame do Pandas.
    Resultado cacheado por 10 minutos via @st.cache_data.

    Retorna:
        pd.DataFrame: Tabela completa de vendas com a coluna 'date' em datetime.
    """
    conn = cria_conexao()
    init_db(conn)
    df = pd.read_sql_query("SELECT * FROM tb_vendas", conn, parse_dates=["date"])
    conn.close()

    return df