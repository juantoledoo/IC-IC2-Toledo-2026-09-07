import requests

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 5


def pedir(metodo, ruta, **kwargs):
    try:
        return requests.request(metodo, f"{BASE_URL}{ruta}", timeout=TIMEOUT, **kwargs)
    except requests.exceptions.Timeout:
        print("La API tardó demasiado en responder (timeout).")
        return None
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con la API. ¿Está levantada?")
        return None


def listar_libros():
    return pedir("GET", "/libros")


def obtener_libro(titulo):
    return pedir("GET", f"/libros/{titulo}")


def crear_libro(libro):
    return pedir("POST", "/libros", json=libro)


def reemplazar_libro(titulo, libro):
    return pedir("PUT", f"/libros/{titulo}", json=libro)


def borrar_libro(titulo):
    return pedir("DELETE", f"/libros/{titulo}")


def describir(respuesta):
    if respuesta.status_code in (200, 201, 204):
        return "ok"
    if respuesta.status_code == 422:
        return "dato inválido"
    if respuesta.status_code == 404:
        return "no existe"
    return f"respuesta inesperada ({respuesta.status_code})"


def mostrar(nombre, respuesta):
    if respuesta is None:
        return
    print(f"{nombre}: {describir(respuesta)} (código {respuesta.status_code})")


if __name__ == "__main__":
    libro = {"titulo": "Cliente Demo", "paginas": 100}

    respuesta = crear_libro(libro)
    mostrar("Crear", respuesta)
    if respuesta is None:
        raise SystemExit("Sin conexión: se cancela la demo.")

    respuesta = listar_libros()
    titulos = [item["titulo"] for item in respuesta.json()]
    print("Títulos en la API:", titulos)

    libro_nuevo = {"titulo": "Cliente Demo", "paginas": 200}
    respuesta = reemplazar_libro("Cliente Demo", libro_nuevo)
    mostrar("Reemplazar", respuesta)
    print("Quedó así:", respuesta.json())

    mostrar("Borrar", borrar_libro("Cliente Demo"))
    mostrar("Buscar después de borrar", obtener_libro("Cliente Demo"))
    