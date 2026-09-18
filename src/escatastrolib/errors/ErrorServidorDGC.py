from typing import Any, Callable

import requests
from functools import wraps


def comprobar_errores(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> requests.Response:
        """
        Comprueba si la respuesta contiene errores.

        Args:
            respuesta (dict): El diccionario de respuesta.

        Raises:
            ErrorServidorSedeCatastro: Si se encuentra un error en la respuesta.

        Returns:
            Response: La respuesta si no hay errores.
        """
        respuesta = func(*args, **kwargs)

        if respuesta.status_code != 200:
            raise ErrorServidorSedeCatastro(mensaje="Status no es 200.")

        if len(respuesta.content) == 0:
            raise ErrorServidorSedeCatastro(mensaje="Resultado vacio")

        try:
            contenido_respuesta = respuesta.json()
        except ValueError:
            return respuesta

        if not isinstance(contenido_respuesta, dict):
            return respuesta

        if len(contenido_respuesta) > 0:
            primer_valor = list(contenido_respuesta.values())[0]
            if isinstance(primer_valor, dict) and 'lerr' in primer_valor:
                lerr = primer_valor['lerr']
                if isinstance(lerr, dict) and 'err' in lerr:
                    raise ErrorServidorSedeCatastro(mensaje=lerr['err'][0]['des'])
                elif isinstance(lerr, list) and len(lerr) > 0:
                    raise ErrorServidorSedeCatastro(mensaje=lerr[0]['des'])

        return respuesta

    return wrapper


class ErrorServidorSedeCatastro(Exception):
    """
    Clase de excepción personalizada para errores relacionados con el servidor del Catastro.
    Atributos:
    - mensaje (str): Mensaje de error específico del servidor del Catastro.
    """

    def __init__(self, mensaje: str = '') -> None:
        self.message = f'Error del Catastro. {mensaje}'
        super().__init__(self.message)