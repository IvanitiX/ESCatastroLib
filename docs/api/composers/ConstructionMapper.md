# ConstructionMapper

**Módulo:** `composers`

Mapper que dispatcha DTOs de construcción a sus modelos de dominio.
Detecta el tipo de DTO (BuildingPart, Building, OtherConstruction)
inspeccionando sus atributos y crea la instancia correspondiente del
modelo de dominio.

## Métodos

### `@staticmethod map()`

Convierte un DTO de construcción INSPIRE a su modelo de dominio.
Detecta el tipo inspeccionando atributos:
- ``height_below_ground_m`` o ``number_of_floors_below_ground`` → BuildingPart
- ``current_use`` o ``number_of_building_units`` → Building
- ``construction_nature`` → OtherConstruction
**Argumentos:**

- `dto` — DTO de construcción INSPIRE (ConstructionBaseDTO).

**Retorna:**

- `Construction` — Modelo de dominio correspondiente (BuildingPart, Building u OtherConstruction).

**Excepciones:**

- `ValueError` — Si el tipo de construcción no es reconocido.


---
