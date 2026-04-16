from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Edge(options=options)
driver.get("https://www.youtube.com")

# Esperar a que el campo de búsqueda esté disponible y buscar el video
# en TODOS los WebDriverWait(driver, 10) son los segundos, si no se encuentra, se lanzará una excepción TimeoutException
buscador = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='search_query']"))
)
buscador.clear() # Limpiar el campo de búsqueda antes de escribir
buscador.send_keys("NSQK - Si en tu mente estuve")

boton_buscar = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytSearchboxComponentSearchButton"))
)
boton_buscar.click()

# Esperar resultados y hacer clic en el primer video
primer_video = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "ytd-video-renderer a#video-title"))
)
primer_video.click()

# Esperar a que el video cargue y hacer clic en el botón de omitir anuncio SI aparece
try:
    skip_ad = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-skip-ad-button, .ytp-skip-ad-button"))
    )
    skip_ad.click()
except:
    pass

# Pantalla completa
fullscreen_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-fullscreen-button"))
)
fullscreen_button.click()

#Cerrar el navegador después de 30 segundos
time.sleep(30)
driver.quit()