# pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scraper_poblacion():
    # 1. URL de la página (Lista de países por población)
    url = "https://slepsantarosa.gob.cl/establecimientos-educacionales/"
    # 2. Hacer la petición a la web
    headers = {'User-Agent': 'Mozilla/5.0'} # Evita que Wikipedia bloquee el script
    respuesta = requests.get(url, headers=headers)

    if respuesta.status_code != 200:
        print("Error al acceder a la página")
        return

    # 3. Parsear el HTML
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    # 4. Buscar la tabla (Wikipedia suele usar la clase 'wikitable')
    tabla = soup.find('figure', {'class': 'wp-block-table'})

    # 5. Extraer filas
    filas = []
    for fila in tabla.find_all('tr')[1:]:  # [1:] para saltar el encabezado
        columnas = fila.find_all(['td', 'th'])
        # print(type(columnas[0]))
        if len(columnas) > 2:
            # Limpiamos el texto de saltos de línea y espacios extra
            datos = {
                "Nombre Establecimiento": columnas[1].get_text(strip=True),
                "Dirección": columnas[3].get_text(strip=True),
                "Comuna": columnas[0].get_text(strip=True)
            }
            filas.append(datos)

        if len(filas) == 20: # Limitar a los top 20 para el ejemplo
            break

    # 6. Convertir a DataFrame de Pandas para visualizar mejor
    df = pd.DataFrame(filas)
    return df

# Ejecutar y mostrar resultados
resultado = scraper_poblacion()
print("### Datos Recolectados ###")
print(resultado) # Muestra los primeros 10

# Guardar a CSV (se guarda en la carpeta 'Files' de la izquierda en Colab)
resultado.to_csv("datos_poblacion.csv", index=False)