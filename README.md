# ESCatastroLib

Una librería de Python para consultar los datos del Catastro de España y obtener información geográfica precisa. Con esta librería, puedes acceder a datos como la ubicación de parcelas, características de construcción y valores geográficos.

## Arquitectura v2

ESCatastroLib v2 utiliza una arquitectura por capas que separa las responsabilidades:

```
┌─────────────────────────────────────────────┐
│  services/          (Facade de alto nivel)  │
├─────────────────────────────────────────────┤
│  clients/           (Clientes HTTP)         │
├─────────────────────────────────────────────┤
│  composers/         (Composición de DTOs)   │
├─────────────────────────────────────────────┤
│  parsers/           (Parseo XML/JSON)       │
├─────────────────────────────────────────────┤
│  providers/         (HTTP SOAP/REST)        │
├─────────────────────────────────────────────┤
│  models/            (Modelos de dominio)    │
├─────────────────────────────────────────────┤
│  exporters/         (JSON, CSV, GeoJSON...) │
└─────────────────────────────────────────────┘
```

### Providers
Conectores HTTP de bajo nivel que interactúan con las APIs del Catastro.

### Parsers
Transforman las respuestas XML/JSON en DTOs internos.

### Composers
Combinan y transforman DTOs en modelos de negocio.

### Models
Dataclasses del dominio: ParcelaCatastral, Geometria, etc.

### Clients
Capa de alto nivel que orquesta providers + parsers + composers.

### Services
Facade más alto: una sola llamada para obtener una parcela completa.

### Exporters
Serialización a JSON, CSV, GeoJSON, GeoPackage, Shapefile, DataFrame.

## Instalación

```bash
pip install escatastrolib
```

### Dependencias opcionales

```bash
# Para exportar a DataFrame/Parquet
pip install escatastrolib[export]

# Para exportar a GeoPackage/Shapefile
pip install escatastrolib[gis]

# Todas las dependencias opcionales
pip install escatastrolib[all]
```

## Uso rápido

```python
from escatastrolib.services import ParcelaCatastral

# Obtener una parcela por referencia catastral
parcela = ParcelaCatastral.from_rc('28067A023001490000FJ')

# Exportar a JSON
parcela.to_json("parcela.json")

# Exportar a GeoJSON
parcela.to_geojson("parcela.geojson")
```

## Requisitos

- Python >= 3.10
- shapely >= 2.0.0
- pyproj >= 3.0.0

## Licencia

Apache License 2.0 - Ver [LICENSE](LICENSE) para más detalles.

## Contribuir

Sigue las instrucciones de [CONTRIBUTING.md](CONTRIBUTING.md) y el [Código de Conducta](CODE_OF_CONDUCT.md).

## Agradecimientos

- Al Catastro por hacer un Endpoint público.
- A GISCE-TI por currarse [una librería similar](https://github.com/gisce/pycatastro), basándose en los endpoints JSON.
