from ..utils.utils import listar_municipios
from typing import Union

class Municipio:
    """
    Clase que representa un municipio.
    Args:
        provincia (str): El nombre de la provincia a la que pertenece el municipio.
        municipio (str, optional): El nombre del municipio. Si no se proporciona, se lanzará una excepción con el municipio.
    Attributes:
        provincia (str): El nombre de la provincia a la que pertenece el municipio.
        municipio (str): El nombre del municipio.
    Raises:
        Exception: Si no se especifica el municipio o si el municipio especificado no está disponible o si no se ha especificado completamente (te dará una lista de coincidencias).
    """

    def __init__(self, provincia: str, municipio: Union[str,None] = None):
        municipios = listar_municipios(provincia=provincia,municipio=municipio)

        if municipio:
            if len(municipios) == 1:
                self.provincia = provincia
                self.municipio = municipios[0]
            elif municipio.upper() in municipios:
                self.provincia = provincia
                self.municipio = municipio.upper()
            else:
                raise Exception(f"Error al asignar municipio. No has especificado el municipio completamente. Estos son los municipios disponibles con esa búsqueda: {','.join(municipios)}")
        else:
            raise Exception(f"Error al asignar municipio. No has especificado el municipio. Estos son los municipios disponibles: {','.join(municipios)}")
