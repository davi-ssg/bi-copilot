import pandas as pd
import random
from datetime import datetime, timedelta

# Listas de dados para combinação aleatória
clientes = [
    'Lucas Silva', 'Mariana Oliveira', 'Pedro Santos', 'Beatriz Lima', 
    'Gabriel Souza', 'Fernanda Rocha', 'Rodrigo Alves', 'Camila Martins',
    'Rafael Costa', 'Juliana Mendes', 'Thiago Ribeiro', 'Aline Barbosa'
]

produtos_cat = {
    'Eletrônicos': [('Notebook Pro', 4500.00), ('Smartphone X', 2800.00), ('Monitor 27', 1500.00), ('Tablet Air', 2200.00)],
    'Acessórios': [('Mouse Sem Fio', 120.00), ('Teclado Mecânico', 350.00), ('Headset Gamer', 400.00), ('Carregador Fast', 90.00)],
    'Móveis': [('Cadeira Ergonômica', 1100.00), ('Mesa Stand-Desk', 1800.00), ('Luminária LED', 150.00)],
    'Vestuário': [('Camiseta Tech', 80.00), ('Jaqueta Impermeável', 350.00), ('Tênis Confort', 290.00)]
}

cidades = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre', 'Salvador', 'Brasília']
status_opcoes = ['Concluído', 'Concluído', 'Concluído', 'Pendente', 'Cancelado']

data_inicial = datetime(2026, 1, 1)

dados = []
for i in range(1, 201): # Gerar 200 linhas
    categoria = random.choice(list(produtos_cat.keys()))
    produto, preco_base = random.choice(produtos_cat[categoria])
    quantidade = random.randint(1, 5)
    valor_total = round(preco_base * quantidade, 2)
    data_venda = (data_inicial + timedelta(days=random.randint(0, 260))).strftime('%Y-%m-%d')
    
    dados.append({
        'id_venda': 1000 + i,
        'data_venda': data_venda,
        'cliente': random.choice(clientes),
        'cidade': random.choice(cidades),
        'categoria': categoria,
        'produto': produto,
        'quantidade': quantidade,
        'valor_unitario': preco_base,
        'valor_total': valor_total,
        'status': random.choice(status_opcoes)
    })

# Cria DataFrame e salva como CSV
df = pd.DataFrame(dados)
df.to_csv('vendas_ficticias.csv', index=False, encoding='utf-8-sig')
print("✅ Arquivo 'vendas_ficticias.csv' gerado com sucesso com 200 registros!")