
class Produto:
    def __init__(self, nome, tipo, preco):
        self.nome = nome
        self.tipo = tipo
        self.preco = preco

    def __str__(self):
        return f"Nome: {self.nome}, Tipo: {self.tipo}, Preço: R${self.preco:.2f}"


def main():
    produtos = []

    while True:
        print("\n--- Cadastro de produtos ----")
        print("1. Cadastrar produto")
        print("2. Listar produtos")
        print("3. Remover produto")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do produto: ")
            tipo = input("Tipo (eletrônico, roupa, alimento): ").lower()
            preco = float(input("Preço do produto: R$"))
            
            produtos.append(Produto(nome, tipo, preco))
            print(f"Produto '{nome}' cadastrado com sucesso!")

        elif opcao == '2':
            if produtos:
                print("\n--- Lista de Produtos ---")
                for produto in produtos:
                    print(produto)
            else:
                print("Nenhum produto cadastrado.")

        elif opcao == '3':
            nome_remover = input("Nome do produto para remover: ").lower()
            for i, produto in enumerate(produtos):
                if produto.nome.lower() == nome_remover:
                    del produtos[i]
                    print(f"Produto '{produto.nome}' removido.")
                    break
            else:
                print("Produto não encontrado.")

        elif opcao == '4':
            print("Saindo do sistema.")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()