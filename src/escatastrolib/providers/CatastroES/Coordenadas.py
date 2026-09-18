import requests

from ...errors.ErrorServidorDGC import comprobar_errores

class CoordenadasAPIProvider:
    """Provider para consultas de coordenadas del Catastro de España.

    Proporciona métodos para convertir entre referencias catastrales (RC)
    y coordenadas geográficas, así como obtener coordenadas de parcelas.

    Attributes:
        URL_BASE: URL base del servicio de coordenadas del Catastro.
    """
    URL_BASE = 'https://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCoordenadas.svc/json'
    

    @comprobar_errores
    def consulta_rc_por_coordenadas(self, lat: float, lon: float, sr: str = 'EPSG:4326') -> requests.Response:
        """
        Convierte coordenadas X e Y a una referencia catastral (RC).
        
        Args:
            lat (float): Latitud.
            lon (float): Longitud.
            sr (str): Sistema de referencia. Por defecto es 'EPSG:4326'.
            
        Returns:
            str: Referencia catastral (RC).
        """
        peticion = requests.get(f'{self.URL_BASE}/Consulta_RCCOOR',
                                params={
                                    'CoorX': lon,
                                    'CoorY': lat,
                                    'SRS': sr
                                }) 
        
        return peticion
    
    @comprobar_errores
    def convertir_rc_a_coordenadas(self, rc: str, sr: str = 'EPSG:4326') -> requests.Response:
        """
        Convierte una referencia catastral (RC) a coordenadas X e Y.
        Args:
            rc (str): Referencia catastral.
            sr (str): Sistema de referencia. Por defecto es 'EPSG:4326'.
        Returns:
            dict: Un diccionario con las coordenadas X e Y.
        """
        peticion = requests.get(f'{self.URL_BASE}/Consulta_CPMRC',
                                params={
                                    'RefCat': rc,
                                    'SRS': sr
                                })
        
        return peticion