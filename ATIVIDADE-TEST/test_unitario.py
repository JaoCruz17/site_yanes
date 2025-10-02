import unittest
import mercadinho  

class TestMercadinho(unittest.TestCase):
    def setUp(self):
        # Limpa os dados antes de cada teste
        mercadinho.usuarios.clear()
        mercadinho.produtos.clear()
        mercadinho.vendas.clear()

    def test_adicionar_usuario(self):
        self.assertTrue(mercadinho.adicionar_usuario("001", "João", "joao@email.com", "999999999"))
        self.assertFalse(mercadinho.adicionar_usuario("001", "Maria", "maria@email.com", "888888888"))  

    def test_remover_usuario(self):
        mercadinho.adicionar_usuario("001", "João", "joao@email.com", "999999999")
        self.assertTrue(mercadinho.remover_usuario("001"))
        self.assertFalse(mercadinho.remover_usuario("002"))  

    def test_cadastrar_produto(self):
        self.assertTrue(mercadinho.cadastrar_produto("Arroz", "Alimentos", 10.0, 50))
        self.assertFalse(mercadinho.cadastrar_produto("Arroz", "Alimentos", 8.0, 30))  

    def test_remover_produto(self):
        mercadinho.cadastrar_produto("Arroz", "Alimentos", 10.0, 50)
        self.assertTrue(mercadinho.remover_produto("Arroz"))
        self.assertFalse(mercadinho.remover_produto("Feijão"))  

    def test_realizar_venda(self):
        mercadinho.cadastrar_produto("Arroz", "Alimentos", 10.0, 50)
        self.assertFalse(mercadinho.realizar_venda("João", "Feijão", 5))  
        self.assertFalse(mercadinho.realizar_venda("João", "Arroz", 60))  
        self.assertTrue(mercadinho.realizar_venda("João", "Arroz", 10))
        self.assertEqual(mercadinho.produtos["Arroz"]["estoque"], 40) 

if __name__ == "__main__":
    unittest.main()
