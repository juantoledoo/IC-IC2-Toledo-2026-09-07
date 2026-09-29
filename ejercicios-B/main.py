from fastapi import FastAPI

app = FastAPI()

libros = [
    {"titulo": "El Aleph", "paginas": 180},
    {"titulo": "Rayuela", "paginas": 600},
    {"titulo": "Ficciones", "paginas": 200},
]


@app.get("/")
def raiz():
    return {"mensaje": "hola"}


@app.get("/libros")
def listar_libros():
    return libros
