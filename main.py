import pandas as pd
import tkinter as tk
import random
import sqlite3
import os
import subprocess
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Função para gerar um jogo de 15 números aleatórios entre 1 e 25
def gerar_jogo():
    return sorted(random.sample(range(1, 26), 15))

# Função para salvar o jogo no banco de dados SQLite
def salvar_jogo(jogo):
    conn = sqlite3.connect('JogosGerados.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            n1 INTEGER, n2 INTEGER, n3 INTEGER, n4 INTEGER, n5 INTEGER,
            n6 INTEGER, n7 INTEGER, n8 INTEGER, n9 INTEGER, n10 INTEGER,
            n11 INTEGER, n12 INTEGER, n13 INTEGER, n14 INTEGER, n15 INTEGER
        )
    ''')

    c.execute('''
        INSERT INTO jogos (n1, n2, n3, n4, n5, n6, n7, n8, n9, n10,
                           n11, n12, n13, n14, n15)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(jogo))

    jogo_id = c.lastrowid
    conn.commit()
    conn.close()
    return jogo_id

# Função para mostrar o jogo na interface
def mostrar_jogo():
    jogo = gerar_jogo()
    jogo_id = salvar_jogo(jogo)
    resultado_label.config(text=f"Jogo nº {jogo_id}: {jogo}")
    atualizar_lista_jogos()

# Função para fazer commit e push para o GitHub
def atualizar_git():
    try:
        repo_dir = r'E:\ProjetoLOTOFACIL'
        os.chdir(repo_dir)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Atualização automática'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("Alterações enviadas ao GitHub com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando Git: {e}")

# Função chamada ao fechar a janela
def on_close():
    atualizar_git()
    root.destroy()

# Função para importar dados do Excel e salvar no banco SQLite
def importar_excel_para_sqlite(arquivo_excel, indices_remover, nome_tabela='dados_importados'):
    df = pd.read_excel(arquivo_excel, sheet_name='LOTOFÁCIL', skiprows=1)
    df = df.drop(df.columns[indices_remover], axis=1)
    engine = create_engine('sqlite:///Importados.db')
    df.to_sql(nome_tabela, con=engine, if_exists='replace', index=False)
    print("Importação concluída com sucesso!")

# Função para atualizar a lista de jogos na interface
def atualizar_lista_jogos():
    conn = sqlite3.connect('JogosGerados.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jogos ORDER BY id DESC LIMIT 101")
    jogos = c.fetchall()
    conn.close()

    listbox_jogos.delete(0, tk.END)
    for jogo in jogos:
        listbox_jogos.insert(tk.END, f"Jogo {jogo[0]}: {jogo[1:]}")
    canvas.config(scrollregion=canvas.bbox("all"))

# Função para verificar ímpares vs pares e mostrar na interface
def verificar_impares_versus_pares_inicial():
    conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_importados")
    resultados = cursor.fetchall()

    mais_impares, mais_pares = 0, 0
    for linha in resultados:
        numeros = linha[1:]
        qtd_impares = sum(1 for n in numeros if n % 2 != 0)
        qtd_pares = len(numeros) - qtd_impares
        if qtd_impares > qtd_pares:
            mais_impares += 1
        elif qtd_pares > qtd_impares:
            mais_pares += 1

    estatisticas_label.config(
        text=f"Mais ímpares: {mais_impares}\nMais pares: {mais_pares}")
    conn.close()

# Função para mostrar gráfico de distribuição por faixas numéricas
def distribuicao_por_faixas():
    conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_importados")
    resultados = cursor.fetchall()
    conn.close()

    faixas = {'1-5': 0, '6-10': 0, '11-15': 0, '16-20': 0, '21-25': 0}

    for linha in resultados:
        numeros = linha[1:]
        for n in numeros:
            if 1 <= n <= 5:
                faixas['1-5'] += 1
            elif 6 <= n <= 10:
                faixas['6-10'] += 1
            elif 11 <= n <= 15:
                faixas['11-15'] += 1
            elif 16 <= n <= 20:
                faixas['16-20'] += 1
            elif 21 <= n <= 25:
                faixas['21-25'] += 1

    plt.bar(faixas.keys(), faixas.values(), color='skyblue')
    plt.title("Distribuição por Faixas Numéricas")
    plt.xlabel("Faixas")
    plt.ylabel("Quantidade de Números Sorteados")
    plt.show()

# ========== INTERFACE TKINTER ========== #

root = tk.Tk()
root.title("Gerador de Jogos Lotofácil")
root.geometry("1100x650")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

frame_esquerdo = tk.Frame(frame)
frame_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=10)

frame_direito = tk.Frame(frame, width=400, height=600)
frame_direito.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

canvas = tk.Canvas(frame_direito)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(canvas)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_jogos = tk.Listbox(canvas, width=55, height=25, yscrollcommand=scrollbar.set)
listbox_jogos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_jogos.yview)

gerar_btn = tk.Button(frame_esquerdo, text="Gerar Jogo", command=mostrar_jogo)
gerar_btn.pack(pady=10)

resultado_label = tk.Label(frame_esquerdo, text="Clique para gerar um jogo.")
resultado_label.pack(pady=10)

frame_estatisticas = tk.Frame(frame_esquerdo)
frame_estatisticas.pack(pady=20)

estatisticas_label = tk.Label(frame_estatisticas, text="Carregando estatísticas...")
estatisticas_label.pack(pady=5)

faixas_btn = tk.Button(frame_estatisticas, text="Distribuição por Faixas Numéricas", command=distribuicao_por_faixas)
faixas_btn.pack(pady=5)

# Importação de Excel e atualização da lista
arquivo_excel = r"E:\ProjetoLOTOFACIL\Resultados.xlsx"
indices_remover = [1, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
importar_excel_para_sqlite(arquivo_excel, indices_remover)

atualizar_lista_jogos()
verificar_impares_versus_pares_inicial()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
