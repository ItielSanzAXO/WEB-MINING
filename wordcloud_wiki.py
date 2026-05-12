from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# ===== CONFIGURACION DE SELENIUM =====
print("Abriendo navegador...")
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Edge(options=options)

# ===== ENTRADA A WIKIPEDIA =====
print("Entrando a Wikipedia...")
driver.get("https://es.wikipedia.org")
time.sleep(2)

# ===== BUSQUEDA EN WIKIPEDIA =====
print("Buscando 'Mundial de futbol 2026'...")

# Clic en la lupa para abrir el buscador
lupa = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cdx-button--icon-only, a.search-toggle"))
)
lupa.click()
time.sleep(1)

# Escribir en el campo de búsqueda
buscador = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search'], input[name='search']"))
)
buscador.send_keys("Mundial de futbol 2026")
time.sleep(1)

# Clic en el botón Buscar
boton_buscar = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cdx-search-input__end-button"))
)
boton_buscar.click()
print("Esperando resultados...")
time.sleep(4)

# Abrir primer resultado
print("Abriendo primer resultado...")
primer_resultado = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, ".mw-search-result-heading a"))
)
primer_resultado.click()
print("Esperando que cargue el articulo...")
time.sleep(4)

# except Exception as e:
#     print(f"Error abriendo resultado: {e}")
#     driver.get("https://es.wikipedia.org/wiki/Copa_Mundial_de_F%C3%BAtbol_de_2026")
#     time.sleep(3)

url_actual = driver.current_url
print(f"Articulo abierto: {url_actual}")
print("Extrayendo contenido...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
response = requests.get(url_actual, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    texto = soup.get_text(separator=' ', strip=True)
    print(f"Contenido extraido: {len(texto)} caracteres")
else:
    print(f"Error al acceder. Codigo: {response.status_code}")
    driver.quit()
    exit()

# ===== LIMPIEZA DE TEXTO =====
print("Limpiando texto...")
palabras_eliminar = [
    'tan','da','hace','solo','lo','y','se','que','el','la','los','las','de','a','en','un','una','por','para','con','uno','dos',
    'no','es','como','mas','menos','si','al','del','sobre','este','esta','entre','otro',
    'me','te','cuando','muy','tambien','ser','yo','fue',
    'ellos','ellas','ha','haber','hacer','esto','estos','esas','pero','o','todo',
    'todos','cual','su','sus','aquel','aquella','aquellos','aquellas','mi',
    'mis','tu','tus','nuestro','nuestros','nuestra','nuestras','desde'
]

texto_limpio = texto.lower()
palabras = texto_limpio.split()
palabras_limpias = [p for p in palabras if p.isalpha() and p not in palabras_eliminar]
texto_limpio = ' '.join(palabras_limpias)
print(f"Texto limpio: {len(palabras_limpias)} palabras")

# ===== WORD CLOUD =====
print("Generando Word Cloud...")
try:
    imagen = Image.open('mundial_2026.png').convert("RGBA")
    imagen2 = Image.new("RGB", imagen.size, "WHITE")
    imagen2.paste(imagen, (0, 0), imagen)
    mascara = np.array(imagen2)
    colores_mascara = ImageColorGenerator(mascara)

    wordcloud = WordCloud(mask=mascara, contour_width=3, min_font_size=6, contour_color='grey',
                          collocation_threshold=10, width=600, height=300,
                          background_color='white').generate(texto_limpio)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud.recolor(color_func=colores_mascara), interpolation='bilinear')
    plt.axis('off')
    plt.title("Word Cloud - Mundial de Futbol 2026")
    print("Word Cloud creado. Mostrando...")
    plt.show()

except FileNotFoundError:
    print("Error: No se encontro 'mundial_2026.png'")
except Exception as e:
    print(f"Error al generar word cloud: {e}")

driver.quit()
print("Proceso completado")
