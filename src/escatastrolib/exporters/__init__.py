"""Exportadores de parcelas catastrales.

Proporciona funciones para exportar modelos ParcelaCatastral a diferentes
formatos: JSON, CSV, GeoJSON, GeoPackage, Shapefile y DataFrame.

Los formatos base (JSON, CSV, GeoJSON) no requieren dependencias adicionales.
Los exportadores de GIS (GeoPackage, Shapefile) y DataFrame requieren
dependencias opcionales que se importan bajo demanda.

Ejemplo de uso::

    from escatastrolib.services import ParcelaCatastral
    from escatastrolib.exporters import to_json, to_geojson, to_csv

    servicio = ParcelaCatastral(rc="...")
    parcelas = servicio.parcelas

    to_json(parcelas, "salida.json")
    to_geojson(parcelas, "salida.geojson")
    to_csv(parcelas, "salida.csv")
"""

from .json_exporter import to_json
from .csv_exporter import to_csv
from .geojson_exporter import to_geojson

__all__ = [
    "to_json",
    "to_csv",
    "to_geojson",
    "to_geopackage",
    "to_shapefile",
    "to_dataframe",
]


def __getattr__(name: str):
    """Lazy import de exportadores que requieren dependencias opcionales."""
    if name == "to_geopackage":
        from .gis_exporters import to_geopackage

        return to_geopackage
    if name == "to_shapefile":
        from .gis_exporters import to_shapefile

        return to_shapefile
    if name == "to_dataframe":
        from .dataframe_exporter import to_dataframe

        return to_dataframe
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
