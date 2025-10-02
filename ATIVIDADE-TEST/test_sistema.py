# teste_sistema.py
from mercadinho import adicionar_usuario, cadastrar_produto, realizar_venda, usuarios, produtos, vendas

def teste_fluxo_completo():
    # Limpar dados antes do teste
    usuarios.clear()
    produtos.clear()
    vendas.clear()

    # Cadastrar usuário
    res1 = adicionar_usuario("001", "João Silva", "joao@email.com", "999999999")
    assert res1 == True, "Falha ao cadastrar usuário"

    # Cadastrar produto
    res2 = cadastrar_produto("Arroz", "Alimentos", 10.0, 50)
    assert res2 == True, "Falha ao cadastrar produto"

    # Realizar venda
    res3 = realizar_venda("João Silva", "Arroz", 5)
    assert res3 == True, "Falha ao realizar venda"

    # Verificar estoque atualizado
    assert produtos["Arroz"]["estoque"] == 45, "Estoque não atualizado corretamente"

    print("Teste de Sistema concluído com sucesso.")

if __name__ == "__main__":
    teste_fluxo_completo()
