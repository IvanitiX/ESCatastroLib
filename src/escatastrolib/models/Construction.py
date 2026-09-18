from __future__ import annotations

from dataclasses import dataclass, field

from .GeometriaCatastral import Geometria


@dataclass
class Construction:
    """Clase base para construcciones catastrales (INSPIRE BU).

    Attributes:
        id: Identificador único de la construcción.
        geometria: Geometría de la construcción, o None si no está disponible.
        condition: Estado de la construcción (ej. "Functional", "Ruins").
    """

    id: str
    geometria: Geometria | None = None
    condition: str | None = None


@dataclass
class BuildingPart(Construction):
    """Parte constructiva de un edificio (BU.BUILDINGPART).

    Representa una porción de un edificio con información específica de
    plantas y altura subterránea.

    Attributes:
        num_plantas_sup: Número de plantas sobre rasante.
        num_plantas_inf: Número de plantas bajo rasante.
        altura_inf: Altura bajo rasante en metros.
    """

    num_plantas_sup: int | None = None
    num_plantas_inf: int | None = None
    altura_inf: float | None = None


@dataclass
class Building(Construction):
    """Edificio completo (BU.BUILDING).

    Contiene la información principal de un edificio catastral, incluyendo
    su uso, unidades, viviendas y una lista de BuildingPart que lo componen.

    Attributes:
        uso_actual: Uso principal del edificio (ej. "Residencial", "Comercial").
        num_unidades: Número total de unidades del edificio.
        num_viviendas: Número de viviendas.
        num_plantas_sup: Número de plantas sobre rasante.
        area_oficial: Superficie oficial del edificio en m².
        building_parts: Lista de partes constructivas del edificio.
    """

    uso_actual: str | None = None
    num_unidades: int | None = None
    num_viviendas: int | None = None
    num_plantas_sup: int | None = None
    area_oficial: float | None = None
    building_parts: list[BuildingPart] = field(default_factory=list)


@dataclass
class OtherConstruction(Construction):
    """Otra construcción distinta de un edificio (BU.OTHERCONSTRUCTION).

    Representa construcciones como garajes, trasteros, piscinas, etc.

    Attributes:
        naturaleza: Tipo o naturaleza de la construcción (ej. "Garaje", "Piscina").
    """

    naturaleza: str | None = None
