from typing import Any

import requests
import xmltodict

from .dto import GeometriaDTO, PuntoDTO, INSPIREParcelDTO
from ...typing import to_int, to_float

class INSPIREParcelParser:
    """Parser de respuestas INSPIRE CP (Cadastral Parcels) en formato WFS XML.

    Extrae la geometría de una parcela catastral desde el servicio INSPIRE
    de parcelas. Recupera:
    - Geometría ``MultiSurface`` como polígono de vértices.
    - Punto de referencia (centroide) como ``Point``.
    - Valor del área de la parcela.
    """

    def parse(self, response: requests.Response) -> INSPIREParcelDTO:
        """Parsea una respuesta WFS XML de parcelas INSPIRE CP.

        Args:
            response: Objeto requests.Response con contenido XML GML/WFS.

        Returns:
            INSPIREParcelDTO: DTO con geometría, centroide y área de la parcela.

        Raises:
            ValueError: Si el contenido está vacío o la API retorna una excepción.
        """
        content = response.content

        if len(content) == 0:
              raise ValueError("No hay informacion")
        
        json_response = xmltodict.parse(content)

        if json_response.get('ExceptionReport',None) is not None:
              self._raise_exception(json_response)

        return self._to_dto(json_response)

    def _raise_exception(self, data: dict[str, Any]) -> None:
        report = data.get('ExceptionReport',{})
        exception = report.get('Exception',{}) 
        raise ValueError(exception.get('ExceptionText','No se proporcionó reporte'))
    
    def _parse_geometry_list(self, data: dict[str, Any]) -> GeometriaDTO:
        puntos = []

        multisurface = data.get('gml:MultiSurface')
        surface_member = multisurface.get('gml:surfaceMember')
        surface = surface_member.get('gml:Surface')
        patches = surface.get('gml:patches')
        polygon_patch = patches.get('gml:PolygonPatch')
        exterior = polygon_patch.get('gml:exterior')
        linear_ring = exterior.get('gml:LinearRing')
        pos_list = linear_ring.get('gml:posList')
        dimensiones = to_int(pos_list.get('@srsDimension'))
        cadena = pos_list.get('#text').split(' ')
        cuenta = to_int(pos_list.get('@count'))
        sr = surface.get('@srsName').split('/')[-1]

        for i in range(cuenta):
            coords = [float(cadena[i*dimensiones + j]) for j in range(dimensiones)]
            puntos.append(PuntoDTO(
                    sr=sr,
                    dimensiones=dimensiones,
                    coordenadas=coords
            ))

        return GeometriaDTO(
             sr=sr,
             tipo="Polygon",
             puntos=puntos
        )

        
    
    def _parse_reference_point(self, data: dict[str, Any]) -> GeometriaDTO:
          point = data.get('gml:Point')
          sr = point.get('@srsName').split('/')[-1]
          position = point.get('gml:pos').split(' ')
          full_sr = f"EPSG:{sr}"

          return GeometriaDTO(
                sr=full_sr,
                tipo='Point',
                puntos=[PuntoDTO(
                      sr=full_sr,
                      dimensiones=len(position),
                      coordenadas=[float(x) for x in position]
                )]
          )

    def _to_dto(self, data: dict[str, Any]) -> INSPIREParcelDTO:
          features = data.get('FeatureCollection')
          member = features.get('member')
          cp = member.get('cp:CadastralParcel')

          return INSPIREParcelDTO(
                geometria=self._parse_geometry_list(cp.get('cp:geometry')),
                centroide=self._parse_reference_point(cp.get('cp:referencePoint')),
                area=to_float(cp.get('cp:areaValue',{}).get('#text'))
          )
