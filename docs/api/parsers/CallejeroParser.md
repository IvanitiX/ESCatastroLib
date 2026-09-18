# CallejeroParser

**Módulo:** `parsers`

Parser base para las respuestas del API de Callejero del Catastro.
Maneja la validación de respuesta HTTP y la conversión a JSON.
Las subclases implementan ``_to_dtos()`` para extraer los DTOs
específicos de cada tipo de consulta.

## Métodos

### `parse(response)`

Valida la respuesta HTTP y delega la extracción a ``_to_dtos()``.
**Argumentos:**

- `response` — Objeto requests.Response con la respuesta de la API.

**Retorna:**

- `list` — Lista de DTOs extraídos de la respuesta.

**Excepciones:**

- `ValueError` — Si la respuesta no contiene JSON válido. requests.HTTPError: Si el código de estado indica error.


---
