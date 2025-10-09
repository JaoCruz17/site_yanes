from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest

class TestSistema(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5500/frontend/login.html")

    def test_login_admin_local(self):
        d = self.driver
        d.find_element(By.ID, "email").send_keys("admin@admin.com")
        d.find_element(By.ID, "senha").send_keys("123456")
        d.find_element(By.ID, "btnLogin").click()
        time.sleep(2)
        self.assertIn("admin.html", d.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
