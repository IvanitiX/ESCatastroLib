from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dataclasses import asdict, fields

from ..models.GeometriaCatastral import Geometria
from ..models.ParcelaCatastral import ParcelaCatastral
from ._base import _EnhancedEncoder


def _serialize_parcela(parcela: ParcelaCatastral, include_geometry: bool) -> dict:
    """Serializa una parcela catastral a diccionario.

    Convierte el modelo de dominio a un diccionario con anidamiento
    controlado. La geometría se serializa como dict con coordinates,
    type y crs.

    Args:
        parcela: Modelo de dominio ParcelaCatastral.
        include_geometry: Si True, incluye la geometría serializada.

    Returns:
        Diccionario con los campos de la parcela.
    """
    data = asdict(parcela)

    if not include_geometry:
        data["geometria"] = None

    return data


def to_json(
    parcelas: list[ParcelaCatastral],
    path: str | Path | None = None,
    *,
    include_geometry: bool = True,
    include_constructions: bool = True,
    indent: int = 2,
) -> str | Path:
    """Serializa parcelas a JSON.

    Convierte una lista de parcelas catastrales a una cadena JSON
    o la exporta a un archivo. Las construcciones se incluyen como
    lista anidada dentro de cada parcela.

    Args:
        parcelas: Lista de modelos ParcelaCatastral.
        path: Ruta del archivo de salida. Si es None, devuelve la cadena JSON.
        include_geometry: Si True, incluye la geometría de cada parcela.
        include_constructions: Si True, incluye las construcciones anidadas.
        indent: Nivel de indentación del JSON.

    Returns:
        Cadena JSON si path es None, o Path del archivo creado.
    """
    data = []
    for parcela in parcelas:
        d = _serialize_parcela(parcela, include_geometry)
        if not include_constructions:
            d["construcciones"] = None
        data.append(d)

    json_str = json.dumps(data, cls=_EnhancedEncoder, indent=indent, ensure_ascii=False)

    if path is None:
        return json_str

    out = Path(path)
    out.write_text(json_str, encoding="utf-8")
    return out
