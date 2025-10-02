import unittest
from unittest.mock import patch
import main

class TestFluxoCompleto(unittest.TestCase):

    def setUp(self):
        # Resetar dados antes de cada teste
        sistema.users = {}
        sistema.products = {}

    @patch("sistema.save_data")  # evita escrever arquivos reais
    @patch("builtins.input", side_effect=[
        # Inputs para cadastrar usuário
        "user1", "Test User", "user@test.com", "12345", "pass",
        # Inputs para remover usuário
        "user1",
        # Inputs para cadastrar produto
        "prod1", "Produto Teste", "1", "10.5", "20"
    ])
    @patch("builtins.print")  # captura prints
    def test_usuario_remocao_produto(self, mock_print, mock_input, mock_save):
        # --- Cadastro de usuário ---
        sistema.cadastrar_usuario()
        self.assertIn("user1", sistema.users)
        self.assertEqual(sistema.users["user1"]["nome"], "Test User")
        mock_print.assert_any_call("✅ Usuário cadastrado!")

        # --- Remoção de usuário ---
        def remover_usuario():
            user_id = input("ID do usuário a remover: ")
            if user_id in sistema.users:
                del sistema.users[user_id]
                sistema.save_data(sistema.USERS_FILE, sistema.users)
                print("✅ Usuário removido!")
            else:
                print("❌ Usuário não encontrado!")

        remover_usuario()
        self.assertNotIn("user1", sistema.users)
        mock_print.assert_any_call("✅ Usuário removido!")

        # --- Cadastro de produto ---
        sistema.cadastrar_produto()
        self.assertIn("prod1", sistema.products)
        self.assertEqual(sistema.products["prod1"]["nome"], "Produto Teste")
        mock_print.assert_any_call("✅ Produto cadastrado!")

if __name__ == "__main__":
    unittest.main()
