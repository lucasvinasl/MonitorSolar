# Criar banco de dados a partir de arquivo CSV
import sqlite3 as sql
import pandas as pd

# Nome do arquivo do banco de dados SQLite3
bd_name = "dados_geracao.db"

# Nome do arquivo CSV com os dados
data_csv = "dados.csv"

# Conectar ao banco de dados ou criá-lo se não existir
conn = sql.connect(bd_name)

# Criar a tabela no banco de dados
table_sql = """
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY,
    cliente TEXT,
    inversor TEXT,
    janeiro REAL,
    fevereiro REAL,
    marco REAL,
    abril REAL,
    maio REAL,
    junho REAL,
    julho REAL,
    agosto REAL,
    setembro REAL,
    outubro REAL,
    novembro REAL,
    dezembro REAL,
    esperada REAL
)
"""

conn.execute(table_sql)

# Ler os dados do arquivo CSV usando o pandas
df = pd.read_csv(data_csv, sep=";")

# Inserir os dados do CSV na tabela SQLite
df.to_sql("clientes", conn, if_exists="replace", index=False)

# Confirmar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados criado e alimentado com sucesso.")
