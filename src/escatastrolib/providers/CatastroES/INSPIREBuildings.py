import requests


class InspireBuildingsProvider:
    """Provider para consultas INSPIRE de edificios y construcciones.

    Proporciona métodos para consultar información de edificios,
    partes de edificios y otras construcciones asociadas a parcelas
    catastrales utilizando el estándar INSPIRE/WFS.

    Attributes:
        URL_BASE: URL base del servicio WFS de edificios INSPIRE.
    """
    URL_BASE = "https://ovc.catastro.meh.es/INSPIRE/wfsBU.aspx"

    def consulta_partes_edificios(self, rc: str, srsname: str = "EPSG:4326") -> requests.Response:
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "STOREDQUERIE_ID": "GetBuildingPartByParcel",
            "REFCAT": rc,
            "srsname": srsname,
        }

        peticion = requests.get(
            self.URL_BASE,
            params=params,
        )

        return peticion

    def consulta_edificios(self, rc: str, srsname: str = "EPSG:4326") -> requests.Response:
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "STOREDQUERIE_ID": "GetBuildingByParcel",
            "REFCAT": rc,
            "srsname": srsname,
        }

        peticion = requests.get(
            self.URL_BASE,
            params=params,
        )

        return peticion

    def consulta_otras_construcciones(self, rc: str, srsname: str = "EPSG:4326") -> requests.Response:
        params = {
            "service": "WFS",
            "version": "2.0.0",
            "request": "GetFeature",
            "STOREDQUERIE_ID": "GetOtherBuildingByParcel",
            "REFCAT": rc,
            "srsname": srsname,
        }

        peticion = requests.get(
            self.URL_BASE,
            params=params,
        )

        return peticion