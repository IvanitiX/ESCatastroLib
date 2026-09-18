# ParcelaCatastralParser

**Módulo:** `parsers`

**Hereda de:** `CallejeroParser`

Parser de respuestas de consulta de parcelas catastrales.
Maneja la extracción de información completa de una parcela desde la API
del callejero. Soporta dos cardinalidades:
- Resultado único (``bico``): parcela completa con regiones y detalles.
- Resultados múltiples (``lrcdnp``): lista resumida de parcelas.
Detecta automáticamente si la parcela es urbana o rústica y extrae
los datos específicos accordingly.

## Métodos

### `parse(response: requests.Response)`

Parsea la respuesta de una consulta de parcela catastral.
Determina automáticamente la cardinalidad del resultado (único o
múltiples parcelas) y extrae la información correspondiente.
**Argumentos:**

- `response` — Objeto requests.Response con la respuesta de la API.

**Retorna:**

- list[ParcelaCatastralDTO]: Lista de parcelas extraídas.

**Excepciones:**

- `ValueError` — Si no hay resultados o la respuesta es inválida.


---
