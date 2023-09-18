import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup
import concurrent.futures
import subprocess

# Rango de direcciones IP a analizar
start_ip = 1
end_ip = 254

# URL base común para todas las IP
base_url = 'http://192.168.29.'

def ping_ip(ip):
    # Componer la dirección IP
    ip_address = base_url + str(ip)
    
    # Ejecutar el comando ping y verificar si la IP responde
    try:
        subprocess.check_output(['ping', '-c', '1', ip_address])
        return ip_address
    except subprocess.CalledProcessError:
        return None

def analyze_ip(ip):
    # Verificar si la IP responde al ping
    if ping_ip(ip):
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
            #print(url)
            pass

        except Exception as e:
            print(url + " - Error: " + str(e))

# Utiliza ThreadPoolExecutor para ejecutar las solicitudes en paralelo
with concurrent.futures.ThreadPoolExecutor() as executor:
    ips = range(start_ip, end_ip + 1)
    results = executor.map(analyze_ip, ips)
