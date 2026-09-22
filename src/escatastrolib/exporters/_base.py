import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from shapely.geometry import mapping

from ..models.Construction import Building, BuildingPart, Construction, OtherConstruction
from ..models.Documentacion import Documento
from ..models.GeometriaCatastral import Geometria
from ..models.ParcelaCatastral import (
    ParcelaCatastral,
    ParcelaRustica,
    ParcelaUrbana,
)
from ..models.RegionCatastral import RegionCatastral
from ..models.ValorRustico import ValorRustico
from ..models.ValorUrbano import ValorUrbano


def _invert_coords(shapely_geom: Any) -> Any:
    """Invierte las coordenadas de una geometría Shapely (lat,lon) a (lon,lat).

    Args:
        shapely_geom: Geometría Shapely (Point, Polygon, etc.).

    Returns:
        Nueva geometría con coordenadas invertidas.
    """
    from shapely.ops import transform as shapely_transform

    return shapely_transform(lambda x, y: (y, x), shapely_geom)


def _geometria_to_wkt(
    geom: Geometria | None,
    *,
    invert_coordinates: bool = False,
) -> str:
    """Convierte una geometría catastral a WKT.

    Args:
        geom: Geometría catastral o None.
        invert_coordinates: Si True, invierte coordenadas de (lat,lon) a (lon,lat).

    Returns:
        Cadena WKT de la geometría, o cadena vacía si no hay geometría.
    """
    if not geom or not geom.coordenadas:
        return ""
    shapely_geom = geom.to_shapely()
    if shapely_geom is None:
        return ""
    if invert_coordinates:
        shapely_geom = _invert_coords(shapely_geom)
    return shapely_geom.wkt


def _geometria_to_geojson_dict(
    geom: Geometria | None,
    transformer: Any | None = None,
    precision: int = 6,
    *,
    invert_coordinates: bool = False,
) -> dict | None:
    """Convierte una geometría catastral a diccionario GeoJSON.

    Aplica reproyección si se proporciona un transformer de pyproj.
    Redondea las coordenadas al número de decimales indicado.

    Args:
        geom: Geometría catastral o None.
        transformer: Transformer de pyproj para reproyección, o None.
        precision: Número de decimales para las coordenadas.
        invert_coordinates: Si True, invierte coordenadas de (lat,lon) a (lon,lat).

    Returns:
        Diccionario GeoJSON con ``type`` y ``coordinates``, o None.
    """
    if not geom or not geom.coordenadas:
        return None

    shapely_geom = geom.to_shapely()
    if shapely_geom is None:
        return None

    if invert_coordinates:
        shapely_geom = _invert_coords(shapely_geom)

    if transformer is not None:
        from shapely.ops import transform as shapely_transform

        shapely_geom = shapely_transform(transformer.transform, shapely_geom)

    geojson = mapping(shapely_geom)

    def _round_coords(coords: Any) -> Any:
        if isinstance(coords, (list, tuple)):
            return [_round_coords(c) for c in coords]
        if isinstance(coords, float):
            return round(coords, precision)
        return coords

    geojson["coordinates"] = _round_coords(geojson["coordinates"])
    return geojson


def _make_crs_transformer(source_crs: str, target_crs: str) -> Any:
    """Crea un transformer de pyproj entre dos CRS.

    El Catastro devuelve coordenadas en orden lat/lon (nativo de EPSG:4258).
    Pyproj con always_xy=True espera lon/lat. Se usa always_xy=False para
    respetar el orden nativo del CRS de origen.

    Args:
        source_crs: Código EPSG de origen (ej. "EPSG:4258").
        target_crs: Código EPSG de destino (ej. "EPSG:25830").

    Returns:
        Transformer de pyproj para transformación de coordenadas.
    """
    from pyproj import Transformer

    return Transformer.from_crs(source_crs, target_crs, always_xy=False)


class _EnhancedEncoder(json.JSONEncoder):
    """Encoder JSON que maneja dataclasses y tipos no serializables."""

    def default(self, o: Any) -> Any:
        if hasattr(o, "__dataclass_fields__"):
            return asdict(o)
        return super().default(o)
