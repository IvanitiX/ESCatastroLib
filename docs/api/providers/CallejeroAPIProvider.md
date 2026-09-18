# CallejeroAPIProvider

**Módulo:** `providers`

Provider para consultas al Catastro de España sobre callejero.
Proporciona métodos para consultar provincias, municipios, calles
y parcelas a través del servicio web del Catastro.
**Atributos:**

- `URL_BASE` — URL base del servicio de callejero del Catastro.


## Métodos

### `consulta_provincias()`

*Sin documentación.*

---

### `consulta_municipios(provincia: str, municipio: str | None)`

*Sin documentación.*

---

### `consulta_calles(provincia: str, municipio: str, tipo_via: str, nombre_calle: str = '')`

*Sin documentación.*

---

### `consulta_parcela_por_rc(rc: str)`

*Sin documentación.*

---

### `consulta_parcela_por_polpar(municipio: str, provincia: str, poligono: int, parcela: int)`

*Sin documentación.*

---

### `consulta_parcela_por_direccion(municipio: str, provincia: str, tipo_via: str, calle: str, numero: str)`

*Sin documentación.*

---
