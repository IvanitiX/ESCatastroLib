# CoordenadasAPIProvider

**Módulo:** `providers`

Provider para consultas de coordenadas del Catastro de España.
Proporciona métodos para convertir entre referencias catastrales (RC)
y coordenadas geográficas, así como obtener coordenadas de parcelas.
**Atributos:**

- `URL_BASE` — URL base del servicio de coordenadas del Catastro.


## Métodos

### `consulta_rc_por_coordenadas(lat: float, lon: float, sr: str)`

Convierte coordenadas X e Y a una referencia catastral (RC).
**Argumentos:**

- lat (float): Latitud. lon (float): Longitud. sr (str): Sistema de referencia. Por defecto es 'EPSG:4326'.

**Retorna:**

- `str` — Referencia catastral (RC).


---

### `convertir_rc_a_coordenadas(rc: str, sr: str)`

Convierte una referencia catastral (RC) a coordenadas X e Y.
**Argumentos:**

- rc (str): Referencia catastral. sr (str): Sistema de referencia. Por defecto es 'EPSG:4326'.

**Retorna:**

- `dict` — Un diccionario con las coordenadas X e Y.


---
