

from dataclasses import dataclass

from shapely.geometry import Point, Polygon


@dataclass
class PuntoDTO:
    sr: str
    dimensiones: int
    coordenadas: list[float]


@dataclass
class GeometriaDTO:
    sr: str
    tipo: str
    puntos: list[PuntoDTO]

    def to_shapely(self) -> Point | Polygon | None:
        coords = [(p.coordenadas[0], p.coordenadas[1]) for p in self.puntos]

        if self.tipo == "Point":
            return Point(coords[0]) if coords else None

        if self.tipo == "Polygon":
            return Polygon(coords) if coords else None

        return None