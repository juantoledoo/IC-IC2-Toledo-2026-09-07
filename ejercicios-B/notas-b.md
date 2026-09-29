# Clase 2 - Parte B: notas

## B4 - Provocar el 422

**1. POST sin el campo `paginas`** -> `422`

```json
{"detail":[{"type":"missing","loc":["body","paginas"],"msg":"Field required","input":{"titulo":"Sin paginas"}}]}
```

`loc` indica dónde está el problema (campo `paginas` del `body`) y `msg` que el
campo es obligatorio y no se mandó.

**2. POST con `paginas: "muchas"`** -> `422`

```json
{"detail":[{"type":"int_parsing","loc":["body","paginas"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"muchas"}]}
```

El campo llegó, pero el tipo es incorrecto: la API esperaba un entero y recibió texto.

**3. POST con un campo de más (`editorial`)** -> `201`

FastAPI **ignora** el campo que el modelo no espera: no da error, y el campo
no se guarda ni aparece en la respuesta.


## B7 - DELETE y código de estado

Cuando el borrado sale bien devuelvo `204 (No Content)`: la operación se hizo
y no hay nada útil para devolver (el libro ya no existe), y por definición un
204 no lleva cuerpo. Si el libro no existe devuelvo `404`. Después de borrar,
un GET a ese título da 404.


## B8 - Validación propia de `paginas`

Un libro con `paginas` menor o igual a 0 se rechaza con `422`, usando
`Field(gt=0)` en el modelo. Elegí 422 y no 400 porque el JSON está bien armado
y el campo tiene el tipo correcto (un entero), pero el valor no cumple el
contrato del modelo. El cuerpo de la respuesta explica el motivo:
`Input should be greater than 0`.


## B12 - Valores por defecto y `response_model`

`disponible: bool = True` es un valor por defecto: si el POST no manda ese
campo, el modelo lo asume `True`. `response_model` sirve para indicarle a
FastAPI qué forma tiene la respuesta y filtrar lo que se devuelve: si el objeto
interno tiene un campo que no debe salir (por ejemplo un precio de costo), un
`response_model` sin ese campo evita que se filtre al cliente.

