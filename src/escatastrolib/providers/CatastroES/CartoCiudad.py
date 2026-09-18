import requests

from ...errors.ErrorServidorDGC import comprobar_errores

class CartoCiudadProvider:
    """Provider para consultas al servicio de CartoCiudad.

    Proporciona métodos de geocodificación para convertir direcciones
    en coordenadas geográficas utilizando el servicio de CartoCiudad.

    Attributes:
        URL_BASE: URL base del servicio de geocodificación de CartoCiudad.
    """
    URL_BASE = 'https://www.cartociudad.es/geocoder/api/geocoder'
    
    @comprobar_errores
    def consulta_por_direccion(self, direccion: str, municipio: str) -> requests.Response:
        peticion = requests.get(f'{self.URL_BASE}/findJsonp', 
                                params = {
                                        'q': f'{direccion}, {municipio}'
                                    }
                                )
        
        return peticion