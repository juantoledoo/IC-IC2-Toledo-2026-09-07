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

    