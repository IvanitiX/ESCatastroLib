# GeometriaMapper

**Módulo:** `composers/mappers`

Mapper que convierte GeometriaDTO a Geometria (modelo de dominio).
Transforma la lista de puntos del DTO en tuplas de coordenadas
compatibles con el modelo ``Geometria`` y Shapely.

## Métodos

### `@staticmethod map()`

Convierte un GeometriaDTO a un modelo Geometria.
**Argumentos:**

- `dto` — GeometriaDTO con puntos, sistema de referencia y tipo.

**Retorna:**

- `Geometria` — Modelo de dominio con coordenadas como tuplas (x, y).


---
