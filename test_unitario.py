import unittest
import os
import json
from main import cadastrar_usuario, users, save_data, USERS_FILE

class TestUsuarios(unittest.TestCase):
    def setUp(self):
        # Limpa dados de teste
        if os.path.exists(USERS_FILE):
            os.remove(USERS_FILE)
        users.clear()
        save_data(USERS_FILE, users)

    def test_cadastro_usuario(self):
        # Simulando input
        users["teste1"] = {"nome": "Teste", "email": "teste@teste.com", "telefone": "1111", "senha": "123"}
        save_data(USERS_FILE, users)

        with open(USERS_FILE, "r") as f:
            data = json.load(f)
        self.assertIn("teste1", data)

if __name__ == '__main__':
    unittest.main()