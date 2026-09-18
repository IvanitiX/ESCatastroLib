# CatastroESClient

**Módulo:** `clients`

**Hereda de:** `BaseCatastroClient`

Cliente principal para consultar el Catastro español.
Punto de entrada principal de la librería. Orquesta providers, parsers
y composers para ofrecer una API simplificada de consulta catastral.
Hereda de ``BaseCatastroClient`` para funcionalidad compartida.
Ejemplo::
client = CatastroESClient(include_geometries=True)
parcelas = client.obtener_parcela_por_rc("12345678901234AA1234F")
**Argumentos:**

- `proyeccion` — Sistema de referencia para coordenadas (default "EPSG4326"). Debe ser uno de los soportados en SISTEMAS_REFERENCIA.
- `include_geometries` — Si True, incluye la geometría INSPIRE de la parcela.
- `include_values` — Si True, incluye valoración del suelo (urbano o rústico).
- `anio_valores` — Año de consulta para valores catastrales. Default año actual.
- `include_regions` — Si True, incluye las regiones catastrales.
- `include_constructions` — Si True, incluye construcciones (edificios, partes, etc.).
- `include_documentation` — Si True, incluye documentos asociados (croquis).
- `force_complete` — Si True, cuando hay múltiples resultados en una búsqueda por polígono/dirección, reconsulta individualmente por RC para obtener datos completos.

**Atributos:**

- `providers` — Contenedor de providers HTTP para cada API.
- `composer` — Composer para ensamblar el modelo ParcelaCatastral.


## Métodos

### `__init__(proyeccion, include_geometries, include_values, anio_valores, include_regions, include_constructions, include_documentation, force_complete)`

*Sin documentación.*

---

### `obtener_provincias()`

Consulta la lista de provincias españolas del Catastro.
**Retorna:**

- list[ProvinciaDTO]: Lista de provincias con código y nombre.


---

### `buscar_municipios(provincia, municipio)`

Busca municipios por provincia y nombre.
**Argumentos:**

- `provincia` — Código de provincia (2 dígitos) o nombre.
- `municipio` — Nombre del municipio a buscar.

**Retorna:**

- list[MunicipioDTO]: Lista de municipios que coinciden con la búsqueda.


---

### `buscar_calles(provincia, municipio, tipo_via, nombre_calle)`

Busca calles dentro de un municipio.
**Argumentos:**

- `provincia` — Código de provincia o nombre.
- `municipio` — Nombre del municipio.
- `tipo_via` — Tipo de vía para filtrar (ej. "Calle", "Avenida"). Vacío para buscar todos los tipos.
- `nombre_calle` — Nombre de la calle a buscar. Vacío para listar todas.

**Retorna:**

- list[CalleDTO]: Lista de calles encontradas.


---

### `geocodificar(direccion, municipio)`

Geocodifica una dirección usando CartoCiudad.
Convierte una dirección textual en coordenadas geográficas y
referencia catastral.
**Argumentos:**

- `direccion` — Dirección a geocodificar (ej. "Calle Mayor 1").
- `municipio` — Nombre del municipio.

**Retorna:**

- CartoCiudadDTO | None: Resultado con coordenadas, referencia catastral y código postal, o None si no se encuentra.


---

### `rc_por_coordenadas(lat, lon)`

Obtiene la referencia catastral a partir de coordenadas geográficas.
**Argumentos:**

- `lat` — Latitud en grados decimales.
- `lon` — Longitud en grados decimales.

**Retorna:**

- list[RefCatDTO]: Lista de referencias catastrales que contienen las coordenadas proporcionadas.


---

### `coordenadas_por_rc(rc)`

Convierte una referencia catastral a coordenadas geográficas.
**Argumentos:**

- `rc` — Referencia catastral (14 primeros caracteres del parcelario).

**Retorna:**

- list[CentroideDTO]: Lista de centroides con coordenadas y sistema de referencia.


---

### `obtener_parcela_por_rc(rc)`

Obtiene la información completa de una parcela por su referencia catastral.
Este es el método principal para obtener datos de una parcela. Si
están habilitadas las opciones (geometrías, valores, construcciones,
documentación), realiza las consultas adicionales necesarias.
**Argumentos:**

- `rc` — Referencia catastral de 20 caracteres (ej. "12345678901234AA1234F").

**Retorna:**

- list[ParcelaCatastral]: Lista con una o más parcelas que coinciden con la referencia.


---

### `obtener_parcela_por_polpar(provincia, municipio, poligono, parcela)`

Obtiene información de parcelas por polígono y número de parcela.
Busca todas las parcelas dentro de un polígono catastral de un municipio.
Si ``force_complete`` está activado y hay múltiples resultados, consulta
individualmente cada parcela por RC para obtener datos completos.
**Argumentos:**

- `provincia` — Código de provincia o nombre.
- `municipio` — Nombre del municipio.
- `poligono` — Número de polígono catastral.
- `parcela` — Número de parcela dentro del polígono.

**Retorna:**

- list[ParcelaCatastral]: Lista de parcelas encontradas.


---

### `obtener_parcela_por_direccion(provincia, municipio, tipo_via, calle, numero)`

Obtiene información de una parcela por su dirección completa.
Busca la parcela que se encuentra en la dirección indicada. Si
``force_complete`` está activado y hay múltiples resultados, consulta
individualmente cada parcela por RC para obtener datos completos.
**Argumentos:**

- `provincia` — Código de provincia o nombre.
- `municipio` — Nombre del municipio.
- `tipo_via` — Tipo de vía (ej. "Calle", "Avenida", "Plaza").
- `calle` — Nombre de la calle.
- `numero` — Número de la parcela en la calle.

**Retorna:**

- list[ParcelaCatastral]: Lista de parcelas encontradas en la dirección.


---
