from bs4 import BeautifulSoup
import pandas as pd
import requests
from dateutil import parser
from datetime import datetime, timedelta  # Importar datetime y timedelta desde datetime
import locale

def generar_web_scrapping():
    # Obtén el contenido HTML del URL
    url = "https://www.acueducto.com.co/wps/portal/EAB2/Home/atencion-al-usuario/programacion_cortes"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encuentra la tabla en el HTML
    tabla_html = soup.find('table', {'class': 'table table-striped mt20 table-bordered table-blue w100 table-responsive'})

    # Inicializar una lista para almacenar los datos
    data = []

    # Encontrar todas las filas en la tabla
    filas = tabla_html.find_all('tr')

    # Inicializar la variable para almacenar el valor de la columna y la validez
    valor_columna = ""
    dato_valido = False

    # Iterar sobre cada fila e imprimir su contenido
    for fila in filas:
        celdas = fila.find_all('td')
        fila_data = []
        for celda in celdas:
            fila_data.append(celda.text.strip())
            if "2023" in celda.text.strip() or "2024" in celda.text.strip():
                valor_columna = celda.text.strip()
                dato_valido = True
        if fila_data and valor_columna:
            fila_data.append(valor_columna)
            fila_data.append(dato_valido)
            data.append(fila_data)
        else:
            dato_valido = False

    # Convertir la lista de datos a un DataFrame de pandas
    df = pd.DataFrame(data, columns=['Localidad', 'Barrios', 'Direccion', 'Horario', 'Trabajo', 'Fecha', 'Dato No Válido'])

    # Establecer la configuración regional en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Obtener la fecha de mañana
    fecha_manana = datetime.now() + timedelta(days=1)  # Usar datetime y timedelta directamente

    # Formatear la fecha de mañana como texto
    texto_fecha_manana = fecha_manana.strftime("%A %d de %B de %Y")

    # Restaurar la configuración regional predeterminada
    locale.setlocale(locale.LC_TIME, '')

    fecha_convertida = texto_fecha_manana.capitalize()

    localidad_validacion = 'Ciudad Bolívar'

    # Filtrar el DataFrame por fecha de mañana y localidad
    df_filtered = df[(df['Fecha'].str.contains(fecha_convertida)) & (df['Localidad'].str.contains(localidad_validacion))]

    return df_filtered
