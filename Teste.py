import sqlite3

# Função para verificar quantos sorteios tiveram mais ímpares que pares
def verificar_impares_versus_pares():
    # Conectar ao banco SQLite
    conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados do site da lotérica.db")  # Substitua pelo caminho correto do seu banco
    cursor = conn.cursor()

    # Consultar todos os sorteios, selecionando as colunas de Bola1 a Bola15
    cursor.execute("SELECT Bola1, Bola2, Bola3, Bola4, Bola5, Bola6, Bola7, Bola8, Bola9, Bola10, Bola11, Bola12, Bola13, Bola14, Bola15 FROM dados_importados")
    resultados = cursor.fetchall()

    mais_impares = 0

    for linha in resultados:
        # Cada 'linha' aqui é uma tupla com os valores das bolas
        numeros = [int(n) for n in linha]  # Convertendo os valores para inteiros

        # Contar ímpares e pares
        qtd_impares = sum(1 for n in numeros if n % 2 != 0)
        qtd_pares = len(numeros) - qtd_impares

        # Verificar se há mais ímpares que pares
        if qtd_impares > qtd_pares:
            mais_impares += 1

    # Exibir o total de sorteios com mais ímpares
    print(f'{mais_impares} sorteios tiveram mais ímpares que pares.')

    # Fechar a conexão
    conn.close()

# Executar a função para verificar os sorteios
verificar_impares_versus_pares()
