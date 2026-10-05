import sqlite3
import pandas as pd
import re
import os

DB_FILE = "empresa.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

def sanitize_column_name(col: str) -> str:
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

def init_db():
    conn = get_connection()
    conn.close()

def load_df_to_sqlite(df: pd.DataFrame, table_name: str = "dados_usuario"):
    df.columns = [sanitize_column_name(c) for c in df.columns]
    conn = get_connection()
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def get_database_schema() -> str:
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    conn.close()
    
    if not tables:
        return "-- Nenhum dado carregado. Envie um arquivo CSV ou Excel na barra lateral."
        
    schema_lines = []
    for table_name, create_sql in tables:
        if create_sql:
            schema_lines.append(f"-- Tabela: {table_name}\n{create_sql};")
            
    return "\n\n".join(schema_lines)

def run_query(sql_query: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df

def reset_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()
    for table_name in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]};")
    conn.commit()
    conn.close()