import argparse
import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup
import concurrent.futures
import subprocess

def parse_arguments():
    parser = argparse.ArgumentParser(description='Script to analyze IP addresses within a given range.')
    parser.add_argument('base_url', help='Base URL for all IP addresses. Ex: http://192.168.1.')
    parser.add_argument('start_ip', type=int, help='Starting IP address (integer). Ex: 1')
    parser.add_argument('end_ip', type=int, help='Ending IP address (integer). Ex: 254')
    return parser.parse_args()

# Parsear los argumentos de línea de comandos
args = parse_arguments()

# Asignar los valores de los argumentos a las variables correspondientes
base_url = args.base_url
start_ip = args.start_ip
end_ip = args.end_ip

def analyze_ip(ip):
# Verificar si la IP responde al ping
    # Componer la URL completa con la dirección IP actual
    url = base_url + str(ip)

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

# Utiliza ThreadPoolExecutor para ejecutar las solicitudes en paralelo
with concurrent.futures.ThreadPoolExecutor() as executor:
    ips = range(start_ip, end_ip + 1)
    results = executor.map(analyze_ip, ips)
