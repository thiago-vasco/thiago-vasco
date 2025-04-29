import tkinter as tk
import random
import sqlite3
import os
import subprocess

# Função para gerar um jogo de 15 números aleatórios entre 1 e 25
def gerar_jogo():
    return sorted(random.sample(range(1, 26), 15))

# Função para salvar o jogo no banco de dados SQLite
def salvar_jogo(jogo):
    conn = sqlite3.connect('JogosGerados.db')
    c = conn.cursor()

    # Cria a tabela se não existir, com 15 colunas (n1 a n15)
    c.execute('''
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            n1 INTEGER,
            n2 INTEGER,
            n3 INTEGER,
            n4 INTEGER,
            n5 INTEGER,
            n6 INTEGER,
            n7 INTEGER,
            n8 INTEGER,
            n9 INTEGER,
            n10 INTEGER,
            n11 INTEGER,
            n12 INTEGER,
            n13 INTEGER,
            n14 INTEGER,
            n15 INTEGER
        )
    ''')

    # Insere os números nas colunas correspondentes
    c.execute('''
        INSERT INTO jogos (n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(jogo))

    conn.commit()
    conn.close()

# Função para gerar e mostrar o jogo na interface
def mostrar_jogo():
    jogo = gerar_jogo()
    resultado_label.config(text="Jogo gerado: " + str(jogo))
    salvar_jogo(jogo)

# Função para fazer commit e push para o GitHub
def atualizar_git():
    try:
        # Caminho onde seu repositório Git está localizado
        repo_dir = r'E:\ProjetoLOTOFACIL'  # Substitua com o caminho correto do seu repositório local
        os.chdir(repo_dir)  # Altera para o diretório do repositório
        
        # Executa os comandos Git
        subprocess.run(['git', 'add', '.'], check=True)  # Adiciona todas as mudanças
        subprocess.run(['git', 'commit', '-m', 'Atualização automática'], check=True)  # Faz o commit
        subprocess.run(['git', 'push'], check=True)  # Faz o push para o GitHub
        print("Alterações enviadas ao GitHub com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando Git: {e}")

# Função que será chamada quando a janela for fechada
def on_close():
    atualizar_git()  # Atualiza o Git ao fechar a janela
    root.destroy()   # Fecha a janela

# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Gerador de Jogos Lotofácil")

# Botão para gerar jogo
gerar_btn = tk.Button(root, text="Gerar Jogo", command=mostrar_jogo)
gerar_btn.pack(pady=10)

# Label para exibir o resultado
resultado_label = tk.Label(root, text="Clique para gerar um jogo.")
resultado_label.pack(pady=10)

# Configura o evento de fechamento da janela
root.protocol("WM_DELETE_WINDOW", on_close)

# Inicia a interface
root.mainloop()
