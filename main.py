import pandas as pd
import tkinter as tk
import random
import sqlite3
import os
import subprocess
from sqlalchemy import create_engine

# Função para gerar um jogo de 15 números aleatórios entre 1 e 25
def gerar_jogo():
    return sorted(random.sample(range(1, 26), 15))

# Função para salvar o jogo no banco de dados SQLite e retornar o ID
def salvar_jogo(jogo):
    conn = sqlite3.connect('JogosGerados.db')
    c = conn.cursor()

    # Cria a tabela se não existir
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            n1 INTEGER, n2 INTEGER, n3 INTEGER, n4 INTEGER, n5 INTEGER,
            n6 INTEGER, n7 INTEGER, n8 INTEGER, n9 INTEGER, n10 INTEGER,
            n11 INTEGER, n12 INTEGER, n13 INTEGER, n14 INTEGER, n15 INTEGER
        )
    ''')

    # Insere os números
    c.execute(''' 
        INSERT INTO jogos (n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(jogo))

    jogo_id = c.lastrowid  # captura o ID do jogo salvo

    conn.commit()
    conn.close()

    return jogo_id  # retorna o id

# Função para gerar e mostrar o jogo na interface
def mostrar_jogo():
    jogo = gerar_jogo()
    jogo_id = salvar_jogo(jogo)  # captura o id retornado
    resultado_label.config(text=f"Jogo nº {jogo_id}: {jogo}")
    atualizar_lista_jogos()

# Função para fazer commit e push para o GitHub
def atualizar_git():
    try:
        repo_dir = r'E:\ProjetoLOTOFACIL'  # Caminho do repositório local
        os.chdir(repo_dir)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Atualização automática'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("Alterações enviadas ao GitHub com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando Git: {e}")

# Função que será chamada ao fechar a janela
def on_close():
    atualizar_git()
    root.destroy()

# Função para importar dados do Excel e salvar no SQLite
def importar_excel_para_sqlite(arquivo_excel, indices_remover, nome_tabela='dados_importados'):
    df = pd.read_excel(arquivo_excel, sheet_name='LOTOFÁCIL')
    print("Colunas no DataFrame:", df.columns)
    df = df.drop(df.columns[indices_remover], axis=1)
    engine = create_engine('sqlite:///Importados.db')
    df.to_sql(nome_tabela, con=engine, if_exists='replace', index=False)
    print("Importação de dados concluída com sucesso!")

# Função para atualizar a lista de jogos na interface
def atualizar_lista_jogos():
    conn = sqlite3.connect('JogosGerados.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jogos ORDER BY id DESC")  # Pega todos os jogos em ordem decrescente
    jogos = c.fetchall()
    conn.close()

    listbox_jogos.delete(0, tk.END)

    for jogo in jogos:
        listbox_jogos.insert(tk.END, f"Jogo {jogo[0]}: {jogo[1:]}")

# Caminho do Excel e colunas a remover
arquivo_excel = r"E:\ProjetoLOTOFACIL\Resultados.xlsx"
indices_remover = [1, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

# Importa dados do Excel para o SQLite
importar_excel_para_sqlite(arquivo_excel, indices_remover)

# Criação da interface com Tkinter
root = tk.Tk()
root.title("Gerador de Jogos Lotofácil")

# Define tamanho fixo da janela
root.geometry("1000x600")

# Frame principal
frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Frame esquerdo (botão e label)
frame_esquerdo = tk.Frame(frame)
frame_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# Frame direito (lista de jogos)
frame_direito = tk.Frame(frame, width=300, height=600)
frame_direito.pack_propagate(False)
frame_direito.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

# Botão de gerar jogo
gerar_btn = tk.Button(frame_esquerdo, text="Gerar Jogo", command=mostrar_jogo)
gerar_btn.pack(pady=10)

# Label de resultado
resultado_label = tk.Label(frame_esquerdo, text="Clique para gerar um jogo.")
resultado_label.pack(pady=10)

# Listbox para exibir jogos gerados
listbox_jogos = tk.Listbox(frame_direito, width=55, height=25)
listbox_jogos.pack(side=tk.LEFT, fill=tk.Y)

# Scrollbar vertical associada à Listbox
scrollbar = tk.Scrollbar(frame_direito, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configura o scrollbar para a Listbox
listbox_jogos.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_jogos.yview)

# Atualiza lista de jogos no início
atualizar_lista_jogos()

# Configura o evento de fechamento da janela
root.protocol("WM_DELETE_WINDOW", on_close)

# Inicia a interface
root.mainloop()
