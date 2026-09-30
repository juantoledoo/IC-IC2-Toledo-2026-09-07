from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_listar_libros_responde_200():
    respuesta = client.get("/libros")
    assert respuesta.status_code == 200


def test_post_sin_paginas_devuelve_422():
    respuesta = client.post("/libros", json={"titulo": "Sin paginas"})
    assert respuesta.status_code == 422


def test_post_con_paginas_de_tipo_incorrecto_devuelve_422():
    respuesta = client.post("/libros", json={"titulo": "Mucho", "paginas": "muchas"})
    assert respuesta.status_code == 422


def test_post_libro_valido_devuelve_201():
    respuesta = client.post("/libros", json={"titulo": "Libro valido", "paginas": 120})
    assert respuesta.status_code == 201


def test_post_libro_invalido_devuelve_422():
    respuesta = client.post("/libros", json={"titulo": "Libro invalido", "paginas": 0})
    assert respuesta.status_code == 422


def test_post_y_luego_get_muestra_el_libro_nuevo():
    nuevo = {"titulo": "Libro encadenado", "paginas": 77}
    respuesta_post = client.post("/libros", json=nuevo)
    assert respuesta_post.status_code == 201

    respuesta_get = client.get("/libros")
    titulos = [libro["titulo"] for libro in respuesta_get.json()]
    assert "Libro encadenado" in titulos

    