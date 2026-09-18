import requests

class MapaValoresRusticosProvider:
    URL_BASE = "https://www1.sedecatastro.gob.es/Cartografia/GeoServerWMS.aspx"
    

    def consulta_valores_rusticos_m2(self, anio: int, bbox_3857: str) -> requests.Response:
        params = {
            "SERVICE": "WMS",
            "VERSION": "1.3.0",
            "REQUEST": "GetFeatureInfo",
            "LAYERS": f"IAMIR{int(str(anio)[-2:])-1}:athiamir{int(str(anio)[-2:])-1}",
            "QUERY_LAYERS": f"IAMIR{int(str(anio)[-2:])-1}:athiamir{int(str(anio)[-2:])-1}",
            "STYLES": "",
            "CRS": "EPSG:3857",
            "SRS": "EPSG:3857",
            "BBOX": bbox_3857,
            "WIDTH": 101,
            "HEIGHT": 101,
            "FORMAT": "image/png",
            "TRANSPARENT": "true",
            "I": 55,
            "J": 55,
            "INFO_FORMAT": "application/json"
        }

        peticion = requests.get(self.URL_BASE, params=params, timeout=15)
        peticion.raise_for_status()

        return peticion