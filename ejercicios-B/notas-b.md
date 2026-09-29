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
