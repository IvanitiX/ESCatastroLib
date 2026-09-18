import json
from pathlib import Path
from typing import Any

from ..models.ParcelaCatastral import ParcelaCatastral
from ._base import _geometria_to_wkt, _make_crs_transformer


def to_geopackage(
    parcelas: list[ParcelaCatastral],
    path: str | Path | None = None,
    *,
    target_crs: str = "EPSG:4326",
) -> Path:
    """Exporta parcelas a un archivo GeoPackage.

    Requiere la dependencia opcional ``fudgeo``. Genera un archivo .gpkg
    con una capa 'parcelas' que incluye todas las construcciones serializadas
    como JSON en la columna 'construcciones'.

    Args:
        parcelas: Lista de modelos ParcelaCatastral.
        path: Ruta del archivo de salida (.gpkg). Debe proporcionarse.
        target_crs: CRS de salida. Default EPSG:4326 (WGS84).

    Returns:
        Path del archivo creado.

    Raises:
        ImportError: Si fudgeo no está instalado.
        ValueError: Si path es None.
    """
    if path is None:
        raise ValueError(
            "GeoPackage requiere una ruta de archivo. "
            "Proporciona un path para exportar a .gpkg."
        )

    try:
        from fudgeo import FeatureClass, Field, GeoPackage, SpatialReferenceSystem
        from fudgeo.enumeration import FieldType, ShapeType
    except ImportError:
        raise ImportError(
            "fudgeo es necesario para exportar a GeoPackage. "
            "Instálalo con: pip install escatastrolib[gis]"
        )

    out = Path(path)

    srs_id = int(target_crs.split(":")[-1])
    srs = SpatialReferenceSystem(
        name=target_crs,
        organization="EPSG",
        org_coord_sys_id=srs_id,
        definition=f"EPSG:{srs_id}",
    )

    gpkg = GeoPackage.create(str(out), flavor="EPSG")

    fields = (
        Field("referencia_catastral", FieldType.text, size=20),
        Field("municipio", FieldType.text, size=100),
        Field("provincia", FieldType.text, size=100),
        Field("tipo", FieldType.text, size=10),
        Field("superficie_plana", FieldType.double),
        Field("superficie_construida", FieldType.double),
        Field("construcciones", FieldType.text),
    )

    fc = gpkg.create_feature_class(
        "parcelas",
        srs=srs,
        fields=fields,
        shape_type=ShapeType.polygon,
        spatial_index=True,
    )

    transformer = None
    if target_crs != "EPSG:4326":
        transformer = _make_crs_transformer("EPSG:4326", target_crs)

    sql = """INSERT INTO parcelas
             (SHAPE, referencia_catastral, municipio, provincia, tipo,
              superficie_plana, superficie_construida, construcciones)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

    rows = []
    for parcela in parcelas:
        if parcela.geometria is None:
            continue

        from shapely.geometry import mapping

        shapely_geom = parcela.geometria.to_shapely()
        if shapely_geom is None:
            continue

        if transformer is not None:
            from shapely.ops import transform as shapely_transform

            shapely_geom = shapely_transform(transformer.transform, shapely_geom)

        from fudgeo.geometry import Polygon

        rings = [list(shapely_geom.exterior.coords)]
        gpkg_geom = Polygon(rings, srs_id=srs_id)

        construcciones_json = ""
        if parcela.construcciones:
            from dataclasses import asdict

            construcciones_json = json.dumps(
                [asdict(c) for c in parcela.construcciones],
                ensure_ascii=False,
            )

        rows.append((
            gpkg_geom,
            parcela.referencia_catastral,
            parcela.municipio.municipio,
            parcela.municipio.provincia,
            parcela.tipo,
            parcela.superficie_plana,
            parcela.superficie_construida,
            construcciones_json,
        ))

    with gpkg.connection as conn:
        conn.executemany(sql, rows)

    return out


def to_shapefile(
    parcelas: list[ParcelaCatastral],
    path: str | Path | None = None,
    *,
    target_crs: str = "EPSG:4326",
) -> Path:
    """Exporta parcelas a un archivo Shapefile.

    Requiere la dependencia opcional ``pyshp``. Genera un archivo .shp
    con las parcelas. Las construcciones se omiten por las limitaciones
    del formato (nombres de campo de 10 caracteres, un tipo de geometría
    por archivo).

    Args:
        parcelas: Lista de modelos ParcelaCatastral.
        path: Ruta del directorio de salida (Shapefile genera varios archivos).
            Debe proporcionarse.
        target_crs: CRS de salida. Default EPSG:4326 (WGS84).

    Returns:
        Path del archivo creado.

    Raises:
        ImportError: Si pyshp no está instalado.
        ValueError: Si path es None.
    """
    if path is None:
        raise ValueError(
            "Shapefile requiere una ruta de archivo. "
            "Proporciona un path para exportar a .shp."
        )

    try:
        import shapefile
    except ImportError:
        raise ImportError(
            "pyshp es necesario para exportar a Shapefile. "
            "Instálalo con: pip install escatastrolib[gis]"
        )

    out = Path(path)

    transformer = None
    if target_crs != "EPSG:4326":
        transformer = _make_crs_transformer("EPSG:4326", target_crs)

    w = shapefile.Writer(str(out), shapeType=shapefile.POLYGON)
    w.autoBalance = 1

    w.field("RC", "C", size=20)
    w.field("MUNICIPIO", "C", size=100)
    w.field("PROVINCIA", "C", size=100)
    w.field("TIPO", "C", size=10)
    w.field("SUP_PLANA", "F", decimal=2)
    w.field("SUP_CONST", "F", decimal=2)

    for parcela in parcelas:
        if parcela.geometria is None:
            w.null()
            w.record(
                parcela.referencia_catastral,
                parcela.municipio.municipio,
                parcela.municipio.provincia,
                parcela.tipo,
                parcela.superficie_plana,
                parcela.superficie_construida,
            )
            continue

        shapely_geom = parcela.geometria.to_shapely()
        if shapely_geom is None:
            w.null()
            w.record(
                parcela.referencia_catastral,
                parcela.municipio.municipio,
                parcela.municipio.provincia,
                parcela.tipo,
                parcela.superficie_plana,
                parcela.superficie_construida,
            )
            continue

        if transformer is not None:
            from shapely.ops import transform as shapely_transform

            shapely_geom = shapely_transform(transformer.transform, shapely_geom)

        coords = list(shapely_geom.exterior.coords)
        w.poly([coords])

        w.record(
            parcela.referencia_catastral,
            parcela.municipio.municipio,
            parcela.municipio.provincia,
            parcela.tipo,
            parcela.superficie_plana,
            parcela.superficie_construida,
        )

    w.close()

    _write_prj(out, target_crs)

    return out


def _write_prj(shp_path: Path, crs: str) -> None:
    """Escribe el archivo .prj con la definición WKT del CRS.

    Args:
        shp_path: Ruta base del shapefile (sin extensión).
        crs: Código EPSG del CRS.
    """
    WKT_PROJECTIONS = {
        "EPSG:4326": 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
        "EPSG:25830": 'PROJCS["ETRS89_UTM_Zone_30N",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Meter",1.0]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0]]',
        "EPSG:25831": 'PROJCS["ETRS89_UTM_Zone_31N",GEOGCS["GCS_ETRS_1989",DATUM["D_ETRS_1989",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Meter",1.0]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",9.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0]]',
    }

    wkt = WKT_PROJECTIONS.get(crs)
    if wkt:
        prj_path = shp_path.with_suffix(".prj")
        prj_path.write_text(wkt, encoding="utf-8")
