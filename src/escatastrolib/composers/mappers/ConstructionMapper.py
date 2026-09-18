from __future__ import annotations

from ...models.Construction import Building, BuildingPart, Construction, OtherConstruction
from ...parsers.CatastroES.INSPIREBuildings.dto import ConstructionBaseDTO
from .GeometriaMapper import GeometriaMapper


class ConstructionMapper:
    """Mapper que dispatcha DTOs de construcción a sus modelos de dominio.

    Detecta el tipo de DTO (BuildingPart, Building, OtherConstruction)
    inspeccionando sus atributos y crea la instancia correspondiente del
    modelo de dominio.
    """

    @staticmethod
    def map(dto: ConstructionBaseDTO) -> Construction:
        """Convierte un DTO de construcción INSPIRE a su modelo de dominio.

        Detecta el tipo inspeccionando atributos:
        - ``height_below_ground_m`` o ``number_of_floors_below_ground`` → BuildingPart
        - ``current_use`` o ``number_of_building_units`` → Building
        - ``construction_nature`` → OtherConstruction

        Args:
            dto: DTO de construcción INSPIRE (ConstructionBaseDTO).

        Returns:
            Construction: Modelo de dominio correspondiente (BuildingPart,
                Building u OtherConstruction).

        Raises:
            ValueError: Si el tipo de construcción no es reconocido.
        """
        geometria = GeometriaMapper.map(dto.geometry) if dto.geometry else None
        base_fields = {
            "id": dto.id,
            "geometria": geometria,
            "condition": dto.condition_of_construction,
        }

        if hasattr(dto, "height_below_ground_m") or hasattr(dto, "number_of_floors_below_ground"):
            return BuildingPart(
                **base_fields,
                num_plantas_sup=dto.number_of_floors_above_ground if hasattr(dto, "number_of_floors_above_ground") else None,
                num_plantas_inf=dto.number_of_floors_below_ground if hasattr(dto, "number_of_floors_below_ground") else None,
                altura_inf=dto.height_below_ground_m if hasattr(dto, "height_below_ground_m") else None,
            )

        if hasattr(dto, "current_use") or hasattr(dto, "number_of_building_units"):
            return Building(
                **base_fields,
                uso_actual=dto.current_use if hasattr(dto, "current_use") else None,
                num_unidades=dto.number_of_building_units if hasattr(dto, "number_of_building_units") else None,
                num_viviendas=dto.number_of_dwellings if hasattr(dto, "number_of_dwellings") else None,
                num_plantas_sup=dto.number_of_floors_above_ground if hasattr(dto, "number_of_floors_above_ground") else None,
                area_oficial=dto.official_area_value if hasattr(dto, "official_area_value") else None,
                building_parts=[],
            )

        if hasattr(dto, "construction_nature"):
            return OtherConstruction(
                **base_fields,
                naturaleza=dto.construction_nature,
            )

        raise ValueError(f"Tipo de construccion desconocido: {type(dto)}")
