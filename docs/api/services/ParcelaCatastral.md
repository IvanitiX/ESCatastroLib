# ParcelaCatastral

**Módulo:** `services`

Servicio de parcelas catastrales con interfaz de constructor directo.
Permite consultar parcelas catastrales de forma similar al original:
se instancia con los parámetros de búsqueda y los datos se cargan
automáticamente en self.parcelas.
**Argumentos:**

- `rc` — Referencia catastral (20 caracteres).
- `provincia` — Nombre o código de la provincia.
- `municipio` — Nombre o código del municipio.
- `poligono` — Número de polígono (búsqueda por parcela).
- `parcela` — Número de parcela (búsqueda por parcela).
- `tipo_via` — Tipo de vía (búsqueda por dirección).
- `calle` — Nombre de la calle (búsqueda por dirección).
- `numero` — Número de la dirección (búsqueda por dirección).
- `projection` — Sistema de referencia espacial. Default "EPSG4326".
- `include_geometries` — Si True, incluye geometría INSPIRE.
- `include_values` — Si True, incluye valoración del suelo.
- `anio_valores` — Año de consulta para valores catastrales.
- `include_regions` — Si True, incluye regiones catastrales.
- `include_constructions` — Si True, incluye construcciones.
- `include_documentation` — Si True, incluye documentos (croquis).
- `force_complete` — Si True, re-consulta por RC cuando hay múltiples resultados.

**Excepciones:**

- `ValueError` — Si no se proporciona suficiente información para la búsqueda.

**Atributos:**

- `parcelas` — Lista de parcelas catastrales encontradas (list[ParcelaCatastralModel]).


## Métodos

### `__init__(rc: str | None, provincia: str | None = None, municipio: str | None = None, poligono: int | None = None, parcela: int | None = None, tipo_via: str | None = None, calle: str | None = None, numero: str | None = None, projection: str = None, include_geometries: bool = 'EPSG:4326', include_values: bool = False, anio_valores: int | None = False, include_regions: bool = None, include_constructions: bool = False, include_documentation: bool = False, force_complete: bool = False)`

*Sin documentación.*

---

### `obtener_provincias()`

Consulta la lista de provincias españolas.

---

### `buscar_municipios(provincia: str, municipio: str)`

Busca municipios por provincia y nombre.

---

### `buscar_calles(provincia: str, municipio: str, tipo_via: str, nombre_calle: str = '')`

Busca calles dentro de un municipio.

---

### `geocodificar(direccion: str, municipio: str)`

Geocodifica una dirección usando CartoCiudad.

---

### `rc_por_coordenadas(lat: float, lon: float)`

Obtiene la referencia catastral a partir de coordenadas.

---

### `coordenadas_por_rc(rc: str)`

Convierte una referencia catastral a coordenadas.

---
