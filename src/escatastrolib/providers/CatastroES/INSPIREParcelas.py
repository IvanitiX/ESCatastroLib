import requests

class InspireParcelasProvider:
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