# ParcelaCatastral

**Módulo:** `models`

Modelo principal que representa una parcela catastral completa.
Modelo de dominio central de la librería. Integra toda la información
disponible de una parcela: identificación, ubicación, superficies,
construcciones, geometría, documentación y valoraciones.
**Atributos:**

- `referencia_catastral` — Referencia catastral de la parcela (20 caracteres).
- `municipio` — Municipio al que pertenece la parcela.
- `tipo` — Tipo de parcela "Urbano" o "Rústico".
- `completo` — True si la información es completa, False si es parcial.
- `superficie_plana` — Superficie de la parcela en m² (suelo).
- `superficie_construida` — Superficie total construida en m².
- `datos_urbanos` — Datos específicos urbanos, o None si es rústica.
- `datos_rusticos` — Datos específicos rústicos, o None si es urbana.
- `regiones` — Lista de regiones catastrales de la parcela.
- `construcciones` — Lista de construcciones sobre la parcela.
- `geometria` — Geometría de la parcela, o None si no está disponible.
- `documentacion` — Documentos asociados (croquis, planos, etc.).
- `valor_urbano` — Valoración urbana del suelo, o None.
- `valor_rustico` — Valoración rústica del suelo, o None.


## Atributos

| Atributo | Tipo | Default |
|----------|------|---------|
| `referencia_catastral` | - | - |
| `municipio` | - | - |
| `tipo` | - | - |
| `completo` | - | - |
| `superficie_plana` | - | - |
| `superficie_construida` | - | - |
| `datos_urbanos` | - | - |
| `datos_rusticos` | - | - |
| `regiones` | - | - |
| `construcciones` | - | - |
| `geometria` | - | - |
| `documentacion` | - | - |
| `valor_urbano` | - | - |
| `valor_rustico` | - | - |

## Métodos

### `perimetro()` *(property)*

Perímetro de la parcela en metros lineales.

---
