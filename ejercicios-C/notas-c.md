# Clase 2 - Parte C: notas

## C3 - "En /docs andaba y acá no"

Al mandar el POST con `data=libro`, la API respondió `422`. La diferencia con
`/docs` es cómo viaja el cuerpo:

- `/docs` manda el cuerpo como **JSON** y con el header
  `Content-Type: application/json`.
- `requests.post(..., data=libro)` manda el diccionario como **formulario**
  (`titulo=Experimento&paginas=99`), que no es JSON. La API esperaba un objeto
  y recibió texto plano, por eso el 422 dice que el cuerpo tiene que ser un
  diccionario u objeto.
- Mandar el JSON como texto (`data=json.dumps(libro)`) sin el header
  `Content-Type: application/json` falla igual, porque el servidor no sabe que
  ese texto es JSON.

La solución es usar `json=libro`: `requests` convierte el diccionario a JSON y
agrega el header solo.

Otros dos errores típicos que quedaron probados:

- URL distinta (`/libro` en vez de `/libros`): responde `404`.
- Puerto distinto (`8001` en vez de `8000`): no hay nadie escuchando y
  `requests` lanza `ConnectionError`.

La URL, el puerto y el path tienen que coincidir exactamente con los de la API.


## C6 - Cuando la API no está levantada

Con el servidor apagado, `requests` lanza `requests.exceptions.ConnectionError`
(el traceback termina con "Max retries exceeded ... Failed to establish a new
connection"). Lo atrapo con un `try/except` en la función `pedir`, que imprime
"No se pudo conectar con la API. ¿Está levantada?" y devuelve `None`, en vez
de dejar que el script explote.


## C7 - Timeout

Sin `timeout`, si el servidor nunca contesta, `requests` espera indefinidamente
y el script se queda colgado para siempre. Con `timeout=5`, después de 5
segundos lanza una excepción de la familia `requests.exceptions.Timeout` y el
script puede avisar y seguir.

Para verlo de verdad se usa una IP que nadie contesta (`10.255.255.1`) con
`timeout=1`: el pedido queda esperando y el timeout salta siempre. Contra
`localhost` no es confiable, porque la respuesta local puede llegar en menos de
un milisegundo, antes de que venza cualquier timeout razonable, y entonces el
ejercicio "no funciona" sin que se haya hecho nada mal.

Detalle al atrapar excepciones: `ConnectTimeout` hereda tanto de `Timeout` como
de `ConnectionError`. Por eso en `pedir` el `except` de `Timeout` va antes que
el de `ConnectionError`; si no, un timeout de conexión se mostraría como "no se
pudo conectar".


## C8 - Session

`requests.get`/`requests.post` sueltos abren una conexión nueva con el servidor
en cada pedido. Una `requests.Session()` mantiene la conexión abierta y la
reutiliza en los pedidos siguientes al mismo servidor, así que se ahorra ese
trabajo cada vez. Con muchos pedidos seguidos se nota: en `c8_medicion.py`, con
Session los 200 pedidos tardaron menos que sin ella.

