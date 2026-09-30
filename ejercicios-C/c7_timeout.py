import requests

URL_SIN_RESPUESTA = "http://10.255.255.1/"

try:
    requests.get(URL_SIN_RESPUESTA, timeout=1)
except requests.exceptions.Timeout as error:
    print("Saltó el timeout:", type(error).__name__)
except requests.exceptions.RequestException as error:
    print("Falló por otro motivo:", type(error).__name__)
