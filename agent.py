import google.generativeai as genai
import re
import os
from dotenv import load_dotenv
import pandas as pd
from database import get_database_schema, run_query

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def clean_sql_query(sql: str) -> str:
    """Remove marcações de markdown ```sql ... ``` que o Gemini possa retornar."""
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    return sql.strip()

def run_bi_agent(user_prompt: str) -> dict:
    """
    Executa a pipeline do Agente BI com limite estrito de 2 tentativas
    para evitar travamentos infinitos.
    """
    schema = get_database_schema()
    
    if not schema or "-- Nenhum dado" in schema:
        return {
            "status": "error",
            "response": "Nenhuma tabela foi encontrada no banco de dados. Carregue um arquivo primeiro."
        }

    # Prompt do Sistema
    system_prompt = f"""
    Você é um assistente especialista em SQL e Business Intelligence (BI).
    
    ESTRUTURA DO BANCO DE DADOS (SQLite):
    {schema}
    
    REGRAS ESTRITAS:
    1. Retorne APENAS a instrução SQL válida do tipo SELECT dentro do bloco ```sql ... ```.
    2. NÃO inclua nenhum texto antes ou depois da query SQL na primeira resposta.
    3. Use nomes de tabelas e colunas EXATAMENTE como estão no esquema acima.
    4. Limite o resultado a 500 linhas se a consulta for muito ampla.
    """

    model = genai.GenerativeModel('gemini-3.5-flash-lite')
    
    max_retries = 2
    attempts = 0
    last_error = ""

    while attempts < max_retries:
        attempts += 1
        try:
            # 1. Solicita a query SQL ao Gemini
            prompt_sql = f"{system_prompt}\n\nPergunta do usuário: {user_prompt}"
            if last_error:
                prompt_sql += f"\n\nATENÇÃO: A tentativa anterior falhou com o erro: {last_error}. Corrija o SQL."

            response_sql = model.generate_content(
                prompt_sql,
                request_options={"timeout": 15}  # Timeout de 15 segundos para não travar
            )
            
            raw_sql = response_sql.text
            clean_sql = clean_sql_query(raw_sql)

            # 2. Executa a query no SQLite
            df_result = run_query(clean_sql)

            # 3. Solicita a explicação final em linguagem natural
            prompt_analysis = f"""
            Com base na pergunta do usuário e no resultado dos dados abaixo, faça uma análise resumida, clara e profissional.
            
            Pergunta: {user_prompt}
            Consulta SQL executada: {clean_sql}
            Dados retornados ({len(df_result)} linhas):
            {df_result.head(10).to_string()}
            """

            response_analysis = model.generate_content(
                prompt_analysis,
                request_options={"timeout": 15}
            )

            return {
                "status": "success",
                "response": response_analysis.text,
                "sql_used": clean_sql,
                "raw_data": df_result.to_dict(orient="records")
            }

        except Exception as e:
            last_error = str(e)
            print(f"[Agente BI] Tentativa {attempts} falhou: {last_error}")

    # Se esgotar as tentativas
    return {
        "status": "error",
        "response": f"Não foi possível processar a consulta. Ocorreu um erro recorrente: {last_error}"
    }