# Clase 2 - Parte D: MQTT, solo el concepto

## D1 - Ver el mensaje viajar

Me conecté con dos pestañas del cliente web de HiveMQ al broker público
`broker.hivemq.com`. En una pestaña me suscribí al topic
`unraf/demo/toledo/saludo` y desde la otra publiqué `hola desde la pestaña B`:
el mensaje apareció del lado del suscriptor. Usé un topic con mi apellido porque
el broker es público y lo usa cualquiera, y no publiqué datos privados.

## D2 - Publicar sin suscriptores

Publiqué `mensaje 1` en `unraf/demo/toledo/sin-nadie` sin que nadie estuviera
suscripto: no hubo ningún error ni aviso del lado del que publica. Después me
suscribí y el `mensaje 1` no llegó: se perdió. Al publicar `mensaje 2`, ese sí
llegó.

Conclusión: el que publica no sabe ni le importa si hay alguien escuchando, y
un mensaje publicado antes de que alguien se suscriba, por defecto, se pierde.

## D3 - Pub/sub vs request/response

En request/response (la API de libros) el cliente pregunta y el servidor le
contesta en el momento, uno a uno. En pub/sub (MQTT) quien tiene un dato lo
publica en un topic sin saber quién escucha, y el broker se lo reparte a todos
los que estén suscriptos.

- Conviene **request/response** cuando necesito la respuesta ya, por ejemplo
  consultar un libro o guardar un dato y confirmar que se guardó.
- Conviene **pub/sub** cuando un dato lo producen muchos y lo consumen varios,
  por ejemplo un sensor de temperatura que publica cada 5 segundos y lo leen a
  la vez un tablero, una alarma y la base de datos.

## D4 - Topics y jerarquía

Los topics se organizan por niveles separados con `/`. Alguien que quiere todo
lo de la cocina se suscribe a `casa/cocina/#`, y recibe tanto `casa/cocina/temp`
como `casa/cocina/hum`.

Los wildcards se usan al suscribirse (no al publicar):

- `+` reemplaza **un solo nivel**. `casa/+/temp` recibe la temperatura de todos
  los ambientes (`casa/cocina/temp`, `casa/living/temp`), pero no
  `casa/cocina/hum`.
- `#` reemplaza **todos los niveles restantes** y tiene que ir al final.
  `casa/#` recibe todo lo que cuelga de `casa`, a cualquier profundidad.

Uso `+` para "este tipo de dato en todos los ambientes" y `#` para "todo un
subárbol".

## D5 - Diseñar los topics

Esquema: `casa/<ambiente>/<sensor>`, con 3 ambientes (cocina, living,
dormitorio) y 2 sensores (temp, hum):

| Topic |
|---|
| `casa/cocina/temp` |
| `casa/cocina/hum` |
| `casa/living/temp` |
| `casa/living/hum` |
| `casa/dormitorio/temp` |
| `casa/dormitorio/hum` |

Suscripciones con wildcards:

| Quiero | Me suscribo a |
|---|---|
| Todo | `casa/#` |
| Un ambiente (la cocina) | `casa/cocina/#` |
| Un tipo de sensor (temperatura) | `casa/+/temp` |

Justificación: la jerarquía va de lo general a lo específico (casa, ambiente,
sensor). Con el ambiente antes que el sensor, "todo un ambiente" se resuelve con
`#` al final y "un tipo de sensor en todos los ambientes" con `+` en el nivel del
medio. Los tres casos salen con una sola suscripción.

## D6 - QoS

- **QoS 0:** "como salga". Se envía una vez y no hay confirmación: puede
  perderse.
- **QoS 1:** "al menos una vez". El receptor confirma y, si no llega la
  confirmación, se reenvía. No se pierde, pero puede llegar duplicado.
- **QoS 2:** "exactamente una vez". Hay un intercambio de varios mensajes para
  garantizar que no se pierda ni se duplique. Es el más seguro y el más lento.

Para un sensor que publica la temperatura cada 2 segundos usaría **QoS 0**:
perder una lectura no importa, porque dos segundos después llega la siguiente,
y no vale la pena pagar el costo de las confirmaciones.

Para un comando de "abrir la puerta" usaría **QoS 1**: no puede perderse, y
recibirlo dos veces es inofensivo (abrir una puerta que ya está abierta no
cambia nada). Si en cambio un duplicado hiciera daño (por ejemplo, un comando
de "cobrar" o "dispensar una dosis"), usaría **QoS 2**.

## D7 - Mensajes retenidos (retained)

Un mensaje **retained** es un mensaje que el broker guarda (el último por
topic) y le entrega a cada cliente nuevo apenas se suscribe, aunque haya sido
publicado antes.

Diferencia con D2: en D2 el que se suscribía tarde se perdía el mensaje. Con
retained, el que se suscribe tarde recibe igual el último.

Se beneficia quien se conecta después y necesita el **último estado conocido**:
por ejemplo un tablero que se abre ahora y quiere ver la última temperatura
reportada sin esperar al próximo mensaje del sensor. No sirve para eventos que
solo importan en el momento (como "sonó el timbre").

## D8 - MQTT vs polling

Ejemplo aproximado: 1000 dispositivos, y cada uno genera un dato nuevo cada
5 segundos.

- **Polling** (cada cliente pregunta a la API "¿hay algo nuevo?" cada 1
  segundo): el servidor recibe unos **1000 pedidos por segundo**, y como el dato
  cambia una vez cada 5 segundos, 4 de cada 5 pedidos (unos **800 por segundo**)
  vuelven con "nada nuevo". Además, entre que pasa el evento y alguien se
  entera pasa hasta 1 segundo.
- **Pub/sub:** nadie pregunta. Solo viajan los datos reales: 1000 dispositivos
  cada 5 segundos son unos **200 mensajes por segundo**, todos útiles, y el
  broker los reparte apenas llegan, con una demora de milisegundos.

Con más dispositivos, el polling crece con la cantidad de preguntas (aunque no
haya nada nuevo) y pub/sub crece solo con la cantidad de datos reales. Por eso
pub/sub escala mejor.

