import requests

BASE_URL = "http://127.0.0.1:8000"


def listar_libros():
    return requests.get(f"{BASE_URL}/libros")


def obtener_libro(titulo):
    return requests.get(f"{BASE_URL}/libros/{titulo}")


def crear_libro(libro):
    return requests.post(f"{BASE_URL}/libros", json=libro)


def reemplazar_libro(titulo, libro):
    return requests.put(f"{BASE_URL}/libros/{titulo}", json=libro)


def borrar_libro(titulo):
    return requests.delete(f"{BASE_URL}/libros/{titulo}")


def describir(respuesta):
    if respuesta.status_code in (200, 201, 204):
        return "ok"
    if respuesta.status_code == 422:
        return "dato inválido"
    if respuesta.status_code == 404:
        return "no existe"
    return f"respuesta inesperada ({respuesta.status_code})"


def mostrar(nombre, respuesta):
    print(f"{nombre}: {describir(respuesta)} (código {respuesta.status_code})")


if __name__ == "__main__":
    libro = {"titulo": "Cliente Demo", "paginas": 100}

    mostrar("Crear", crear_libro(libro))

    respuesta = listar_libros()
    titulos = [item["titulo"] for item in respuesta.json()]
    print("Títulos en la API:", titulos)

    libro_nuevo = {"titulo": "Cliente Demo", "paginas": 200}
    respuesta = reemplazar_libro("Cliente Demo", libro_nuevo)
    mostrar("Reemplazar", respuesta)
    print("Quedó así:", respuesta.json())

    mostrar("Borrar", borrar_libro("Cliente Demo"))
    mostrar("Buscar después de borrar", obtener_libro("Cliente Demo"))
           