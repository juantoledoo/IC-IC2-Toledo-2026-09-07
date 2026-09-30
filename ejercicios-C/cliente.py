import requests

BASE_URL = "http://127.0.0.1:8000"


def listar_libros():
    respuesta = requests.get(f"{BASE_URL}/libros")
    return respuesta.json()


def crear_libro(libro):
    respuesta = requests.post(f"{BASE_URL}/libros", json=libro)
    return respuesta.json()


if __name__ == "__main__":
    nuevo = {"titulo": "Bestiario", "paginas": 150}
    print("Creado:", crear_libro(nuevo))
    libros = listar_libros()
    titulos = [libro["titulo"] for libro in libros]
    print("Titulos ahora:", titulos)
    print("Se agrego:", "Bestiario" in titulos)
    