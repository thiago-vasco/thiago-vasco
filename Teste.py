import sqlite3

# Função para verificar quantos sorteios tiveram mais ímpares que pares
def verificar_impares_versus_pares():
    # Conectar ao banco SQLite
    conn = sqlite3.connect(r"E:\ProjetoLOTOFACIL\Importados.db")  # Substitua pelo caminho correto do seu banco
    cursor = conn.cursor()

    # Consultar todos os sorteios, selecionando todas as colunas (incluindo as bolas)
    cursor.execute("SELECT * FROM dados_importados")  # Isso pega todos os dados das colunas
    resultados = cursor.fetchall()

    mais_impares = 0  # Contador para sorteios com mais ímpares
    mais_pares = 0    # Contador para sorteios com mais pares

    for linha in resultados:
        # A primeira coluna será o Concurso, que não precisamos para a contagem
        numeros = linha[1:]  # Excluímos a primeira coluna, pois contém o Concurso (linha[0])

        # Contar ímpares e pares
        qtd_impares = sum(1 for n in numeros if n % 2 != 0)
        qtd_pares = len(numeros) - qtd_impares

        # Print para depuração
        print(f"Sorteio: {linha[0]} - Ímpares: {qtd_impares} / Pares: {qtd_pares}")

        # Verificar se há mais ímpares que pares
        if qtd_impares > qtd_pares:
            mais_impares += 1
        elif qtd_pares > qtd_impares:
            mais_pares += 1

    # Exibir o total de sorteios com mais ímpares e pares
    print(f'{mais_impares} sorteios tiveram mais ímpares que pares.')
    print(f'{mais_pares} sorteios tiveram mais pares que ímpares.')

    # Fechar a conexão
    conn.close()

# Executar a função para verificar os sorteios
verificar_impares_versus_pares()
