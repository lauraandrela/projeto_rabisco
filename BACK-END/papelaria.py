import os
import mysql.connector

conexaoDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senai",
    database="Papelaria"
)

def header():
    os.system('cls')
    print("- SISTEMA PAPELARIA -")

def cadastro():
    header()
    print("Você escolheu a opcão 1 - CADASTRO DE PRODUTOS!")
    nome = input("Informe o nome do produto: ")
    descricao = input("Informe a descrição do produto: ")

    #validação de números
    try:
        preco = float(input("Preço: "))
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("Erro! Preço e quantidade devem ser valores numéricos.")
        return
    
    #validação de campos vazios
    if (not nome) or (not descricao) or (not preco) or (not quantidade):
        print("Erro! Todos os campos devem ser preenchidos!!")
        return
    
    #validação de valores menores que zero
    if (preco < 0) or (quantidade < 0):
        print("Erro! Preço e quantidade não podem ser menores que ZERO!!")
        return

    #validação de excedência de caracteres
    if len(nome) > 50:
        print("Erro! O nome do produto excede a capacidade máxima de 50 caracteres!!")
        return
    
    comandoSQL = f'INSERT INTO Produto VALUES (null, "{nome}", "{descricao}", {preco}, {quantidade})'

    try:
        cursorDB = conexaoDB.cursor()
        cursorDB.execute(comandoSQL)
        conexaoDB.commit()
    except mysql.connector.Error as erro:
        print(f"Erro! Falha ao cadastrar: {erro}")
        return
    
    print("*** OK! Cadastro realizado com sucesso!!")
    cursorDB.close()

def estoque():
    header()
    print("Você escolheu a opcão 2 - ALTERAR ESTOQUE!")
    try:
        id_produto = int(input("Informe o ID do produto: "))
    except ValueError:
        print("Erro! ID deve ser numérico!")
        return
    
    produto = get_produto(id_produto)

    if not produto:
        print(f"Produto com o ID {id_produto} não encontrado!")
        return
    print("Produto encontrado!")
    print(f"ID: {produto[0]} - NOME: {produto[1]} - QUANTIDADE ATUAL: {produto[4]}")

    try:
        nova_quantidade = int(input("Informe a nova quantidade: "))
    except ValueError:
        print("Erro! Valor da quantidade deve ser um número inteiro!")
        return
    
    if nova_quantidade == produto[4]: 
        print("A quantidade informada é igual à quantidade anterior!")
        return
    if nova_quantidade < 0 or nova_quantidade > 10000:
        print("Erro: A quantidade não pode ser negativa ou menor que 10000!")
        return
    
def preco():
    header()
    print("Você escolheu a opcão 3 - ALTERAR PREÇO!")
    try:
        id_produto = int(input("Informe o ID do produto: "))
    except ValueError:
        print("Erro! ID deve ser numérico!")
        return
    
    produto = get_produto(id_produto)

    if not produto:
        print(f"Produto com o ID {id_produto} não encontrado!")
        return
    print("Produto encontrado!")
    print(f"ID: {produto[0]} - NOME: {produto[1]} - PREÇO ATUAL: {produto[3]}")

    try:
        novo_preco = float(input("Informe o novo preço: "))
    except ValueError:
        print("Erro! Valor da quantidade deve ser numérico!")
        return
    
    if novo_preco == produto[3]: 
        print("O preço informado é igual ao preço anterior!")
        return
    
    if novo_preco < 0 or novo_preco > 1000:
        print("Erro: O preço não pode ser negativo ou maior que 1000!")
        return
    
    try:
        comandoSQL = f'UPDATE Profuto SET quantidade = {novo_preco} WHERE idProduto = {id_produto}'
        cursorDB = conexaoDB.cursor()
        cursorDB.execute(comandoSQL)
        conexaoDB.commit()
    except mysql.connector.Error as erro:
        print(f'Erro: Falha na atualização: {erro}')

    print("OK! Atualização realizada com sucesso!")
    cursorDB.close()

def listar():
    header()
    print("Você escolheu a opcão 4 - LISTAR PRODUTOS!")

    try: 
        cursorDB = conexaoDB.cursor()
        cursorDB.execute('SELECT * FROM Produto')
        resultados = cursorDB.fetchall()

        if not resultados:
            print("Não há produtos cadastrados!")
        else:
            for produto in resultados:
                print(f"ID: {produto[0]} - NOME: {produto[1]} - DESCRIÇÃO {produto[2]} - PREÇO {produto[3]} - QUANTIDADE {produto[4]}")
                print("- " * 50)
    except mysql.connector.Error as erro:
        print(f"Erro! Falha ao listar: {erro}")
        return 
       
    cursorDB.close()

def get_produto(id_produto):
    cursorDB = conexaoDB.cursor()
    comandoSQL = f'SELECT * FROM Produto WHERE idProduto = {id_produto}'
    cursorDB.execute(comandoSQL)
    resultado = cursorDB.fetchone()
    cursorDB.close()
    return resultado

def excluir():
    header()
    print("Você escolheu a opcão 5 - EXCLUIR PRODUTOS!")
    try:
        id_produto = int(input("Informe o ID do produto: "))
    except ValueError:
        print("Erro! ID deve ser numérico!")
        return
    
    produto = get_produto(id_produto)

    if not produto:
        print(f"Produto com o ID {id_produto} não encontrado!")
        return
    print("Produto encontrado!")
    print(f"ID: {produto[0]} - NOME: {produto[1]}")

    confirma = input("Digite S para confirmar a exclusão: ")
    if confirma != 'S' and confirma != 's':
        print("Exclusão cancelada!")
        return
    try:
        cursorDB = conexaoDB.cursor()
        comandoSQL = f'DELETE FROM Produto WHERE idProduto = {id_produto}'
        cursorDB.execute()
        conexaoDB.commit()
    except mysql.connector.Error as erro:
        print(f'Erro: Falha na exclusão: {erro}')
        return
    
    print("OK! Exclusão frealizada com sucesso!")
    cursorDB.close()

while True:
    header()
    print("MENU PAPELARIA")
    print("1 - Cadastrar produto")
    print("2 - Alterar estoque de produto")
    print("3 - Alterar preço de produto")
    print("4 - Listar produtos")
    print("5 - Excluir produto")
    print("6 - Sair do sistema")
    opcao = input("Informe a opção desejada: ")

    if opcao == '1':
        cadastro()
    elif opcao == '2':
        estoque()
    elif opcao == '3':
        preco()
    elif opcao == '4':
        listar()
    elif opcao == '5':
        excluir()
    elif opcao == '6':
        break
    else:
        print("OPÇÃO INVÁLIDA!")

    os.system('pause')

print("SISTEMA ENCERRADO!")
conexaoDB.close()