import time

import requests

URL = "http://127.0.0.1:8000/libros"
CANTIDAD = 200

inicio = time.perf_counter()
for _ in range(CANTIDAD):
    requests.get(URL)
sin_session = time.perf_counter() - inicio

inicio = time.perf_counter()
with requests.Session() as sesion:
    for _ in range(CANTIDAD):
        sesion.get(URL)
con_session = time.perf_counter() - inicio

print(f"Sin Session: {sin_session:.2f} s")
print(f"Con Session: {con_session:.2f} s")
