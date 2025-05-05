import pandas as pd
import tkinter as tk
import random
import sqlite3
import os
import subprocess
from sqlalchemy import create_engine
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

def mostrar_jogo():
    jogo = gerar_jogo()
    jogo_id = salvar_jogo(jogo)
    resultado_label.config(text=f"Jogo nº {jogo_id}: {jogo}")
    atualizar_lista_jogos()

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

def on_close():
    atualizar_git()
    root.destroy()

def importar_excel_para_sqlite(arquivo_excel, indices_remover, nome_tabela='dados_importados'):
    df = pd.read_excel(arquivo_excel, sheet_name='LOTOFÁCIL', skiprows=1)
    df = df.drop(df.columns[indices_remover], axis=1)
    engine = create_engine('sqlite:///Importados.db')
    df.to_sql(nome_tabela, con=engine, if_exists='replace', index=False)
    print("Importação de dados concluída com sucesso!")

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

def contar_quantidade_impares():
    conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_importados")
    resultados = cursor.fetchall()
    conn.close()

    contagem = {i: 0 for i in range(3, 14)}

    for linha in resultados:
        numeros = linha[1:]
        qtd_impares = sum(1 for n in numeros if n % 2 != 0)
        if 3 <= qtd_impares <= 13:
            contagem[qtd_impares] += 1

    # Gera gráfico de barras
    fig, ax = plt.subplots(figsize=(7, 4))  # aumenta o tamanho
    ax.bar(contagem.keys(), contagem.values(), color='purple')
    ax.set_xlabel('Quantidade de Números Ímpares no Sorteio')
    ax.set_ylabel('Quantidade de Sorteios')
    ax.set_title('Distribuição de Ímpares por Sorteio (Lotofácil)')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.set_xticks(range(3, 14))
    ax.set_ylim(0, max(contagem.values()) + 30)  # aumenta escala vertical

    for i in contagem:
        ax.text(i, contagem[i] + 2, str(contagem[i]), ha='center', fontsize=8)

    # Coloca o gráfico na interface
    canvas_grafico = FigureCanvasTkAgg(fig, master=frame_esquerdo)
    canvas_grafico.draw()
    canvas_grafico.get_tk_widget().pack(pady=10)

# Caminho do arquivo Excel e índices das colunas a serem removidas
arquivo_excel = r"E:\ProjetoLOTOFACIL\Resultados.xlsx"
indices_remover = [1, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

# Importa dados do Excel para o banco Importados.db
importar_excel_para_sqlite(arquivo_excel, indices_remover)

# Interface gráfica
root = tk.Tk()
root.title("Gerador de Jogos Lotofácil")
root.geometry("1200x700")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

frame_esquerdo = tk.Frame(frame)
frame_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=10)

frame_direito = tk.Frame(frame, width=300, height=600)
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

# Atualiza lista de jogos
# atualizar_lista_jogos()

# Gera gráfico ao carregar
contar_quantidade_impares()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
