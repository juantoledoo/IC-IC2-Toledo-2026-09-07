import requests

BASE_URL = "http://127.0.0.1:8000"


def listar_libros():
    return requests.get(f"{BASE_URL}/libros")


def obtener_libro(titulo):
    return requests.get(f"{BASE_URL}/libros/{titulo}")


def crear_libro(libro):
    return requests.post(f"{BASE_URL}/libros", json=libro)


def describir(respuesta):
    if respuesta.status_code in (200, 201):
        return "ok"
    if respuesta.status_code == 422:
        return "dato inválido"
    if respuesta.status_code == 404:
        return "no existe"
    return f"respuesta inesperada ({respuesta.status_code})"


if __name__ == "__main__":
    casos = [
        ("Crear libro válido", crear_libro({"titulo": "Bestiario", "paginas": 150})),
        ("Crear libro con 0 páginas", crear_libro({"titulo": "Vacio", "paginas": 0})),
        ("Buscar libro inexistente", obtener_libro("NoExiste")),
        ("Listar libros", listar_libros()),
    ]
    for nombre, respuesta in casos:
        print(f"{nombre}: {describir(respuesta)} (código {respuesta.status_code})")
         