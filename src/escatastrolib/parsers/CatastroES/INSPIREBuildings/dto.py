from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ...common.dtos_geometria import GeometriaDTO


@dataclass(slots=True)
class ConstructionBaseDTO:
    """
    Campos comunes de las entidades de construcciones INSPIRE BU.
    """

    id: str

    local_id: str | None = None
    namespace: str | None = None

    begin_lifespan_version: datetime | None = None
    condition_of_construction: str | None = None

    addresses_href: str | None = None
    cadastral_parcels_href: str | None = None

    geometry: GeometriaDTO | None = None


@dataclass(slots=True)
class BuildingPartDTO(ConstructionBaseDTO):
    """
    Parte constructiva de un edificio.

    Procede de la entidad BU.BUILDINGPART.
    """

    horizontal_geometry_estimated_accuracy_m: float | None = None
    horizontal_geometry_reference: str | None = None
    reference_geometry: bool | None = None

    number_of_floors_above_ground: int | None = None
    number_of_floors_below_ground: int | None = None
    height_below_ground_m: float | None = None


@dataclass(slots=True)
class BuildingDTO(ConstructionBaseDTO):
    """
    Edificio.

    Procede de la entidad BU.BUILDING.
    """

    end_lifespan_version: datetime | None = None

    date_of_construction_beginning: datetime | None = None
    date_of_construction_end: datetime | None = None

    external_reference_url: str | None = None
    external_reference: str | None = None

    current_use: str | None = None

    number_of_building_units: int | None = None
    number_of_dwellings: int | None = None
    number_of_floors_above_ground: int | None = None

    document_link: str | None = None
    document_format: str | None = None
    document_source_status: str | None = None

    official_area_reference: str | None = None
    official_area_value: float | None = None
    official_area_uom: str | None = None


@dataclass(slots=True)
class OtherConstructionDTO(ConstructionBaseDTO):
    """
    Otra construcción distinta de un edificio.

    Procede de la entidad BU.OTHERCONSTRUCTION.
    """

    construction_nature: str | None = None