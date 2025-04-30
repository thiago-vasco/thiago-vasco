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

# Função para importar dados do Excel, remover colunas pelo índice e salvar no banco SQLite
def importar_excel_para_sqlite(arquivo_excel, indices_remover, nome_tabela='dados_importados'):
    # Ler a planilha inteira ou por aba
    df = pd.read_excel(arquivo_excel, sheet_name='LOTOFÁCIL')

    # Verificar as colunas do DataFrame
    print("Colunas no DataFrame:", df.columns)

    # Remover as colunas pelos índices
    df = df.drop(df.columns[indices_remover], axis=1)

    # Criar conexão com banco SQLite (se o banco não existir, ele será criado)
    engine = create_engine('sqlite:///Importados do site da lotérica.db')  # 'Importados.db' é o nome do seu arquivo SQLite

    # Exportar para o banco (use 'replace' se você quiser substituir os dados da tabela, ou 'append' para adicionar mais dados)
    df.to_sql(nome_tabela, con=engine, if_exists='replace', index=False)

    print("Importação de dados concluída com sucesso!")

# Caminho do arquivo Excel e índices das colunas a serem removidas
arquivo_excel = r"E:\ProjetoLOTOFACIL\Resultados.xlsx"  # Caminho do seu arquivo Excel
# Índices das colunas que você quer remover: 2, 18, 19, 20 até 33 (lembre-se que o índice é baseado em 0)
indices_remover = [1, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

# Importa dados do Excel para o banco Importados.db
importar_excel_para_sqlite(arquivo_excel, indices_remover)

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
