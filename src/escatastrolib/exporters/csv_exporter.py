import csv
import json
from pathlib import Path
from typing import Any

from ..models.ParcelaCatastral import ParcelaCatastral
from ._base import _geometria_to_wkt


def _parcela_to_row(
    parcela: ParcelaCatastral,
    include_geometry: bool,
    *,
    invert_coordinates: bool = False,
) -> dict:
    """Convierte una parcela a diccionario plano para CSV.

    Aplana la estructura de la parcela a un solo nivel. La geometría
    se serializa como WKT. Las construcciones se serializan como
    cadena JSON.

    Args:
        parcela: Modelo de dominio ParcelaCatastral.
        include_geometry: Si True, incluye columna con geometría WKT.
        invert_coordinates: Si True, invierte coordenadas de (lat,lon) a (lon,lat).

    Returns:
        Diccionario plano con los campos de la parcela.
    """
    row: dict[str, Any] = {
        "referencia_catastral": parcela.referencia_catastral,
        "municipio": parcela.municipio.municipio,
        "provincia": parcela.municipio.provincia,
        "tipo": parcela.tipo,
        "superficie_plana": parcela.superficie_plana,
        "superficie_construida": parcela.superficie_construida,
    }

    if parcela.datos_urbanos:
        row["calle"] = f"{parcela.datos_urbanos.calle.tipo_via} {parcela.datos_urbanos.calle.calle}"
        row["numero"] = parcela.datos_urbanos.numero
        row["antiguedad"] = parcela.datos_urbanos.antiguedad
        row["uso"] = parcela.datos_urbanos.uso
    else:
        row["calle"] = ""
        row["numero"] = ""
        row["antiguedad"] = ""
        row["uso"] = ""

    if parcela.datos_rusticos:
        row["poligono"] = parcela.datos_rusticos.poligono
        row["parcela"] = parcela.datos_rusticos.parcela
        row["nombre_paraje"] = parcela.datos_rusticos.nombre_paraje
    else:
        row["poligono"] = ""
        row["parcela"] = ""
        row["nombre_paraje"] = ""

    if parcela.valor_urbano:
        row["val_catastral"] = parcela.valor_urbano.val_tipo_m2
    elif parcela.valor_rustico:
        row["val_catastral"] = parcela.valor_rustico.nombre_region
    else:
        row["val_catastral"] = ""

    if include_geometry:
        row["geometria_wkt"] = _geometria_to_wkt(
            parcela.geometria, invert_coordinates=invert_coordinates
        )

    return row


def to_csv(
    parcelas: list[ParcelaCatastral],
    path: str | Path | None = None,
    *,
    include_geometry: bool = True,
    invert_coordinates: bool = False,
    delimiter: str = ",",
) -> str | Path:
    """Exporta parcelas a CSV.

    Genera un CSV con columnas planas. La geometría se serializa como
    WKT. Las construcciones se omiten del CSV por ser datos anidados
    de estructura variable.

    Args:
        parcelas: Lista de modelos ParcelaCatastral.
        path: Ruta del archivo de salida. Si es None, devuelve la cadena CSV.
        include_geometry: Si True, incluye columna con geometría WKT.
        invert_coordinates: Si True, invierte coordenadas de (lat,lon) a (lon,lat).
        delimiter: Delimitador del CSV.

    Returns:
        Cadena CSV si path es None, o Path del archivo creado.
    """
    if not parcelas:
        csv_str = ""
        if path is None:
            return csv_str
        Path(path).write_text(csv_str, encoding="utf-8")
        return Path(path)

    rows = [
        _parcela_to_row(p, include_geometry, invert_coordinates=invert_coordinates)
        for p in parcelas
    ]
    fieldnames = list(rows[0].keys())

    from io import StringIO

    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, delimiter=delimiter)
    writer.writeheader()
    writer.writerows(rows)
    csv_str = buf.getvalue()

    if path is None:
        return csv_str

    out = Path(path)
    out.write_text(csv_str, encoding="utf-8")
    return out
