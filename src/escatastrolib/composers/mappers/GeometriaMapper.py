

from ...models.GeometriaCatastral import Geometria
from ...parsers.common.dtos_geometria import GeometriaDTO


class GeometriaMapper:
    """Mapper que convierte GeometriaDTO a Geometria (modelo de dominio).

    Transforma la lista de puntos del DTO en tuplas de coordenadas
    compatibles con el modelo ``Geometria`` y Shapely.
    """

    @staticmethod
    def map(dto: GeometriaDTO) -> Geometria:
        """Convierte un GeometriaDTO a un modelo Geometria.

        Args:
            dto: GeometriaDTO con puntos, sistema de referencia y tipo.

        Returns:
            Geometria: Modelo de dominio con coordenadas como tuplas (x, y).
        """
        coordenadas = [(p.coordenadas[0], p.coordenadas[1]) for p in dto.puntos]
        return Geometria(
            sistema_referencia=dto.sr,
            coordenadas=coordenadas,
            tipo=dto.tipo,
        )
