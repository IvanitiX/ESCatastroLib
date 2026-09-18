import requests

class InspireParcelasProvider:
    """Provider para consultas INSPIRE de parcelas catastrales.

    Proporciona métodos para consultar la geometría y atributos
    de parcelas catastrales utilizando el estándar INSPIRE/WFS.

    Attributes:
        URL_BASE: URL base del servicio WFS de parcelas INSPIRE.
    """
    URL_BASE = 'https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx'
    
    def consultar_coordenadas_parcela(self, rc: str, projection: str) -> requests.Response:
        params = {
            'service':'wfs',
            'version':'2',
            'request':'getfeature',
            'STOREDQUERIE_ID':'GetParcel',
            'refcat':rc,
            'srsname':projection
        }

        peticion = requests.get(self.URL_BASE, params=params)

        return peticion