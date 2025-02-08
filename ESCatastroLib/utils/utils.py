import requests
import json

from .statics import URL_BASE_CALLEJERO, MAPEOS_PROVINCIAS, TIPOS_VIA
from .exceptions import lanzar_excepcion

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

def listar_municipios(provincia: str, municipio: str|None = None):

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
    if response.status_code == 200 and comprobar_errores(response.json()):
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
        if response.status_code == 200 and comprobar_errores(response.json()):
            calles_dict_raw = json.loads(response.content)
            return [f"{calle.get('dir').get('tv')} {calle.get('dir').get('nv')}" for calle in calles_dict_raw.get('consulta_callejeroResult').get('callejero').get('calle')]
        else:
            return []
    else: return []
