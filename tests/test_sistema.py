#Automatizar login e acesso ao painel
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5500/telas/login.html")

driver.find_element(By.ID, "email").send_keys("admin@admin.com")
driver.find_element(By.ID, "senha").send_keys("123456")
driver.find_element(By.ID, "btnLogin").click()

time.sleep(2)
print("Página atual:", driver.current_url)

driver.quit()
    