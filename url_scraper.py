import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup

# Rango de direcciones IP a analizar
start_ip = 1
end_ip = 255

# URL base común para todas las IP
base_url = 'http://192.168.29.'

for i in range(start_ip, end_ip + 1):
    # Componer la URL completa con la dirección IP actual
    url = base_url + str(i)

    try:
        # Realiza una solicitud GET a la URL
        response = requests.get(url, timeout=1)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Parsea el contenido HTML de la página
            soup = BeautifulSoup(response.text, 'html.parser')

            # Encuentra la etiqueta <title>
            title_tag = soup.find('title')

            if title_tag:
                # Imprime el contenido de la etiqueta <title>
                print(url + ' - ' + title_tag.text)
            else:
                print(url + " - Sin título.")
    
    except ConnectTimeout as e:
        print(url)

    except Exception as e:
        print(url + " - Error: " + str(e))
