import requests
import json

from typing import Union

from .statics import URL_BASE_CALLEJERO, MAPEOS_PROVINCIAS, TIPOS_VIA, SISTEMAS_REFERENCIA, URL_BASE_COORDENADAS, URL_BASE_CARTOCIUDAD_GEOCODER
from .exceptions import lanzar_excepcion

def comprobar_long_contenido(contenido:str):
    """
        Comprueba si el mensaje se puede cargar, es decir, si no esta vacio
        
        Args:
        - contenido: El contenido de la peticion
        Raises:
        - lanzar_excepcion: Si el mensaje esta vacio o no se puede formar el JSON.
    """
    
    try:
        if len(contenido)>0:
            json.loads(contenido)
            return True
        else:
            raise Exception()
    except:
        raise lanzar_excepcion(mensaje_error="Error al cargar JSON")

def comprobar_errores(respuesta: dict):
    """
    Comprueba si la respuesta contiene errores.

    Args:
        respuesta (dict): El diccionario de respuesta.

    Raises:
        lanzar_excepcion: Si se encuentra un error en la respuesta.

    Returns:
        bool: True si no se encuentran errores, False en caso contrario.
    """
    # Check if the response contains the expected structure
    if len(list(respuesta.values())) > 0:
        if list(respuesta.values())[0] is not None and 'lerr' in list(respuesta.values())[0].keys():
            if 'err' in list(respuesta.values())[0]['lerr']:
                raise lanzar_excepcion(mensaje_error=list(respuesta.values())[0]['lerr']['err'][0]['des'])
            else:
                raise lanzar_excepcion(mensaje_error=list(respuesta.values())[0]['lerr'][0]['des'])
        return True

def listar_provincias():
    """
    Obtiene una lista de provincias.
    Returns:
        list: Una lista de nombres de provincias.
    Raises:
        None
    """
    
    response = requests.get(f'{URL_BASE_CALLEJERO}/ObtenerProvincias')
    return [provincia.get('np') for provincia in response.json().get('consulta_provincieroResult').get('provinciero').get('prov')] if comprobar_errores(response.json()) else []

def listar_municipios(provincia: str, municipio: Union[str,None] = None):

    """
    Obtiene una lista de municipios de España.
    Args:
        provincia (str): El nombre de la provincia. Preferentemente en mayúsculas o capitalizado.
        municipio (str, optional): El nombre del municipio. Por defecto es None.
    Returns:
        List[str]: Una lista de nombres de municipios.
    Raises:
        Exception: Si la provincia no existe. Muestra un mensaje con las provincias disponibles.
    """

    if provincia and provincia.capitalize() not in MAPEOS_PROVINCIAS and provincia.upper() not in listar_provincias():
            raise Exception(f'La provincia {provincia} no existe. Las provincias de España son: {listar_provincias()}')
    
    response = requests.get(f'{URL_BASE_CALLEJERO}/ObtenerMunicipios', 
                                params={
                                    'provincia' : MAPEOS_PROVINCIAS.get(provincia.capitalize()) 
                                                    if MAPEOS_PROVINCIAS.get(provincia.capitalize(),None) != None 
                                                    else provincia ,
                                    'municipio': municipio
                                })
    if response.status_code == 200 and comprobar_long_contenido(response.content) and comprobar_errores(response.json()):
        mun_dict_raw = json.loads(response.content)
        return [mun.get('nm') for mun in mun_dict_raw.get('consulta_municipieroResult').get('municipiero').get('muni')]
    else:
         return []
    

def listar_tipos_via():
    """
    Retorna una lista de los tipos de vía disponibles.
    Returns:
        list: Una lista de los tipos de vía disponibles.
    """

    return TIPOS_VIA

def listar_calles(provincia: str, municipio: str):
    """
    Devuelve una lista de calles para una provincia y municipio dados.
    Args:
        provincia (str): El nombre de la provincia.
        municipio (str): El nombre del municipio.
    Returns:
        list: Una lista de calles en formato "tipo de vía nombre de vía".
    """

    provincia_final = MAPEOS_PROVINCIAS.get(provincia.capitalize()) if provincia.capitalize() in MAPEOS_PROVINCIAS.keys() else provincia
    if provincia_final.upper() in listar_provincias() and municipio.upper() in listar_municipios(provincia=provincia_final):
        response = requests.get(f'{URL_BASE_CALLEJERO}/ObtenerCallejero',
                                params={
                                    'Provincia': provincia_final,
                                    'Municipio': municipio
                                })
        if response.status_code == 200 and comprobar_long_contenido(response.content) and comprobar_errores(response.json()):
            calles_dict_raw = json.loads(response.content)
            return [f"{calle.get('dir').get('tv')} {calle.get('dir').get('nv')}" for calle in calles_dict_raw.get('consulta_callejeroResult').get('callejero').get('calle')]
        else:
            return []
    else: return []

def listar_sistemas_referencia():
    """
    Devuelve una lista de sistemas de referencia disponibles.
    Returns:
        list: Una lista de sistemas de referencia disponibles.
    """
    return [key for key in SISTEMAS_REFERENCIA.keys()]

def convertir_coordenadas_a_rc(lat: float, lon: float, sr: str = 'EPSG:4326'):
    """
    Convierte coordenadas X e Y a una referencia catastral (RC).
    
    Args:
        lat (float): Latitud.
        lon (float): Longitud.
        sr (str): Sistema de referencia. Por defecto es 'EPSG:4326'.
        
    Returns:
        str: Referencia catastral (RC).
    """
    response = requests.get(f'{URL_BASE_COORDENADAS}/Consulta_RCCOOR',
                            params={
                                'CoorX': lon,
                                'CoorY': lat,
                                'SRS': sr
                            })
    if response.status_code == 200 and comprobar_long_contenido(response.content) and comprobar_errores(response.json()):
        return ''.join([part for part in response.json().get('Consulta_RCCOORResult').get('coordenadas').get('coord')[0].get('pc').values()])
    else:
        return None
    
def convertir_rc_a_coordenadas(rc: str, sr: str = 'EPSG:4326'):
    """
    Convierte una referencia catastral (RC) a coordenadas X e Y.
    Args:
        rc (str): Referencia catastral.
        sr (str): Sistema de referencia. Por defecto es 'EPSG:4326'.
    Returns:
        dict: Un diccionario con las coordenadas X e Y.
    """
    if len(rc) > 14:
        rc_corregido = rc[0:14]
    else: rc_corregido = rc

    response = requests.get(f'{URL_BASE_COORDENADAS}/Consulta_CPMRC',
                            params={
                                'RefCat': rc_corregido,
                                'SRS': sr
                            })
    if response.status_code == 200 and comprobar_long_contenido(response.content) and comprobar_errores(response.json()):
        coordenadas = response.json().get('Consulta_CPMRCResult').get('coordenadas').get('coord')[0].get('geo')
        return {
            'x': coordenadas.get('xcen'),
            'y': coordenadas.get('ycen')
        }
    else:
        return None
    
def geocodificar_direccion(direccion: str, municipio: str = None):
    """
    Geocodifica una dirección utilizando el servicio de CartoCiudad.
    
    Args:
        direccion (str): La dirección a geocodificar.
        provincia (str, optional): La provincia de la dirección. Por defecto es None.
        municipio (str, optional): El municipio de la dirección. Por defecto es None.
        
    Returns:
        dict: Un diccionario con las coordenadas X e Y y otros datos relevantes.
    """
    
    response = requests.get(f'{URL_BASE_CARTOCIUDAD_GEOCODER}/findJsonp', 
                            params = {
                                'q': f'{direccion}, {municipio}'
                            })
    
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8').replace('callback(', '').replace(')', ''))
        print(data)
        if type(data) == dict:
           return {
                'x': data.get('lng'),
                'y': data.get('lat'),
                'rc': data.get('refCatastral')
            }
        elif type(data) == list and len(data) > 0:
            pc = data[0]
            return {
                'x': pc.get('lng'),
                'y': pc.get('lat'),
                'rc': pc.get('refCatastral')
            }
        else:
            return None
    else:
        return None
            
def lon_lat_from_coords_dict(coords):
    return float(coords["x"]), float(coords["y"])

