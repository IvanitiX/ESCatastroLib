# Municipio

**Módulo:** `services`

Wrapper de servicio que valida y busca municipios via el cliente catastral.
Equivalente al Municipio original: valida que el municipio existe
y lanza excepciones con sugerencias si no se encuentra.
**Argumentos:**

- `provincia` — Nombre o código de la provincia.
- `municipio` — Nombre del municipio. Si no se proporciona, lanza excepción.

**Excepciones:**

- `Exception` — Si no se especifica el municipio o si no se encuentra.

**Atributos:**

- `municipio` — Nombre del municipio (str).
- `provincia` — Nombre de la provincia (str).


## Métodos

### `__init__(provincia: str, municipio: str | None)`

*Sin documentación.*

---
