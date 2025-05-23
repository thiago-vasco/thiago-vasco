import pandas as pd
import tkinter as tk
import random
import sqlite3
import os
import subprocess
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

def gerar_jogo():
    # Gerar um jogo com a quantidade de números ímpares selecionada nos checkboxes
    impares_selecionados = [i for i in range(3, 14) if var_impares[i-3].get()]
    if not impares_selecionados:
        resultado_label.config(text="Selecione pelo menos uma quantidade de ímpares.")
        return
    
    # Sortear a quantidade de números ímpares de acordo com o que foi marcado
    qtd_impares = random.choice(impares_selecionados)
    qtd_pares = 15 - qtd_impares

    numeros_impares = [n for n in range(1, 26) if n % 2 != 0]
    numeros_pares = [n for n in range(1, 26) if n % 2 == 0]
    
    jogo_impares = random.sample(numeros_impares, qtd_impares)
    jogo_pares = random.sample(numeros_pares, qtd_pares)
    
    jogo = sorted(jogo_impares + jogo_pares)
    
    jogo_id = salvar_jogo(jogo)
    resultado_label.config(text=f"Jogo nº {jogo_id}: {jogo}")
    atualizar_lista_jogos()

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

    contagem_todos = {i: 0 for i in range(3, 14)}
    contagem_ultimos_500 = {i: 0 for i in range(3, 14)}

    # Contagem de ímpares para todos os jogos
    for linha in resultados:
        numeros = linha[1:]
        qtd_impares = sum(1 for n in numeros if n % 2 != 0)
        if 3 <= qtd_impares <= 13:
            contagem_todos[qtd_impares] += 1

    # Contagem de ímpares para os últimos 500 jogos
    conn = sqlite3.connect('JogosGerados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jogos ORDER BY id DESC LIMIT 500")
    jogos_ultimos_500 = cursor.fetchall()
    conn.close()

    for jogo in jogos_ultimos_500:
        numeros = jogo[1:]
        qtd_impares = sum(1 for n in numeros if n % 2 != 0)
        if 3 <= qtd_impares <= 13:
            contagem_ultimos_500[qtd_impares] += 1

    # Gráfico para todos os jogos
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(contagem_todos.keys(), contagem_todos.values(), color='mediumvioletred', alpha=0.6, label='Todos os Jogos')

    # Gráfico para os últimos 500 jogos
    ax.bar(contagem_ultimos_500.keys(), contagem_ultimos_500.values(), color='dodgerblue', alpha=0.6, label='Últimos 500 Jogos')

    ax.set_xlabel('Quantidade de Números Ímpares no Sorteio')
    ax.set_ylabel('Quantidade de Sorteios')
    ax.set_title('Distribuição de Ímpares por Sorteio (Lotofácil)')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.set_xticks(range(3, 14))
    ax.set_ylim(0, max(max(contagem_todos.values()), max(contagem_ultimos_500.values())) + 30)

    # Adiciona as legendas
    ax.legend()

    for i in contagem_todos:
        ax.text(i, contagem_todos[i] + 2, str(contagem_todos[i]), ha='center', fontsize=8)

    for i in contagem_ultimos_500:
        ax.text(i, contagem_ultimos_500[i] + 2, str(contagem_ultimos_500[i]), ha='center', fontsize=8)

    plt.tight_layout()
    plt.show()


def contar_quantidade_primos():
    primos = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_importados")
    resultados = cursor.fetchall()
    conn.close()

    contagem_todos = {i: 0 for i in range(3, 14)}
    contagem_ultimos_500 = {i: 0 for i in range(3, 14)}

    # Contagem de primos para todos os jogos
    for linha in resultados:
        numeros = linha[1:]
        qtd_primos = sum(1 for n in numeros if n in primos)
        if 3 <= qtd_primos <= 13:
            contagem_todos[qtd_primos] += 1

    # Contagem de primos para os últimos 500 jogos
    conn = sqlite3.connect('JogosGerados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jogos ORDER BY id DESC LIMIT 500")
    jogos_ultimos_500 = cursor.fetchall()
    conn.close()

    for jogo in jogos_ultimos_500:
        numeros = jogo[1:]
        qtd_primos = sum(1 for n in numeros if n in primos)
        if 3 <= qtd_primos <= 13:
            contagem_ultimos_500[qtd_primos] += 1

    # Gráfico para todos os jogos
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(contagem_todos.keys(), contagem_todos.values(), color='royalblue', alpha=0.6, label='Todos os Jogos')

    # Gráfico para os últimos 500 jogos
    ax.bar(contagem_ultimos_500.keys(), contagem_ultimos_500.values(), color='tomato', alpha=0.6, label='Últimos 500 Jogos')

    ax.set_xlabel('Quantidade de Números Primos no Sorteio')
    ax.set_ylabel('Quantidade de Sorteios')
    ax.set_title('Distribuição de Primos por Sorteio (Lotofácil)')
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    ax.set_xticks(range(3, 14))
    ax.set_ylim(0, max(max(contagem_todos.values()), max(contagem_ultimos_500.values())) + 30)

    # Adiciona as legendas
    ax.legend()

    for i in contagem_todos:
        ax.text(i, contagem_todos[i] + 2, str(contagem_todos[i]), ha='center', fontsize=8)

    for i in contagem_ultimos_500:
        ax.text(i, contagem_ultimos_500[i] + 2, str(contagem_ultimos_500[i]), ha='center', fontsize=8)

    plt.tight_layout()
    plt.show()


def distribuicao_faixas_numericas():
    import matplotlib.pyplot as plt
    import sqlite3
    plt.close('all')  # Fecha todos os gráficos abertos

    conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_importados")
    resultados = cursor.fetchall()
    conn.close()

    # Faixas numéricas
    faixas = {
        '1-5': 0,
        '6-10': 0,
        '11-15': 0,
        '16-20': 0,
        '21-25': 0
    }
    
    faixas_ultimos_500 = {
        '1-5': 0,
        '6-10': 0,
        '11-15': 0,
        '16-20': 0,
        '21-25': 0
    }

    # Para todos os resultados
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

    # Para os últimos 500 resultados
    total_resultados = len(resultados)
    ultimos_500_resultados = resultados[-500:] if total_resultados >= 500 else resultados
    for linha in ultimos_500_resultados:
        numeros = linha[1:]
        for n in numeros:
            if 1 <= n <= 5:
                faixas_ultimos_500['1-5'] += 1
            elif 6 <= n <= 10:
                faixas_ultimos_500['6-10'] += 1
            elif 11 <= n <= 15:
                faixas_ultimos_500['11-15'] += 1
            elif 16 <= n <= 20:
                faixas_ultimos_500['16-20'] += 1
            elif 21 <= n <= 25:
                faixas_ultimos_500['21-25'] += 1

    # Criar a figura e os dois subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Gráfico 1: Distribuição de Faixas (Todos os sorteios)
    ax1.bar(faixas.keys(), faixas.values(), color='seagreen', label='Todos os sorteios')
    ax1.set_xlabel('Faixas Numéricas')
    ax1.set_ylabel('Quantidade de Números Sorteados')
    ax1.set_title('Distribuição Numérica - Todos os Sorteios')
    ax1.grid(axis='y', linestyle='--', alpha=0.6)
    ax1.set_ylim(10000, 10500)
    ax1.legend()

    # Adicionando números sobre as barras
    for i, (faixa, count) in enumerate(faixas.items()):
        ax1.text(i, count + 10, str(count), ha='center', fontsize=10)

    # Gráfico 2: Distribuição de Faixas (Últimos 500 sorteios)
    ax2.bar(faixas_ultimos_500.keys(), faixas_ultimos_500.values(), color='royalblue', label='Últimos 500 sorteios')
    ax2.set_xlabel('Faixas Numéricas')
    ax2.set_ylabel('Quantidade de Números Sorteados')
    ax2.set_title('Distribuição Numérica - Últimos 500 Sorteios')
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    ax2.set_ylim(1000, 2000)  # Definindo a escala do gráfico
    ax2.legend()

    # Adicionando números sobre as barras
    for i, (faixa, count) in enumerate(faixas_ultimos_500.items()):
        ax2.text(i, count + 10, str(count), ha='center', fontsize=10)
    plt.tight_layout()
    plt.show()


def grafico_frequencia_numeros():
    import matplotlib.pyplot as plt
    import sqlite3
    plt.close('all')  # Fecha todos os gráficos abertos

    conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados_importados")
    resultados = cursor.fetchall()
    conn.close()

    numeros = list(range(1, 26))
    frequencia_todos = {n: 0 for n in numeros}
    frequencia_ultimos_500 = {n: 0 for n in numeros}

    total_resultados = len(resultados)
    ultimos_500_resultados = resultados[-500:] if total_resultados >= 500 else resultados

    for linha in resultados:
        numeros_sorteio = linha[1:]
        for n in numeros_sorteio:
            frequencia_todos[n] += 1

    for linha in ultimos_500_resultados:
        numeros_sorteio = linha[1:]
        for n in numeros_sorteio:
            frequencia_ultimos_500[n] += 1

    # Criar a figura e os dois subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Gráfico 1: todos vs últimos 500 (escala normal)
    ax1.bar([n - 0.2 for n in numeros], [frequencia_todos[n] for n in numeros], width=0.4, label='Todos os sorteios', color='mediumvioletred')
    ax1.bar([n + 0.2 for n in numeros], [frequencia_ultimos_500[n] for n in numeros], width=0.4, label='Últimos 500 sorteios', color='royalblue')

    ax1.set_xlabel('Número')
    ax1.set_ylabel('Número de jogos')
    ax1.set_title('Frequência de cada número - Todos os sorteios')
    ax1.set_xticks(numeros)
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.6)

    max_valor_todos = max(frequencia_todos.values())
    ax1.set_ylim(1900, max_valor_todos + 20)

    for n in numeros:
        v_todos = frequencia_todos[n]
        v_ultimos = frequencia_ultimos_500[n]
        ax1.text(n - 0.2, v_todos + 2, str(v_todos), ha='center', fontsize=8)
        ax1.text(n + 0.2, v_ultimos + 2, str(v_ultimos), ha='center', fontsize=8)

    # Gráfico 2: últimos 500 com escala 250–350
    ax2.bar(numeros, [frequencia_ultimos_500[n] for n in numeros], width=0.5, color='royalblue')

    ax2.set_xlabel('Número')
    ax2.set_ylabel('Número de jogos')
    ax2.set_title('Frequência de cada número - Últimos 500 sorteios')
    ax2.set_xticks(numeros)
    ax2.grid(axis='y', linestyle='--', alpha=0.6)
    ax2.set_ylim(250, 350)

    for n in numeros:
        v_ultimos = frequencia_ultimos_500[n]
        ax2.text(n, v_ultimos + 1, str(v_ultimos), ha='center', fontsize=8)

    plt.tight_layout()
    plt.show()



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

# Checkbox dos ímpares
var_impares = []
checkbox_frame = tk.Frame(frame_esquerdo)
checkbox_frame.pack(pady=10)

colunas_por_linha = 5

for idx, i in enumerate(range(3, 14)):
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(checkbox_frame, text=f'{i} ímpares', variable=var)
    
    # Calcula linha e coluna
    row = idx // colunas_por_linha
    col = idx % colunas_por_linha
    
    checkbox.grid(row=row, column=col, padx=5, pady=2, sticky="w")
    var_impares.append(var)

gerar_btn = tk.Button(frame_esquerdo, text="Gerar Jogo", command=mostrar_jogo)
gerar_btn.pack(pady=10)

resultado_label = tk.Label(frame_esquerdo, text="Clique para gerar um jogo.")
resultado_label.pack(pady=10)

# Botões para mostrar gráficos
grafico_impares_btn = tk.Button(frame_esquerdo, text="Gráfico de Ímpares", command=contar_quantidade_impares)
grafico_impares_btn.pack(pady=10)

grafico_primos_btn = tk.Button(frame_esquerdo, text="Gráfico de Primos", command=contar_quantidade_primos)
grafico_primos_btn.pack(pady=10)

grafico_faixas_btn = tk.Button(frame_esquerdo, text="Gráfico Distribuição Numérica", command=distribuicao_faixas_numericas)
grafico_faixas_btn.pack(pady=10)

grafico_frequencia_btn = tk.Button(frame_esquerdo, text="Gráfico Frequência Números", command=grafico_frequencia_numeros)
grafico_frequencia_btn.pack(pady=10)

# Janela inicia sem jogos carregados
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()