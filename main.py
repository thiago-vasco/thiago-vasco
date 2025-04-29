import tkinter as tk
import random
import sqlite3

# Função para gerar um jogo de 15 números aleatórios entre 1 e 25
def gerar_jogo():
    return sorted(random.sample(range(1, 26), 15))

# Função para salvar o jogo no banco de dados SQLite
def salvar_jogo(jogo):
    # Conecta ou cria o banco de dados
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Cria a tabela se não existir
    c.execute('''
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numeros TEXT
        )
    ''')

    # Insere o jogo na tabela
    c.execute('INSERT INTO jogos (numeros) VALUES (?)', (str(jogo),))

    # Salva as alterações e fecha a conexão
    conn.commit()
    conn.close()

# Função para gerar e mostrar o jogo na interface
def mostrar_jogo():
    jogo = gerar_jogo()
    resultado_label.config(text="Jogo gerado: " + str(jogo))
    salvar_jogo(jogo)

# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Gerador de Jogos Lotofácil")

# Botão para gerar jogo
gerar_btn = tk.Button(root, text="Gerar Jogo", command=mostrar_jogo)
gerar_btn.pack(pady=10)

# Label para exibir o resultado
resultado_label = tk.Label(root, text="Clique para gerar um jogo.")
resultado_label.pack(pady=10)

# Inicia a interface
root.mainloop()