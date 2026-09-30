from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_listar_libros_responde_200():
    respuesta = client.get("/libros")
    assert respuesta.status_code == 200
    