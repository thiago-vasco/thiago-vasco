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

    jogo_id = c.lastrowid  # pega o ID gerado

    conn.commit()
    conn.close()

    return jogo_id  # retorna o ID


# Função para gerar e mostrar o jogo na interface
def mostrar_jogo():
    jogo = gerar_jogo()
    jogo_id = salvar_jogo(jogo)  # salva e pega o ID
    resultado_label.config(text=f"Jogo nº {jogo_id}: {jogo}")
    atualizar_lista_jogos()
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

# Função para importar dados do Excel, remover colunas pelo índice e salvar no banco SQLite
def importar_excel_para_sqlite(arquivo_excel, indices_remover, nome_tabela='dados_importados'):
    # Ler a planilha inteira ou por aba
    df = pd.read_excel(arquivo_excel, sheet_name='LOTOFÁCIL', skiprows=1)

    # Verificar as colunas do DataFrame
    print("Colunas no DataFrame:", df.columns)

    # Remover as colunas pelos índices
    df = df.drop(df.columns[indices_remover], axis=1)

    # Criar conexão com banco SQLite (se o banco não existir, ele será criado)
    engine = create_engine('sqlite:///Importados.db')  # 'Importados.db' é o nome do seu arquivo SQLite

    # Exportar para o banco (use 'replace' se você quiser substituir os dados da tabela, ou 'append' para adicionar mais dados)
    df.to_sql(nome_tabela, con=engine, if_exists='replace', index=False)

    print("Importação de dados concluída com sucesso!")

# Função para atualizar a lista de jogos na interface
def atualizar_lista_jogos():
    # Conectar ao banco SQLite para buscar os jogos gerados
    conn = sqlite3.connect('JogosGerados.db')
    c = conn.cursor()
    c.execute("SELECT * FROM jogos ORDER BY id DESC LIMIT 101")  # Pega os últimos 100 jogos gerados, ajuste conforme necessário
    jogos = c.fetchall()
    conn.close()

    # Limpar a lista de jogos atual
    listbox_jogos.delete(0, tk.END)

    # Adicionar os jogos mais recentes à lista
    for jogo in jogos:
        listbox_jogos.insert(tk.END, f"Jogo {jogo[0]}: {jogo[1:]}")

    # Atualizar a região de rolagem do Canvas para o tamanho correto
    canvas.config(scrollregion=canvas.bbox("all"))

# Caminho do arquivo Excel e índices das colunas a serem removidas
arquivo_excel = r"E:\ProjetoLOTOFACIL\Resultados.xlsx"  # Caminho do seu arquivo Excel
# Índices das colunas que você quer remover: 2, 18, 19, 20 até 33 (lembre-se que o índice é baseado em 0)
indices_remover = [0, 1, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

# Importa dados do Excel para o banco Importados.db
importar_excel_para_sqlite(arquivo_excel, indices_remover)

# Criando a interface gráfica com Tkinter
root = tk.Tk()
root.title("Gerador de Jogos Lotofácil")

# Aumentando o tamanho da janela (5x maior)
root.geometry("1000x600")  # 1000x600 pixels para a janela maior

# Criando o Frame para a parte principal da interface
frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Criando o Frame para o lado esquerdo (onde estará o botão)
frame_esquerdo = tk.Frame(frame)
frame_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=10)

# Criando o Frame para o lado direito (onde estará a lista de jogos)
frame_direito = tk.Frame(frame, width=300, height=600)  # Definindo o tamanho fixo do Frame do lado direito
frame_direito.pack(side=tk.RIGHT, padx=10, fill=tk.Y)

# Criando um Canvas para o lado direito
canvas = tk.Canvas(frame_direito)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Criando uma Scrollbar para a Listbox
scrollbar = tk.Scrollbar(canvas)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Criando a Listbox para exibir os jogos gerados (lado direito) com tamanho fixo
listbox_jogos = tk.Listbox(canvas, width=55 , height=25, yscrollcommand=scrollbar.set)  # Tamanho fixo para a Listbox
listbox_jogos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configurando a scrollbar para a Listbox
scrollbar.config(command=listbox_jogos.yview)

# Botão para gerar jogo (lado esquerdo)
gerar_btn = tk.Button(frame_esquerdo, text="Gerar Jogo", command=mostrar_jogo)
gerar_btn.pack(pady=10)

# Label para exibir o resultado (lado esquerdo)
resultado_label = tk.Label(frame_esquerdo, text="Clique para gerar um jogo.")
resultado_label.pack(pady=10)

# Atualizar lista de jogos
atualizar_lista_jogos()

# Configura o evento de fechamento da janela
root.protocol("WM_DELETE_WINDOW", on_close)

# Inicia a interface
root.mainloop()
