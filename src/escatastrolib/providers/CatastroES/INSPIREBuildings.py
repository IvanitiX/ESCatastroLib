import requests


class InspireBuildingsProvider:
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