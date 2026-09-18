# Geometria

**Módulo:** `models`

Geometría catastral de una parcela o construcción.
Almacena las coordenadas de una geometría junto con su sistema de
referencia y tipo. Proporciona conversión a objetos Shapely y
propiedades calculadas de área y perímetro.
**Atributos:**

- `sistema_referencia` — Código del sistema de referencia (ej. "EPSG4258").
- `coordenadas` — Lista de coordenadas. Para Point es una tupla (x, y), para Polygon es una lista de tuplas [(x1,y1), (x2,y2), ...].
- `tipo` — Tipo de geometría "Point" o "Polygon".


## Atributos

| Atributo | Tipo | Default |
|----------|------|---------|
| `sistema_referencia` | `str` | - |
| `coordenadas` | `list` | - |
| `tipo` | `str` | - |

## Métodos

### `to_shapely()`

Convierte la geometría a un objeto Shapely.
**Retorna:**

- Point o Polygon de Shapely según el tipo, o None si no se puede convertir.


---

### `area()` *(property)*

Área de la geometría en unidades cuadradas del sistema de referencia.

---

### `perimetro()` *(property)*

Perímetro de la geometría en unidades lineales del sistema de referencia.

---
