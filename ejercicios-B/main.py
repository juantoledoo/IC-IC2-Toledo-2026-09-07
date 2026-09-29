from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Libro(BaseModel):
    titulo: str
    paginas: int


libros = [
    Libro(titulo="El Aleph", paginas=180),
    Libro(titulo="Rayuela", paginas=600),
    Libro(titulo="Ficciones", paginas=200),
]


@app.get("/")
def raiz():
    return {"mensaje": "hola"}


@app.get("/libros")
def listar_libros():
    return libros


@app.post("/libros", status_code=201)
def crear_libro(libro: Libro):
    libros.append(libro)
    return libro
