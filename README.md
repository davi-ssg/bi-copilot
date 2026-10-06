# 📊 BI Copilot — Assistente Inteligente de Business Intelligence

O **BI Copilot** é uma aplicação web interativa desenvolvida em Python e Streamlit que transforma perguntas em linguagem natural 
em consultas SQL operacionais e análises visuais avançadas. Permite o carregamento de bases de dados CSV ou Excel, analisa 
autonomamente a estrutura dos dados através da API do **Google Gemini (`gemini-3.5-flash`)**, executa queries num ambiente SQLite 
isolado em memória e gera gráficos interativos com Plotly, além de relatórios executivos estruturados em formato Word (`.docx`).

BI Copilot: https://bi-copilot-dssg.streamlit.app

---

## 🚀 Principais Funcionalidades

- 📁 **Carregamento Flexível de Dados:** Suporte a ficheiros `.csv` e `.xlsx` com sanitização e normalização automática de colunas (remoção de acentos, caracteres especiais e espaços).
- 🔒 **Isolamento de Dados por Sessão:** Arquitetura *stateless* com banco de dados SQLite em memória (`:memory:`) alocado individualmente na `st.session_state` de cada utilizador, garantindo total privacidade e segurança concorrente.
- 🤖 **Agente BI Autónomo:** Conversão inteligente de linguagem natural para SQL com limites estritos de execução (*timeouts* de 15s) e mecanismo de re-tentativa resiliente.
- 📈 **Gráficos Interativos (Plotly Express):** Deteção automática do tipo de dado para renderização de gráficos de linhas (séries temporais), rosca/pizza (categorias reduzidas) ou barras com gradientes.
- 📝 **Exportação de Relatórios Executivos:**
  - **Word (`.docx`):** Documento formatado com cabeçalho corporativo, síntese analítica do Gemini e tabela de dados integrada.
  - **Planilhas (`.csv` / `.xlsx`):** Download direto da tabela filtrada pela consulta SQL.
  - **Análise (`.txt`):** Exportação em texto simples dos insights obtidos.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Interface Web:** [Streamlit](https://streamlit.io/)
- **Modelo de IA:** [Google Gemini API (`gemini-3.5-flash`)](https://ai.google.dev/)
- **Base de Dados:** SQLite (In-Memory per Session)
- **Manipulação de Dados:** Pandas & Openpyxl
- **Visualização de Dados:** Plotly Express
- **Geração de Documentos:** `python-docx`
- **Gestão de Ambiente:** `python-dotenv`

---

## 📂 Estrutura do Projeto

```text
├── app.py              # Interface principal do Streamlit, histórico de chat e renderização gráfica
├── agent.py            # Lógica do Agente Gemini (prompting com esquema, execução SQL e timeout)
├── database.py         # Gestão da conexão SQLite em memória, sanitização de colunas e schema
├── requirements.txt    # Lista de dependências para instalação e deploy
├── .gitignore          # Ficheiros e pastas ignorados pelo Git (.env, caches, etc.)
└── README.md           # Documentação do projeto
