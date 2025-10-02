import json
import os

USERS_FILE = "users.json"
PRODUCTS_FILE = "products.json"

def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

users = load_data(USERS_FILE)
products = load_data(PRODUCTS_FILE)

# Usuário admin padrão
if "admin" not in users:
    users["admin"] = {"nome": "Administrador", "email": "admin@admin.com", "telefone": "0000", "senha": "1234"}
    save_data(USERS_FILE, users)

def cadastrar_usuario():
    user_id = input("ID do usuário: ")
    if user_id in users:
        print("❌ ID já existe!")
        return
    nome = input("Nome completo: ")
    email = input("E-mail: ")
    telefone = input("Telefone: ")
    senha = input("Senha: ")
    users[user_id] = {"nome": nome, "email": email, "telefone": telefone, "senha": senha}
    save_data(USERS_FILE, users)
    print("✅ Usuário cadastrado!")

def remover_usuario():
    user_id = input("ID do usuário a remover: ")
    if user_id in users and user_id != "admin":
        del users[user_id]
        save_data(USERS_FILE, users)
        print("✅ Usuário removido!")
    else:
        print("❌ Usuário não encontrado ou é o admin!")

def cadastrar_produto():
    prod_id = input("ID do produto: ")
    if prod_id in products:
        print("❌ Produto já existe!")
        return
    nome = input("Nome do produto: ")
    tipo = input("Tipo (1, 2 ou 3): ")
    preco = float(input("Preço: "))
    estoque = int(input("Quantidade em estoque: "))
    products[prod_id] = {"nome": nome, "tipo": tipo, "preco": preco, "estoque": estoque}
    save_data(PRODUCTS_FILE, products)
    print("✅ Produto cadastrado!")

def remover_produto():
    prod_id = input("ID do produto a remover: ")
    if prod_id in products:
        del products[prod_id]
        save_data(PRODUCTS_FILE, products)
        print("✅ Produto removido!")
    else:
        print("❌ Produto não encontrado!")

def atualizar_estoque():
    prod_id = input("ID do produto: ")
    if prod_id in products:
        qtd = int(input("Nova quantidade em estoque: "))
        products[prod_id]["estoque"] = qtd
        save_data(PRODUCTS_FILE, products)
        print("✅ Estoque atualizado!")
    else:
        print("❌ Produto não encontrado!")

def compra_venda(tipo):
    prod_id = input("ID do produto: ")
    if prod_id in products:
        qtd = int(input("Quantidade: "))
        if tipo == "compra":
            products[prod_id]["estoque"] += qtd
            print(f"✅ Compra registrada! Estoque atual: {products[prod_id]['estoque']}")
        elif tipo == "venda":
            if products[prod_id]["estoque"] >= qtd:
                products[prod_id]["estoque"] -= qtd
                total = qtd * products[prod_id]["preco"]
                print(f"✅ Venda registrada! Valor total: R$ {total:.2f}")
            else:
                print("❌ Estoque insuficiente!")
        save_data(PRODUCTS_FILE, products)
    else:
        print("❌ Produto não encontrado!")

def login():
    user = input("Usuário: ")
    senha = input("Senha: ")
    if user in users and users[user]["senha"] == senha:
        print(f"✅ Bem-vindo, {users[user]['nome']}!")
        return user
    else:
        print("❌ Login inválido!")
        return None

def menu_admin():
    while True:
        print("""
------ MENU ADMIN ------
1 - Cadastrar Usuário
2 - Remover Usuário
3 - Cadastrar Produto
4 - Remover Produto
5 - Atualizar Estoque
6 - Compra
7 - Venda
0 - Sair
        """)
        op = input("Escolha: ")
        if op == "1": cadastrar_usuario()
        elif op == "2": remover_usuario()
        elif op == "3": cadastrar_produto()
        elif op == "4": remover_produto()
        elif op == "5": atualizar_estoque()
        elif op == "6": compra_venda("compra")
        elif op == "7": compra_venda("venda")
        elif op == "0": break
        else: print("❌ Opção inválida!")

usuario = login()
if usuario == "admin":
    menu_admin()
else:
    print("Apenas o admin pode acessar o menu!")
