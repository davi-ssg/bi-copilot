import sqlite3
import json
from database import DB_FILE

def execute_sql(query: str) -> str:
    """
    Executa uma consulta SQL no banco de dados SQLite e retorna o resultado em JSON.
    
    Args:
        query: Instrução SQL SELECT a ser executada no banco.
    """
    query_clean = query.strip().upper()
    
    if not (query_clean.startswith("SELECT") or query_clean.startswith("WITH")):
        return json.dumps({"error": "Segurança: Apenas consultas SELECT são permitidas."})
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        
        result = [dict(zip(columns, row)) for row in rows]
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"Erro de sintaxe SQL: {str(e)}"})