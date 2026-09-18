# Calle

**Módulo:** `services`

Wrapper de servicio que valida y busca calles via el cliente catastral.
Equivalente a la Calle original: busca la calle en el municipio
y lanza excepciones con sugerencias si no se encuentra.
**Argumentos:**

- `municipio` — Objeto Municipio al que pertenece la calle.
- `nombre_calle` — Nombre de la calle. Si no se proporciona, lanza excepción.
- `tipo_via` — Tipo de vía (ej. "CL", "AV"). Opcional.

**Excepciones:**

- `Exception` — Si no se especifica la calle o si no se encuentra.

**Atributos:**

- `calle` — Nombre de la calle (str).
- `tipo_via` — Tipo de vía (str).
- `municipio` — Objeto Municipio.


## Métodos

### `__init__(municipio, nombre_calle, tipo_via)`

*Sin documentación.*

---
