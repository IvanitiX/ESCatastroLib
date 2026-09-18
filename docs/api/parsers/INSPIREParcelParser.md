# INSPIREParcelParser

**Módulo:** `parsers`

Parser de respuestas INSPIRE CP (Cadastral Parcels) en formato WFS XML.
Extrae la geometría de una parcela catastral desde el servicio INSPIRE
de parcelas. Recupera:
- Geometría ``MultiSurface`` como polígono de vértices.
- Punto de referencia (centroide) como ``Point``.
- Valor del área de la parcela.

## Métodos

### `parse(response)`

Parsea una respuesta WFS XML de parcelas INSPIRE CP.
**Argumentos:**

- `response` — Objeto requests.Response con contenido XML GML/WFS.

**Retorna:**

- `INSPIREParcelDTO` — DTO con geometría, centroide y área de la parcela.

**Excepciones:**

- `ValueError` — Si el contenido está vacío o la API retorna una excepción.


---
