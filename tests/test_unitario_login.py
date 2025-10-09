from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import unittest

class TestLoginSistema(unittest.TestCase):
    def setUp(self):
        # abre o navegador com o ChromeDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # abre o arquivo HTML local
        self.driver.get("http://localhost:5500/frontend/login.html")  # ajuste o caminho se necessário

    def test_login_admin_local(self):
        d = self.driver

        # insere email e senha do admin local
        d.find_element(By.ID, "email").send_keys("admin@admin.com")
        d.find_element(By.ID, "senha").send_keys("123456")

        # clica no botão de login
        d.find_element(By.ID, "btnLogin").click()
        time.sleep(2)

        # verifica se redirecionou para o painel admin
        self.assertIn("admin.html", d.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
