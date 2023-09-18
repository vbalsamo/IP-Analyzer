import argparse
import requests
from requests.exceptions import ConnectTimeout
from bs4 import BeautifulSoup
import concurrent.futures


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Script to analyze IP addresses within a given range."
    )
    parser.add_argument(
        "base_url", help="Base URL for all IP addresses. Ex: http://192.168.1."
    )
    parser.add_argument(
        "start_ip", type=int, help="Starting IP address (integer). Ex: 1"
    )
    parser.add_argument("end_ip", type=int, help="Ending IP address (integer). Ex: 254")
    return parser.parse_args()


args = parse_arguments()

base_url = args.base_url
start_ip = args.start_ip
end_ip = args.end_ip


def analyze_ip(ip):
    url = base_url + str(ip)

    try:
        response = requests.get(url, timeout=1)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find("title")

            if title_tag:
                print(url + " - " + title_tag.text)
            else:
                print(url + " - Sin título.")

    except ConnectTimeout as e:
        print(url)

    except Exception as e:
        print(url + " - Error: " + str(e))


with concurrent.futures.ThreadPoolExecutor() as executor:
    ips = range(start_ip, end_ip + 1)
    results = executor.map(analyze_ip, ips)
