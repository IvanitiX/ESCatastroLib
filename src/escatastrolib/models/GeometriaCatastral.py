from dataclasses import dataclass
from shapely.geometry import Point, Polygon


@dataclass
class Geometria:
    """Geometría catastral de una parcela o construcción.

    Almacena las coordenadas de una geometría junto con su sistema de
    referencia y tipo. Proporciona conversión a objetos Shapely y
    propiedades calculadas de área y perímetro.

    Attributes:
        sistema_referencia: Código del sistema de referencia (ej. "EPSG:4258").
        coordenadas: Lista de coordenadas. Para Point es una tupla (x, y),
            para Polygon es una lista de tuplas [(x1,y1), (x2,y2), ...].
        tipo: Tipo de geometría: "Point" o "Polygon".
    """

    sistema_referencia: str
    coordenadas: list
    tipo: str

    def to_shapely(self) -> Point | Polygon | None:
        """Convierte la geometría a un objeto Shapely.

        Returns:
            Point o Polygon de Shapely según el tipo, o None si no se puede
            convertir.
        """
        if self.tipo == "Point" and self.coordenadas:
            return Point(self.coordenadas[0])
        if self.tipo == "Polygon" and self.coordenadas:
            return Polygon(self.coordenadas)
        return None

    @property
    def area(self) -> float:
        """Área de la geometría en unidades cuadradas del sistema de referencia."""
        geom = self.to_shapely()
        return geom.area if geom else 0.0

    @property
    def perimetro(self) -> float:
        """Perímetro de la geometría en unidades lineales del sistema de referencia."""
        geom = self.to_shapely()
        return geom.length if geom else 0.0