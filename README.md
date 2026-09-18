# ESCatastroLib

Una librería de Python para consultar los datos del Catastro de España en base a objetos y obtener información geográfica precisa. Con esta librería, puedes acceder a datos como la ubicación de parcelas, características de construcción y valores geográficos.

## Arquitectura: ¡Ahora con capas!

Con respecto a la v1 de ESCatastroLib, ahora la librería se basa una arquitectura por capas que separa las responsabilidades:

|Path|¿Qué lleva?| Más info|
|----|-----------|---------|
|services/|Facade de alto nivel, agnóstico a territorio (casi todo lo llevarás desde aquí)|[Documentación](./docs/api/services/)|
|clients/|Clientes por territorios|[Documentación](./docs/api/clients/)|
|composers/|Composición de DTO a modelos comunes|[Documentación](./docs/api/composers/)|
|parsers/|Parseo XML/JSON a DTOS|[Documentación](./docs/api/parsers/)|
|providers/|Todas las peticiones HTTP SOAP/REST|[Documentación](./docs/api/providers/)|
|models/|Modelos de dominio comunes|[Documentación](./docs/api/models/)|
|exporters/|Exportación de parcelas a JSON, CSV, GeoJSON... (algunos requieren módulos extra)|[Documentación](./docs/api//exporters/)|



## Instalación

```bash
# Soporta todo la arquitectura y las exportaciones a CSV y (Geo)JSON
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
parcela = ParcelaCatastral(rc='28067A023001490000FJ')

# Exportar a JSON
from escatastrolib.exporters import to_json
json_parcela = to_json(parcela.parcelas)

# Exportar a GeoJSON, guardado en disco
from escatastrolib.exporters import to_geojson
to_geojson(parcela.parcelas,"parcela_geo.json")
```

# ¿Cómo puedo contribuir?
Sigue las instrucciones de CONTRIBUTING.md y el Código de Conducta.

# Agradecimientos
- Al Catastro por hacer un Endpoint público.
- A GISCE-TI por currarse [una librería similar][1], basándose en los endpoints JSON.
- A mi abuelo y mi tío por pedirme que os eche una mano buscando tierras.
- A [Juanlu Cano][2] por darme la idea de extender el primer concepto en la PyConES para convertirlo en esta librería.
- A [Jaime Gómez-Obregón][3] por animar de forma muuuy indirecta a "hackear las Administraciones públicas".

[1]: https://github.com/gisce/pycatastro
[2]: https://github.com/astrojuanlu
[3]: https://github.com/JaimeObregon