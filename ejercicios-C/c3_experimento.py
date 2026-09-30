import json

import requests

BASE_URL = "http://127.0.0.1:8000"
libro = {"titulo": "Experimento", "paginas": 99}

# Intento 1: el diccionario va con data=, que lo manda como formulario y no como JSON.
r = requests.post(f"{BASE_URL}/libros", data=libro)
print("1) data=libro ->", r.status_code, r.text)

# Intento 2: el JSON va como texto, pero sin avisarle al servidor que es JSON.
r = requests.post(f"{BASE_URL}/libros", data=json.dumps(libro))
print("2) texto JSON sin header ->", r.status_code, r.text)

# Intento 3: URL equivocada (le falta la 's' final).
r = requests.post(f"{BASE_URL}/libro", json=libro)
print("3) URL /libro ->", r.status_code, r.text)

# Intento 4: puerto equivocado.
try:
    requests.post("http://127.0.0.1:8001/libros", json=libro)
except requests.exceptions.ConnectionError:
    print("4) puerto 8001 -> no hay nadie escuchando (ConnectionError)")

# Intento 5: el correcto, con json= (arma el cuerpo y el header solo).
r = requests.post(f"{BASE_URL}/libros", json=libro)
print("5) json=libro ->", r.status_code, r.text)
