import sqlite3
import pandas as pd
import re
import streamlit as st

def get_connection():
    """
    Retorna a conexão SQLite exclusiva da sessão atual do utilizador.
    Se não existir, cria um banco isolado em memória (:memory:).
    """
    if "db_conn" not in st.session_state:
        st.session_state.db_conn = sqlite3.connect(":memory:", check_same_thread=False)
    return st.session_state.db_conn

def init_db():
    """Inicializa a conexão em memória para a sessão atual."""
    get_connection()

def sanitize_column_name(col: str) -> str:
    """Normaliza os nomes das colunas (remove acentos, espaços e caracteres especiais)."""
    col = str(col).strip().lower()
    col = re.sub(r'[áàâã]', 'a', col)
    col = re.sub(r'[éèê]', 'e', col)
    col = re.sub(r'[íì]', 'i', col)
    col = re.sub(r'[óòôõ]', 'o', col)
    col = re.sub(r'[úù]', 'u', col)
    col = re.sub(r'[ç]', 'c', col)
    col = re.sub(r'[^\w\s]', '', col)
    col = re.sub(r'\s+', '_', col)
    return col or "coluna"

def load_df_to_sqlite(df: pd.DataFrame, table_name: str = "dados_usuario"):
    """Sanitiza os nomes das colunas e carrega o DataFrame no banco em memória da sessão."""
    df_clean = df.copy()
    df_clean.columns = [sanitize_column_name(c) for c in df_clean.columns]
    conn = get_connection()
    df_clean.to_sql(table_name, conn, if_exists="replace", index=False)

def get_database_schema() -> str:
    """Extrai o esquema SQL (CREATE TABLE) das tabelas ativas da sessão atual."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    
    if not tables:
        return "-- Nenhum dado carregado. Envie um arquivo CSV ou Excel na barra lateral."
        
    schema_lines = []
    for table_name, create_sql in tables:
        if create_sql:
            schema_lines.append(f"-- Tabela: {table_name}\n{create_sql};")
            
    return "\n\n".join(schema_lines)

def run_query(sql_query: str) -> pd.DataFrame:
    """Executa uma consulta SELECT no banco isolado da sessão."""
    conn = get_connection()
    return pd.read_sql_query(sql_query, conn)

def reset_database():
    """Fecha e remove a conexão em memória da sessão atual."""
    if "db_conn" in st.session_state:
        try:
            st.session_state.db_conn.close()
        except Exception:
            pass
        del st.session_state.db_conn