from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import unittest, time, random

class TestSistemaReal(unittest.TestCase):
    def setUp(self):
        # Inicia o navegador Chrome
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.base_url = "http://localhost:5500"  # ajuste conforme seu projeto

    def test_fluxo_real(self):
        d = self.driver

        # =======================
        # 1️⃣ LOGIN REAL
        # =======================
        d.get(f"{self.base_url}/login.html")
        d.find_element(By.ID, "email").send_keys("admin@admin.com")
        d.find_element(By.ID, "senha").send_keys("123456")
        d.find_element(By.ID, "btnLogin").click()
        time.sleep(3)  # espera redirecionamento

        assert "admin.html" in d.current_url, "Falha no login"

        # =======================
        # 2️⃣ CADASTRAR USUÁRIO REAL
        # =======================
        d.get(f"{self.base_url}/cadastro_usuario.html")
        time.sleep(1)

        random_id = random.randint(1000,9999)
        d.find_element(By.ID, "nome").send_keys(f"Teste User {random_id}")
        d.find_element(By.ID, "idUsuario").send_keys(f"ID{random_id}")
        d.find_element(By.ID, "email").send_keys(f"teste{random_id}@email.com")
        d.find_element(By.ID, "telefone").send_keys(f"119{random_id}")
        d.find_element(By.ID, "senha").send_keys("123456")
        d.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        msg_usuario = d.find_element(By.ID, "msg").text
        assert "cadastrado" in msg_usuario.lower(), "Falha ao cadastrar usuário"

        # =======================
        # 3️⃣ CADASTRAR PRODUTO REAL
        # =======================
        d.get(f"{self.base_url}/cadastro_produto.html")
        time.sleep(1)

        d.find_element(By.ID, "nome").send_keys(f"Produto Teste {random_id}")
        d.find_element(By.ID, "codigo").send_keys(f"C{random_id}")
        d.find_element(By.ID, "preco").send_keys("9.99")
        d.find_element(By.ID, "quantidade").send_keys("50")
        d.find_element(By.ID, "descricao").send_keys("Produto de teste automatizado")
        d.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        msg_produto = d.find_element(By.ID, "msg").text
        assert "cadastrado" in msg_produto.lower(), "Falha ao cadastrar produto"

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
