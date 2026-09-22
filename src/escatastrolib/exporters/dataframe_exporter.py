

from pathlib import Path
from typing import TYPE_CHECKING

from ..models.ParcelaCatastral import ParcelaCatastral
from ._base import _geometria_to_wkt

if TYPE_CHECKING:
    import pandas as pd


def _parcela_to_row(
    parcela: ParcelaCatastral,
    include_geometry: bool,
    *,
    invert_coordinates: bool = False,
) -> dict:
    """Convierte una parcela a diccionario plano para DataFrame.

    Args:
        parcela: Modelo de dominio ParcelaCatastral.
        include_geometry: Si True, incluye columna con geometría WKT.
        invert_coordinates: Si True, invierte coordenadas de (lat,lon) a (lon,lat).

    Returns:
        Diccionario plano con los campos de la parcela.
    """
    row: dict = {
        "referencia_catastral": parcela.referencia_catastral,
        "municipio": parcela.municipio.municipio,
        "provincia": parcela.municipio.provincia,
        "tipo": parcela.tipo,
        "superficie_plana": parcela.superficie_plana,
        "superficie_construida": parcela.superficie_construida,
    }

    if parcela.datos_urbanos:
        row["calle"] = parcela.datos_urbanos.calle.calle
        row["tipo_via"] = parcela.datos_urbanos.calle.tipo_via
        row["numero"] = parcela.datos_urbanos.numero
        row["antiguedad"] = parcela.datos_urbanos.antiguedad
        row["uso"] = parcela.datos_urbanos.uso
    else:
        row["calle"] = None
        row["tipo_via"] = None
        row["numero"] = None
        row["antiguedad"] = None
        row["uso"] = None

    if parcela.datos_rusticos:
        row["poligono"] = parcela.datos_rusticos.poligono
        row["parcela_rustica"] = parcela.datos_rusticos.parcela
        row["nombre_paraje"] = parcela.datos_rusticos.nombre_paraje
    else:
        row["poligono"] = None
        row["parcela_rustica"] = None
        row["nombre_paraje"] = None

    if parcela.valor_urbano:
        row["val_catastral"] = parcela.valor_urbano.val_tipo_m2
    elif parcela.valor_rustico:
        row["val_catastral"] = parcela.valor_rustico.valor_promedio

    if include_geometry:
        row["geometria_wkt"] = _geometria_to_wkt(
            parcela.geometria, invert_coordinates=invert_coordinates
        )

    return row


def to_dataframe(
    parcelas: list[ParcelaCatastral],
    path: str | Path | None = None,
    *,
    format: str = "csv",
    include_geometry: bool = True,
    invert_coordinates: bool = False,
) -> "pd.DataFrame | Path":
    """Convierte parcelas a DataFrame de pandas.

    Requiere la dependencia opcional ``pandas``. Aplana la estructura
    de parcelas a un DataFrame con columnas planas. Si se proporciona
    path, exporta al formato indicado.

    Args:
        parcelas: Lista de modelos ParcelaCatastral.
        path: Ruta del archivo de salida. Si es None, devuelve el DataFrame.
        format: Formato de salida: "csv", "excel" o "parquet".
        include_geometry: Si True, incluye columna con geometría WKT.
        invert_coordinates: Si True, invierte coordenadas de (lat,lon) a (lon,lat).

    Returns:
        DataFrame de pandas si path es None, o Path del archivo creado.

    Raises:
        ImportError: Si pandas no está instalado.
        ValueError: Si el formato no es soportado.
    """
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas es necesario para exportar a DataFrame. "
            "Instálalo con: pip install escatastrolib[export]"
        )

    rows = [
        _parcela_to_row(p, include_geometry, invert_coordinates=invert_coordinates)
        for p in parcelas
    ]
    df = pd.DataFrame(rows)

    if path is None:
        return df

    out = Path(path)
    format_lower = format.lower()

    if format_lower == "csv":
        df.to_csv(out, index=False)
    elif format_lower == "excel":
        df.to_excel(out, index=False)
    elif format_lower == "parquet":
        try:
            df.to_parquet(out, index=False)
        except ImportError:
            raise ImportError(
                "pyarrow o fastparquet es necesario para exportar a Parquet. "
                "Instálalo con: pip install escatastrolib[export]"
            )
    else:
        raise ValueError(
            f"Formato no soportado: {format}. "
            f"Usa 'csv', 'excel' o 'parquet'."
        )

    return out
