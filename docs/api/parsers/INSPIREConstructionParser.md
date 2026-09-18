# INSPIREConstructionParser

**Módulo:** `parsers`

Parser de respuestas INSPIRE BU (Buildings) en formato WFS XML.
Extrae construcciones de las respuestas GML/WFS del servicio INSPIRE
de edificios del Catastro. Maneja tres tipos de entidades:
- ``BuildingPart``: partes constructivas de un edificio.
- ``Building``: edificios completos con uso, unidades y superficie oficial.
- ``OtherConstruction``: construcciones especiales (garajes, piscinas, etc.).
La geometría se extrae de ``gml:Surface`` con ``PolygonPatch``.

## Métodos

### `parse(response: requests.Response)`

Parsea una respuesta WFS XML de construcciones INSPIRE BU.
**Argumentos:**

- `response` — Objeto requests.Response con contenido XML GML/WFS.

**Retorna:**

- `list` — Lista de DTOs de construcción (BuildingPartDTO, BuildingDTO u OtherConstructionDTO).

**Excepciones:**

- `ValueError` — Si el contenido está vacío o la API retorna una excepción.


---
