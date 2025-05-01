import sqlite3

# Conectar ao banco SQLite
conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados.db")  # Substitua pelo caminho correto do seu banco
cursor = conn.cursor()

# Listar todas as tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

# Exibir as tabelas encontradas
print("Tabelas no banco de dados:")
for tabela in tabelas:
    print(tabela[0])

# Fechar a conexão
conn.close()