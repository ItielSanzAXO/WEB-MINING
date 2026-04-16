from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

import os
import subprocess

driver = webdriver.Chrome()
driver.get("https://itiztapalapa1.mindbox.app/login/administrativo")
usuario = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='user']")))
usuario.clear()
usuario.send_keys('VEMJ840712NP2')
pwd = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
pwd.clear()
pwd.send_keys('putoelquelolea')
boton = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "btn btn-primary btn-block")]')
boton.click()
#//boton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"button[name='btnG']"))).click()
# tiempo para esté en el DOM
driver.get("https://itiztapalapa1.mindbox.app/teachers/courses/index")
driver.get("https://itiztapalapa1.mindbox.app/teachers/scores/units/20261/12322")
inputs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH,'//input[@type="number" and @tabindex="2" and @class="form-control min-w-20 max-w-20"]'))
    )
for input_element in inputs:
    input_element.clear()
    input_element.send_keys('0')


boton_imprimir = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-warning"]//button[contains(text(), "Imprimir")]')))

boton_imprimir.click()


directorio_descargas = os.path.join(os.path.expanduser("~"), "Downloads")


time.sleep(5)

def obtener_archivo_mas_reciente(directorio):
    archivos = [os.path.join(directorio, f) for f in os.listdir(directorio)]

    archivos = [f for f in archivos if os.path.isfile(f)]

    return max(archivos, key=os.path.getmtime) if archivos else None


archivo_descargado = obtener_archivo_mas_reciente(directorio_descargas)

if archivo_descargado:

    try:
        subprocess.run(["open", archivo_descargado])
    except Exception as e:
        print(f"No se pudo abrir el archivo: {e}")
else:
    print("No se encontró ningún archivo descargado.")

time.sleep(10)