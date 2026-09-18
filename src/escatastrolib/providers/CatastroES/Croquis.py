import requests

from ...errors.ErrorServidorDGC import comprobar_errores

class CroquisAPIProvider:
    URL_BASE = f'https://www1.sedecatastro.gob.es/CYCBienInmueble/SECImprimirCroquisYDatos.aspx'

    def consulta_url_croquis(self, rc: str) -> str:
        return requests.get(self.URL_BASE, params={'refcat': rc}).url
