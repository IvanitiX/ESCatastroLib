# Building

**Módulo:** `models`

**Hereda de:** `Construction`

Edificio completo (BU.BUILDING).
Contiene la información principal de un edificio catastral, incluyendo
su uso, unidades, viviendas y una lista de BuildingPart que lo componen.
**Atributos:**

- `uso_actual` — Uso principal del edificio (ej. "Residencial", "Comercial").
- `num_unidades` — Número total de unidades del edificio.
- `num_viviendas` — Número de viviendas.
- `num_plantas_sup` — Número de plantas sobre rasante.
- `area_oficial` — Superficie oficial del edificio en m².
- `building_parts` — Lista de partes constructivas del edificio.


## Atributos

| Atributo | Tipo | Default |
|----------|------|---------|
| `uso_actual` | `str | None` | `None` |
| `num_unidades` | `int | None` | `None` |
| `num_viviendas` | `int | None` | `None` |
| `num_plantas_sup` | `int | None` | `None` |
| `area_oficial` | `float | None` | `None` |
| `building_parts` | `list[BuildingPart]` | `field(default_factory=list)` |
