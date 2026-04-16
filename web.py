from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def reproducir_youtube(video_url=None, busqueda=None, esperar_segundos=30):
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 20)
    pagina_principal = "https://www.youtube.com/?app=desktop&hl=es"

    try:
        if video_url:
            driver.get(video_url)
        else:
            driver.get(pagina_principal)
            caja_busqueda = wait.until(
                EC.element_to_be_clickable((By.NAME, "search_query"))
            )
            caja_busqueda.clear()
            caja_busqueda.send_keys(busqueda or "musica relajante")
            caja_busqueda.send_keys(Keys.ENTER)

            primer_video = wait.until(
                EC.element_to_be_clickable((By.XPATH, "(//a[@id='video-title'])[1]"))
            )
            primer_video.click()

        video = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))

        # Espera a que el video tenga datos suficientes para iniciar reproduccion.
        wait.until(
            lambda d: d.execute_script(
                "return arguments[0].readyState >= 3 && arguments[0].duration > 0;",
                video,
            )
        )

        # Autoplay robusto: intenta play por script y, si sigue pausado, clic en boton play.
        for _ in range(3):
            driver.execute_script("arguments[0].play();", video)
            time.sleep(1)

            esta_pausado = driver.execute_script("return arguments[0].paused;", video)
            if not esta_pausado:
                break

            boton_play = driver.find_element(By.CSS_SELECTOR, "button.ytp-play-button")
            boton_play.click()

        print("Video abierto. Reproduciendo...")
        time.sleep(esperar_segundos)
    finally:
        driver.quit()


if __name__ == "__main__":
    # Opcion 1: pega aqui un enlace directo de YouTube.
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    # Opcion 2: deja url en None y usa una busqueda.
    termino_busqueda = "python selenium tutorial"

    reproducir_youtube(video_url=url, busqueda=termino_busqueda, esperar_segundos=40)