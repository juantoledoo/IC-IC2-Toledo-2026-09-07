# Clase 2 - Parte A: entender HTTP antes de escribir nada

## A1 - Verbo correcto

| Acción | Verbo | Por qué |
|---|---|---|
| (a) Ver la lista de libros | GET `/libros` | Solo lee datos, no modifica nada. |
| (b) Agregar un libro nuevo | POST `/libros` | Crea un recurso nuevo dentro de la colección. |
| (c) Borrar un libro | DELETE `/libros/{id}` | Elimina un recurso puntual. |
| (d) Cambiarle el precio a un libro | PATCH `/libros/{id}` | Se manda solo el campo `precio`, o sea una modificación parcial. |
| (e) Reemplazar un libro entero por otro | PUT `/libros/{id}` | Se manda el libro completo y reemplaza al anterior. |
| (f) Cambiarle solo la disponibilidad | PATCH `/libros/{id}` | Se manda solo el campo `disponible` y el resto queda como estaba. |

**Diferencia entre (e) y (f):** con PUT se manda el libro completo y todo lo que
no venga en el pedido se pierde o se reemplaza. Con PATCH se manda solo el campo
que cambia y los demás campos no se tocan.

## A2 - Códigos de estado, con ejemplos de libros

- **200 (OK):** `GET /libros` devuelve la lista de libros sin problemas.
- **201 (Created):** `POST /libros` con un libro válido y el libro quedó creado.
- **204 (No Content):** `DELETE /libros/Rayuela` borró el libro y no hay nada
  que devolver, así que la respuesta no lleva cuerpo.
- **400 (Bad Request):** el cuerpo del POST ni siquiera es un JSON válido, por
  ejemplo falta cerrar una llave.
- **404 (Not Found):** `GET /libros/LibroQueNoExiste`: el libro que se pide no existe.
- **405 (Method Not Allowed):** `DELETE /libros`: la URL existe, pero solo acepta
  GET y POST. Lo que sobra es el verbo.
- **422 (Unprocessable Entity):** `POST /libros` con un JSON bien escrito, pero
  sin el campo `paginas` o con `"paginas": "muchas"`. Se entendió el pedido, pero
  no cumple el contrato.
- **500 (Internal Server Error):** un bug del servidor, por ejemplo la API se cae
  al armar la respuesta porque el código intenta usar un campo que no existe.
  No es culpa de quien hizo el pedido.

## A3 - Familias de códigos

- **2xx:** el pedido salió bien.
- **3xx:** redirección, lo que se pidió está en otro lado y hay que ir a buscarlo ahí.
- **4xx:** el cliente se equivocó (pidió mal o pidió algo que no existe).
- **5xx:** el servidor se rompió, no es culpa de quien pidió.

Clasificando códigos que no vimos: **301** empieza con 3, es una redirección
(lo que pediste se movió a otra dirección). **403** empieza con 4, es un error
del cliente (el servidor entendió el pedido pero no tiene permiso para hacerlo).

## A4 - JSON a mano

Un libro:

```json
{
  "titulo": "El Aleph",
  "autor": "Jorge Luis Borges",
  "paginas": 180,
  "disponible": true
}
```

Una lista de 2 libros:

```json
[
  {
    "titulo": "El Aleph",
    "autor": "Jorge Luis Borges",
    "paginas": 180,
    "disponible": true
  },
  {
    "titulo": "Rayuela",
    "autor": "Julio Cortazar",
    "paginas": 600,
    "disponible": false
  }
]
```

Un libro con un campo anidado (`editorial`):

```json
{
  "titulo": "El Aleph",
  "autor": "Jorge Luis Borges",
  "paginas": 180,
  "disponible": true,
  "editorial": {
    "nombre": "Sudamericana",
    "pais": "Argentina"
  }
}
```

Se parece mucho a un diccionario de Python: las llaves `{}` son el diccionario,
los corchetes `[]` son la lista, y un diccionario adentro de otro en Python
es lo mismo que un objeto anidado en JSON. Las diferencias de escritura: en
JSON los textos van siempre con comillas dobles y los booleanos se escriben
`true` y `false` (en minúscula), no `True` y `False`.

## A5 - Idempotencia

Un pedido es **idempotente** si hacerlo una vez o cien veces seguidas deja el
mismo resultado final.

- **GET:** idempotente, solo lee.
- **PUT:** idempotente, siempre reemplaza por lo mismo.
- **DELETE:** idempotente, después de borrar una vez el recurso ya no existe, y
  volver a borrarlo no cambia ese estado final (la segunda respuesta puede ser
  un 404, pero el estado del sistema es el mismo).
- **POST:** normalmente **no** es idempotente, porque cada vez crea un recurso nuevo.

Si un mismo POST de "crear libro" se manda dos veces por un error de red (el
cliente no supo si el primero llegó y reintentó), se crean dos libros iguales.
Con un PUT que reemplaza por lo mismo, en cambio, mandarlo dos veces deja el
libro exactamente igual.

## A6 - Headers: `Content-Type`

El header `Content-Type: application/json` le dice al servidor **cómo
interpretar el cuerpo** del pedido: "lo que te mando es JSON, leelo así". No es
decorativo. Si un cliente manda un cuerpo JSON sin ese header, el servidor puede
no entenderlo como JSON y rechazarlo o tratarlo como texto, aunque el cuerpo esté
perfectamente escrito. Es una causa típica de "en `/docs` andaba y desde mi
script no".

## A7 - Diseñar URLs (REST básico)

| Qué se quiere hacer | Verbo y URL |
|---|---|
| Listar todos los libros | GET `/libros` |
| Ver un libro puntual | GET `/libros/{id}` |
| Listar los libros de un autor puntual | GET `/autores/{id}/libros` |
| Crear un autor | POST `/autores` |

Las URLs usan **sustantivos** (`libros`, `autores`), no verbos. La acción la
indica el verbo HTTP: por eso no hay `/getLibros` ni `/crearAutor`.
