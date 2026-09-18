# CatastroESProviders

**Módulo:** `clients`

Contenedor de todos los providers de acceso a APIs del Catastro.
Agrupa las instancias de los providers HTTP que conectan con los
diferentes servicios de la Sede Electrónica del Catastro y servicios
complementarios.
**Atributos:**

- `callejero` — Provider del API de callejero (provincias, municipios, calles, parcelas).
- `cartociudad` — Provider del geocodificador CartoCiudad.
- `coordenadas` — Provider del API de coordenadas del Catastro.
- `inspire_parcelas` — Provider INSPIRE CP para geometrías de parcelas.
- `inspire_buildings` — Provider INSPIRE BU para construcciones y edificios.
- `valores_urbanos` — Provider del Mapa de Valores Urbanos (GeoJSON).
- `valores_rusticos` — Provider del Mapa de Valores Rústicos (WMS).
- `croquis` — Provider para obtención de croquis catastrales.


## Atributos

| Atributo | Tipo | Default |
|----------|------|---------|
| `callejero` | - | - |
| `cartociudad` | - | - |
| `coordenadas` | - | - |
| `inspire_parcelas` | - | - |
| `inspire_buildings` | - | - |
| `valores_urbanos` | - | - |
| `valores_rusticos` | - | - |
| `croquis` | - | - |
