from .Municipio import Municipio
from ..utils.statics import URL_BASE_CALLEJERO
from ..utils.utils import comprobar_errores, comprobar_long_contenido

import requests
import json

from typing import Union

class Calle:
    """
    Clase que representa una calle.
    Args:
        municipio (Municipio): Objeto que representa el municipio al que pertenece la calle.
        nombre_calle (str, optional): Nombre de la calle. Default es None.
        tipo_via (str, optional): Tipo de vía de la calle. Default es None.
    Raises:
        Exception: Se produce cuando ocurre un error al asignar la calle.
        Exception: Se produce cuando no se especifica el nombre de la calle.
        Exception: Se produce cuando no se encuentran calles disponibles.
    Attributes:
        calle (str): Nombre de la calle asignada.
        tipo_via (str): Tipo de vía de la calle asignada.
        municipio (Municipio): Objeto que representa el municipio al que pertenece la calle.
    """

    def __init__(self, municipio: Municipio, nombre_calle: Union[str,None] = None, tipo_via: Union[str,None] = None):
        uri = f'{URL_BASE_CALLEJERO}/ObtenerCallejero'

        request = requests.get(uri, params={
            'Provincia': municipio.provincia,
            'Municipio': municipio.municipio,
            'NomVia': nombre_calle,
            'TipoVia': tipo_via
        })

        if request.status_code == 200 and comprobar_long_contenido(request.content):
            calle_dict = json.loads(request.text)

            if comprobar_errores(calle_dict) and nombre_calle:
                if len(calle_dict.get('consulta_callejeroResult').get('callejero').get('calle')) == 1:
                    self.calle = calle_dict.get('consulta_callejeroResult').get('callejero').get('calle')[0].get('dir').get('nv')
                    self.tipo_via = calle_dict.get('consulta_callejeroResult').get('callejero').get('calle')[0].get('dir').get('tv')
                    self.municipio = municipio
                else:
                    raise Exception(f"""Error al asignar calle. No has especificado la calle completamente, o ese nombre está en varios lados (indica el tipo de vía que aparezca al principio de la vía como PZ o CL). Estas son las calles disponibles con esa búsqueda: {','.join(f"{cl.get('dir').get('tv')} {cl.get('dir').get('nv')}" for cl in calle_dict.get('consulta_callejeroResult').get('callejero').get('calle'))}""")
            else:
                raise Exception(f"""Error al asignar calle. No has especificado la calle. Estas son las calles disponibles: {','.join(f"{cl.get('dir').get('tv')} {cl.get('dir').get('nv')}" for cl in calle_dict.get('consulta_callejeroResult').get('callejero').get('calle'))}""")
            
        else:
            raise Exception(f'Error al listar calles: Puede que no exista ese municipio.')
