import requests

from ...typing import to_str

from .dto import CentroideDTO, RefCatDTO

class CoordenadasParser:
    """Parser base para respuestas de coordenadas del Catastro.

    Proporciona métodos comunes para parsear respuestas JSON del servicio
    de coordenadas del Catastro y convertirlas en DTOs.
    """
    def parse(self, response: requests.Response) -> list[CentroideDTO | RefCatDTO]:
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError as error:
            raise ValueError(
                "La respuesta no contiene un JSON válido"
            ) from error

        if not data:
            return []

        return self._to_dtos(data)

class RCaCoordenadasParser(CoordenadasParser):
    """Parser para convertir referencias catastrales a coordenadas.

    Parsea las respuestas del servicio Consulta_CPMRC del Catastro
    y extrae las coordenadas geográficas de una referencia catastral.
    """
    def parse(self, response: requests.Response) -> list[CentroideDTO]:
        return super().parse(response)
    
    def _to_dtos(self, data: dict[str, object]) -> list[CentroideDTO]:
        lista_dtos = []

        resultado = data.get('Consulta_CPMRCResult',{})
        coordenadas = resultado.get('coordenadas',{})
        coords = coordenadas.get('coord',{})

        for item in coords:
            lista_dtos.append(CentroideDTO(
                x=item.get('geo',{}).get('xcen'),
                y=item.get('geo',{}).get('ycen'),
                sr=item.get('geo',{}).get('srs')
            ))

        return lista_dtos

class CoordenadasaRCParser(CoordenadasParser):
    """Parser para convertir coordenadas a referencias catastrales.

    Parsea las respuestas del servicio Consulta_RCCOOR del Catastro
    y extrae las referencias catastrales correspondientes a unas coordenadas.
    """
    def parse(self, response: requests.Response) -> list[RefCatDTO]:
        return super().parse(response)
    
    def _to_dtos(self, data: dict[str, object]) -> list[RefCatDTO]:
        lista_dtos = []

        resultado = data.get('Consulta_RCCOORResult',{})
        coordenadas = resultado.get('coordenadas',{})
        coords = coordenadas.get('coord',{})

        for item in coords:
            pc1 = item.get('pc').get('pc1')
            pc2 = item.get('pc').get('pc2')
            lista_dtos.append(RefCatDTO(
                rc=to_str(f"{pc1}{pc2}")
            ))

        return lista_dtos
