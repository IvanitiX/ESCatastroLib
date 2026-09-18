import requests

from ...errors.ErrorServidorDGC import comprobar_errores

class CroquisAPIProvider:
    """Provider para obtención de croquis de parcelas catastrales.

    Proporciona métodos para obtener la URL del croquis gráfico
    de una parcela catastral desde la sede electrónica del Catastro.

    Attributes:
        URL_BASE: URL base del servicio de croquis del Catastro.
    """
    URL_BASE = f'https://www1.sedecatastro.gob.es/CYCBienInmueble/SECImprimirCroquisYDatos.aspx'

    def consulta_url_croquis(self, rc: str) -> str:
        return requests.get(self.URL_BASE, params={'refcat': rc}).url
