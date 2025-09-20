import geopandas as gpd
from shapely.geometry import Point, Polygon, GeometryCollection

from typing import Union
from ..utils.utils import lon_lat_from_coords_dict

def to_geodataframe(parcelas: list) -> gpd.GeoDataFrame:
    """
    Convierte la lista de parcelas en un GeoDataFrame de GeoPandas.

    Args:
        projection (str): El sistema de referencia espacial (SRS) para el GeoDataFrame. Default es 'EPSG:4326'.

    Returns:
        gpd.GeoDataFrame: Un GeoDataFrame que contiene las parcelas de la MetaParcela.
    """
    return gpd.GeoDataFrame({
                    "rc": pc.rc,
                    "tipo": pc.tipo,
                    "superficie": pc.superficie,
                    "provincia": pc.provincia, 
                    "municipio": pc.municipio, 
                    "regiones": ','.join([f"{reg.get('descripcion')} ({reg.get('superficie')} m^2)" for reg in pc.regiones]) , 
                    "geometry": Polygon([lon_lat_from_coords_dict(coord) for coord in pc.geometria]),
                    "calle": pc.calle if pc.tipo == "Urbano" else '',
                    "numero": pc.numero if pc.tipo == "Urbano" else '',
                    "antiguedad": pc.antiguedad if pc.tipo == "Urbano" else '',
                    "uso": pc.uso if pc.tipo == "Urbano" else '',
                    "nombre_paraje": pc.nombre_paraje if pc.tipo == "Rústico" else '',
                    "poligono": pc.poligono if pc.tipo == "Rústico" else '',
                    "parcela": pc.parcela if pc.tipo == "Rústico" else ''
                    } for pc in parcelas)

def to_json(parcelas: list, filename: Union[str,None] = None) -> str:
    json_data = to_geodataframe(parcelas).to_json()

    if filename:
        with open(filename, 'w') as writer:
            writer.write(json_data)
            
    return json_data

def to_csv(parcelas: list , filename: Union[str,None] = None) -> str:
    if filename:
        to_geodataframe(parcelas).to_csv(filename, index=False)
    return to_geodataframe(parcelas).to_csv(index=False)

def to_shapefile(parcelas: list , filename: str):
    """
    Guarda la MetaParcela como un archivo Shapefile.

    Args:
        filename (str): El nombre del archivo Shapefile a guardar.
    """
    to_geodataframe(parcelas).to_file(filename, driver='ESRI Shapefile')

def to_parquet(parcelas: list,  filename: str):
    """
    Guarda la MetaParcela como un archivo Parquet.

    Args:
        filename (str): El nombre del archivo Parquet a guardar.
    """

    to_geodataframe(parcelas).to_parquet(filename)
