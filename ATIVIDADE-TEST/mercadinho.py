# mercadinho.py

usuarios = {}
produtos = {}
vendas = []

admin_user = "admin"
admin_pass = "1234"

def login():
    print("==== LOGIN ====")
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    if usuario == admin_user and senha == admin_pass:
        print("✅ Login realizado com sucesso!\n")
        return True
    else:
        print("❌ Usuário ou senha incorretos.\n")
        return False

def menu_principal():
    while True:
        print("""
====== MENU PRINCIPAL ======
1 - Cadastrar Usuário
2 - Remover Usuário
3 - Cadastrar Produto
4 - Remover Produto
5 - Listar Produtos
6 - Realizar Venda
7 - Listar Usuários
8 - Sair
""")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            remover_usuario()
        elif opcao == "3":
            cadastrar_produto()
        elif opcao == "4":
            remover_produto()
        elif opcao == "5":
            listar_produtos()
        elif opcao == "6":
            realizar_venda()
        elif opcao == "7":
            listar_usuarios()
        elif opcao == "8":
            print("Encerrando sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

def cadastrar_usuario():
    print("=== Cadastro de Usuário ===")
    nome = input("Nome completo: ")
    user_id = input("ID do usuário: ")
    email = input("E-mail: ")
    telefone = input("Telefone: ")

    if user_id in usuarios:
        print("❌ Usuário com esse ID já existe.")
        return

    usuarios[user_id] = {"nome": nome, "email": email, "telefone": telefone}
    print(f"✅ Usuário '{nome}' cadastrado com sucesso.\n")

def remover_usuario():
    print("=== Remoção de Usuário ===")
    user_id = input("ID do usuário a remover: ")
    if user_id in usuarios:
        del usuarios[user_id]
        print("✅ Usuário removido com sucesso.\n")
    else:
        print("❌ Usuário não encontrado.\n")

def cadastrar_produto():
    print("=== Cadastro de Produto ===")
    nome = input("Nome do produto: ")
    categoria = input("Categoria (Alimentos, Bebidas, Limpeza): ")
    preco = float(input("Preço: "))
    estoque = int(input("Quantidade em estoque: "))

    if nome in produtos:
        print("❌ Produto já cadastrado.")
        return

    produtos[nome] = {"categoria": categoria, "preco": preco, "estoque": estoque}
    print(f"✅ Produto '{nome}' cadastrado com sucesso.\n")

def remover_produto():
    print("=== Remoção de Produto ===")
    nome = input("Nome do produto a remover: ")
    if nome in produtos:
        del produtos[nome]
        print("✅ Produto removido com sucesso.\n")
    else:
        print("❌ Produto não encontrado.\n")

def listar_produtos():
    print("=== Lista de Produtos ===")
    if not produtos:
        print("Nenhum produto cadastrado.\n")
        return
    for nome, info in produtos.items():
        print(f"{nome} | Categoria: {info['categoria']} | Preço: R${info['preco']} | Estoque: {info['estoque']}")
    print("")

def realizar_venda():
    print("=== Realizar Venda ===")
    nome_cliente = input("Nome do cliente: ")
    produto_nome = input("Nome do produto: ")
    quantidade = int(input("Quantidade: "))

    if produto_nome not in produtos:
        print("❌ Produto não encontrado.")
        return

    produto = produtos[produto_nome]
    if produto["estoque"] < quantidade:
        print("❌ Estoque insuficiente.")
        return

    total = produto["preco"] * quantidade
    produto["estoque"] -= quantidade
    vendas.append({"cliente": nome_cliente, "produto": produto_nome, "qtd": quantidade, "total": total})

    print(f"✅ Venda realizada para {nome_cliente} | Total: R${total:.2f}\n")

def listar_usuarios():
    print("=== Lista de Usuários ===")
    if not usuarios:
        print("Nenhum usuário cadastrado.\n")
        return
    for uid, info in usuarios.items():
        print(f"ID: {uid} | Nome: {info['nome']} | Email: {info['email']} | Telefone: {info['telefone']}")
    print("")

# Execução principal
if __name__ == "__main__":
    if login():
        menu_principal()
