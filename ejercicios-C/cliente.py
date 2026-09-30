import requests

respuesta = requests.get("http://127.0.0.1:8000/libros")

print(respuesta.status_code)
print(respuesta.json())
