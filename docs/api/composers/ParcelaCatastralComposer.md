# ParcelaCatastralComposer

**Módulo:** `composers`

Orquestador que ensambla el modelo ParcelaCatastral desde DTOs.
Coordina la transformación de los diferentes DTOs obtenidos de las APIs
en el modelo de dominio ``ParcelaCatastral``. Utiliza mappers específicos
para cada tipo de dato y respeta los flags de configuración para incluir
o no información opcional (geometrías, valores, regiones, etc.).
**Argumentos:**

- `include_geometries` — Incluir geometría INSPIRE de la parcela.
- `include_values` — Incluir valoración del suelo (urbana o rústica).
- `include_regions` — Incluir regiones catastrales.
- `include_constructions` — Incluir construcciones (edificios, partes, etc.).
- `include_documentation` — Incluir documentos asociados (croquis).


## Métodos

### `__init__(include_geometries: bool, include_values: bool = False, include_regions: bool = False, include_constructions: bool = False, include_documentation: bool = False)`

*Sin documentación.*

---

### `compose(parcela_dto: ParcelaCatastralDTO, completo: bool = False, geometria_dto: INSPIREParcelDTO | None = None, croquis_dtos: list[CroquisDTO] | None = None, valor_urbano_dto: ValorUrbanoDTO | None = None, valor_rustico_dto: ValoresRusticosDTO | None = None, construcciones_dtos: list[ConstructionBaseDTO] | None = None)`

Ensbla un modelo ParcelaCatastral completo desde DTOs.
Orquesta la transformación de todos los DTOs obtenidos de las APIs
en el modelo de dominio. Utiliza los mappers correspondientes para
cada tipo de dato y respeta los flags de configuración.
**Argumentos:**

- `parcela_dto` — DTO con los datos base de la parcela del callejero.
- `completo` — Si True, marca la parcela como información completa.
- `geometria_dto` — DTO de geometría INSPIRE de la parcela (opcional).
- `croquis_dtos` — Lista de DTOs de croquis/documentación (opcional).
- `valor_urbano_dto` — DTO de valoración urbana del suelo (opcional).
- `valor_rustico_dto` — DTO de valoración rústica del suelo (opcional).
- `construcciones_dtos` — Lista de DTOs de construcciones INSPIRE BU (ConstructionBaseDTO) (opcional).

**Retorna:**

- `ParcelaCatastral` — Modelo de dominio completo con toda la información disponible de la parcela.


---
