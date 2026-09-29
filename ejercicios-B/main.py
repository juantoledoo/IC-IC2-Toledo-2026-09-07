from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

app = FastAPI()


class Libro(BaseModel):
    titulo: str
    paginas: int = Field(gt=0)


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


@app.get("/libros/{titulo}")
def obtener_libro(titulo: str):
    for libro in libros:
        if libro.titulo == titulo:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.put("/libros/{titulo}")
def reemplazar_libro(titulo: str, libro_nuevo: Libro):
    for i in range(len(libros)):
        if libros[i].titulo == titulo:
            libros[i] = libro_nuevo
            return libro_nuevo
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.delete("/libros/{titulo}", status_code=204)
def borrar_libro(titulo: str):
    for i in range(len(libros)):
        if libros[i].titulo == titulo:
            libros.pop(i)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail="Libro no encontrado")
