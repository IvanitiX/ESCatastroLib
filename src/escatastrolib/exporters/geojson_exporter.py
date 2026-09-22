import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ..models.GeometriaCatastral import Geometria
from ..models.ParcelaCatastral import ParcelaCatastral
from ._base import (
    _EnhancedEncoder,
    _geometria_to_geojson_dict,
    _make_crs_transformer,
)


def _parcela_to_feature(
    parcela: ParcelaCatastral,
    transformer: Any | None,
    coordinate_precision: int,
    include_constructions: bool,
    *,
    invert_coordinates: bool = False,
) -> dict:
    """Convierte una parcela a un Feature GeoJSON.

    La geometría se convierte a GeoJSON geometry con reproyección
    opcional. Los atributos se incluyen como properties. Las
    construcciones se anidan como lista de dicts en properties.

    Args:
        parcela: Modelo de dominio ParcelaCatastral.
        transformer: Transformer de pyproj para reproyección, o None.
        coordinate_precision: Decimales para las coordenadas.
        include_constructions: Si True, incluye construcciones en properties.
        invert_coordinates: Si True, invierte coordenadas de (lat,lon) a (lon,lat).

    Returns:
        Diccionario GeoJSON Feature.

    Raises:
        ValueError: Si la parcela no tiene geometría.
    """
    geometry = _geometria_to_geojson_dict(
        parcela.geometria,
        transformer=transformer,
        precision=coordinate_precision,
        invert_coordinates=invert_coordinates,
    )
    if geometry is None:
        raise ValueError(
            f"La parcela {parcela.referencia_catastral} no tiene geometría."
        )

    properties: dict[str, Any] = {
        "referencia_catastral": parcela.referencia_catastral,
        "municipio": parcela.municipio.municipio,
        "provincia": parcela.municipio.provincia,
        "tipo": parcela.tipo,
        "superficie_plana": parcela.superficie_plana,
        "superficie_construida": parcela.superficie_construida,
    }

    if parcela.datos_urbanos:
        properties["calle"] = parcela.datos_urbanos.calle.calle
        properties["tipo_via"] = parcela.datos_urbanos.calle.tipo_via
        properties["numero"] = parcela.datos_urbanos.numero
        properties["antiguedad"] = parcela.datos_urbanos.antiguedad
        properties["uso"] = parcela.datos_urbanos.uso

    if parcela.datos_rusticos:
        properties["poligono"] = parcela.datos_rusticos.poligono
        properties["parcela"] = parcela.datos_rusticos.parcela
        properties["nombre_paraje"] = parcela.datos_rusticos.nombre_paraje

    if parcela.valor_urbano:
        properties["valor_urbano"] = asdict(parcela.valor_urbano)

    if parcela.valor_rustico:
        properties["valor_rustico"] = asdict(parcela.valor_rustico)

    if parcela.regiones:
        properties["regiones"] = [asdict(r) for r in parcela.regiones]

    if include_constructions and parcela.construcciones:
        properties["construcciones"] = [
            asdict(c) for c in parcela.construcciones
        ]

    return {
        "type": "Feature",
        "geometry": geometry,
        "properties": properties,
    }


def to_geojson(
    parcelas: list[ParcelaCatastral],
    path: str | Path | None = None,
    *,
    target_crs: str = "EPSG:4326",
    include_constructions: bool = True,
    coordinate_precision: int = 6,
    invert_coordinates: bool = False,
) -> dict | Path:
    """Convierte parcelas a GeoJSON FeatureCollection.

    Cada parcela se convierte en un Feature con geometría Polygon o Point.
    La geometría se reproyecta al CRS indicado (requerimiento RFC 7946
    para GeoJSON, que exige WGS84). Las construcciones se incluyen
    como lista anidada en las propiedades.

    Args:
        parcelas: Lista de modelos ParcelaCatastral.
        path: Ruta del archivo de salida (.geojson). Si es None, devuelve
            el diccionario GeoJSON.
        target_crs: CRS de salida. Default EPSG:4326 (WGS84).
        include_constructions: Si True, incluye construcciones en properties.
        coordinate_precision: Decimales para las coordenadas.
        invert_coordinates: Si True, invierte coordenadas de (lat,lon) a (lon,lat).

    Returns:
        Diccionario GeoJSON si path es None, o Path del archivo creado.

    Raises:
        ValueError: Si alguna parcela no tiene geometría.
    """
    transformer = None
    if target_crs != "EPSG:4326":
        transformer = _make_crs_transformer("EPSG:4326", target_crs)

    features = []
    for parcela in parcelas:
        feature = _parcela_to_feature(
            parcela,
            transformer=transformer,
            coordinate_precision=coordinate_precision,
            include_constructions=include_constructions,
            invert_coordinates=invert_coordinates,
        )
        features.append(feature)

    geojson: dict[str, Any] = {
        "type": "FeatureCollection",
        "features": features,
    }

    if path is None:
        return geojson

    out = Path(path)
    out.write_text(
        json.dumps(geojson, cls=_EnhancedEncoder, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return out
