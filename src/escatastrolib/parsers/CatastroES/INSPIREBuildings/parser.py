# parsers.py

from datetime import datetime
from typing import Any

import requests
import xmltodict

from .dto import BuildingDTO, BuildingPartDTO, OtherConstructionDTO
from ...common.dtos_geometria import GeometriaDTO, PuntoDTO
from ...typing import to_int


class INSPIREConstructionParser:
    """Parser de respuestas INSPIRE BU (Buildings) en formato WFS XML.

    Extrae construcciones de las respuestas GML/WFS del servicio INSPIRE
    de edificios del Catastro. Maneja tres tipos de entidades:
    - ``BuildingPart``: partes constructivas de un edificio.
    - ``Building``: edificios completos con uso, unidades y superficie oficial.
    - ``OtherConstruction``: construcciones especiales (garajes, piscinas, etc.).

    La geometría se extrae de ``gml:Surface`` con ``PolygonPatch``.
    """

    def parse(self, response: requests.Response) -> list[BuildingPartDTO | BuildingDTO | OtherConstructionDTO]:
        """Parsea una respuesta WFS XML de construcciones INSPIRE BU.

        Args:
            response: Objeto requests.Response con contenido XML GML/WFS.

        Returns:
            list: Lista de DTOs de construcción (BuildingPartDTO, BuildingDTO
                u OtherConstructionDTO).

        Raises:
            ValueError: Si el contenido está vacío o la API retorna una excepción.
        """
        content = response.content

        if len(content) == 0:
            raise ValueError("No hay información")

        data = xmltodict.parse(content)

        if data.get("ExceptionReport") is not None:
            self._raise_exception(data)

        return self._to_dtos(data)

    def _raise_exception(self, data: dict[str, Any]) -> None:
        report = data.get("ExceptionReport", {})
        exception = report.get("Exception", {})

        raise ValueError(
            exception.get(
                "ExceptionText",
                "No se proporcionó reporte",
            )
        )

    def _to_dtos(self, data: dict[str, Any]) -> list[BuildingPartDTO | BuildingDTO | OtherConstructionDTO]:
        features = data.get("gml:FeatureCollection", {})

        members = features.get("gml:featureMember", [])

        if not isinstance(members, list):
            members = [members]

        dtos: list[BuildingPartDTO | BuildingDTO | OtherConstructionDTO] = []

        for member in members:
            building_part = member.get("bu-ext2d:BuildingPart")
            building = member.get("bu-ext2d:Building")
            other_construction = member.get(
                "bu-ext2d:OtherConstruction"
            )

            if building_part:
                dtos.append(
                    self._parse_building_part(building_part)
                )

            elif building:
                dtos.append(
                    self._parse_building(building)
                )

            elif other_construction:
                dtos.append(
                    self._parse_other_construction(
                        other_construction
                    )
                )

        return dtos

    def _parse_building_part(self, data: dict[str, Any]) -> BuildingPartDTO:
        inspire_id = data.get("bu-core2d:inspireId", {})

        return BuildingPartDTO(
            id=data.get("@gml:id"),
            local_id=inspire_id.get("base:Identifier").get("base:localId"),
            namespace=inspire_id.get("base:Identifier").get("base:namespace"),
            begin_lifespan_version=self._parse_datetime(
                data.get("bu-core2d:beginLifespanVersion")
            ),
            condition_of_construction=data.get(
                "bu-core2d:conditionOfConstruction"
            ),
            addresses_href=data.get(
                "bu-core2d:addresses",
                {},
            ).get("@xlink:href"),
            cadastral_parcels_href=data.get(
                "bu-core2d:cadastralParcels",
                {},
            ).get("@xlink:href"),
            geometry=self._parse_geometry(
                data.get("bu-ext2d:geometry", {}).get("bu-core2d:BuildingGeometry",{}).get("bu-core2d:geometry",{})
            ),
            horizontal_geometry_estimated_accuracy_m=self._safe_float(
                data.get("bu-ext2d:geometry", {}).get("bu-core2d:BuildingGeometry",{}).get(
                    "bu-core2d:horizontalGeometryEstimatedAccuracy",
                )
            ),
            horizontal_geometry_reference=data.get("bu-ext2d:geometry", {}).get("bu-core2d:BuildingGeometry",{}).get(
                "bu-core2d:horizontalGeometryReference"
            ),
            reference_geometry=data.get("bu-ext2d:geometry", {}).get("bu-core2d:BuildingGeometry",{}).get(
                "bu-core2d:referenceGeometry"
            ),
            number_of_floors_above_ground=self._safe_int(
                data.get("bu-ext2d:numberOfFloorsAboveGround")
            ),
            number_of_floors_below_ground=self._safe_int(
                data.get("bu-ext2d:numberOfFloorsBelowGround")
            ),
            height_below_ground_m=self._safe_float(
                data.get("bu-ext2d:heightBelowGround", {}).get("#text")
            ),
        )

    def _parse_building(self, data: dict[str, Any]) -> BuildingDTO:
        inspire_id = data.get("bu-core2d:inspireId", {})
        construction_date = data.get(
            "bu-core2d:dateOfConstruction",
            {},
        )
        external_reference = data.get(
            "bu-core2d:externalReference",
            {},
        )
        document = data.get("bu-ext2d:document", {})
        official_area = data.get(
            "bu-ext2d:officialArea",
            {},
        )
        official_area_value = official_area.get(
            "bu-ext2d:value",
            {},
        )

        return BuildingDTO(
            id=data.get("@gml:id"),
            local_id=inspire_id.get("base:Identifier").get("base:localId"),
            namespace=inspire_id.get("base:Identifier").get("base:namespace"),
            begin_lifespan_version=self._parse_datetime(
                data.get("bu-core2d:beginLifespanVersion")
            ),
            condition_of_construction=data.get(
                "bu-core2d:conditionOfConstruction"
            ),
            addresses_href=data.get(
                "bu-core2d:addresses",
                {},
            ).get("@xlink:href"),
            cadastral_parcels_href=data.get(
                "bu-core2d:cadastralParcels",
                {},
            ).get("@xlink:href"),
            geometry=self._parse_geometry(
                data.get("bu-ext2d:geometry", {})
            ),
            end_lifespan_version=self._parse_datetime(
                data.get("bu-core2d:endLifespanVersion")
            ),
            date_of_construction_beginning=self._parse_datetime(
                construction_date.get("bu-core2d:beginning")
            ),
            date_of_construction_end=self._parse_datetime(
                construction_date.get("bu-core2d:end")
            ),
            external_reference_url=external_reference.get(
                "bu-core2d:informationSystem",
                {},
            ).get("@xlink:href"),
            external_reference=external_reference.get(
                "bu-core2d:reference"
            ),
            current_use=data.get("bu-ext2d:currentUse"),
            number_of_building_units=self._safe_int(
                data.get("bu-ext2d:numberOfBuildingUnits")
            ),
            number_of_dwellings=self._safe_int(
                data.get("bu-ext2d:numberOfDwellings")
            ),
            number_of_floors_above_ground=self._safe_int(
                data.get("bu-ext2d:numberOfFloorsAboveGround")
            ),
            document_link=document.get(
                "bu-ext2d:documentLink",
                {},
            ).get("@xlink:href"),
            document_format=document.get("bu-ext2d:format"),
            document_source_status=document.get(
                "bu-ext2d:sourceStatus"
            ),
            official_area_reference=official_area.get(
                "bu-ext2d:officialAreaReference"
            ),
            official_area_value=self._safe_float(
                official_area_value.get("#text")
            ),
            official_area_uom=official_area_value.get(
                "@uom"
            ),
        )

    def _parse_other_construction(self, data: dict[str, Any]) -> OtherConstructionDTO:
        inspire_id = data.get("bu-core2d:inspireId", {})

        return OtherConstructionDTO(
            id=data.get("@gml:id"),
            local_id=inspire_id.get("base:Identifier").get("base:localId"),
            namespace=inspire_id.get("base:Identifier").get("base:namespace"),
            begin_lifespan_version=self._parse_datetime(
                data.get("bu-core2d:beginLifespanVersion")
            ),
            condition_of_construction=data.get(
                "bu-core2d:conditionOfConstruction"
            ),
            addresses_href=data.get(
                "bu-core2d:addresses",
                {},
            ).get("@xlink:href"),
            cadastral_parcels_href=data.get(
                "bu-core2d:cadastralParcels",
                {},
            ).get("@xlink:href"),
            geometry=self._parse_geometry(
                data.get("bu-ext2d:geometry", {})
            ),
            construction_nature=data.get(
                "bu-ext2d:constructionNature"
            ),
        )

    def _parse_geometry(self, data: dict[str, Any]) -> GeometriaDTO:
        surface = data.get("gml:Surface", {})
        patches = surface.get("gml:patches", {})
        polygon_patch = patches.get(
            "gml:PolygonPatch",
            {},
        )
        exterior = polygon_patch.get(
            "gml:exterior",
            {},
        )
        linear_ring = exterior.get(
            "gml:LinearRing",
            {},
        )
        pos_list = linear_ring.get(
            "gml:posList",
            {},
        )

        srs_name = surface.get("@srsName", "")
        sr = srs_name.split("/")[-1] if srs_name else "EPSG:4326"
        dimensiones = to_int(pos_list.get("@srsDimension")) or 2

        coordinates = [
            float(value)
            for value in pos_list.get("#text", "").split()
        ]

        puntos = [
            PuntoDTO(
                sr=sr,
                dimensiones=dimensiones,
                coordenadas=coordinates[index:index + dimensiones],
            )
            for index in range(0, len(coordinates), dimensiones)
        ]

        return GeometriaDTO(
            sr=sr,
            tipo="Polygon",
            puntos=puntos,
        )

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if not value or isinstance(value, dict):
            return None

        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

    @staticmethod
    def _safe_int(value: Any, default: int = 0) -> int:
        if not value or isinstance(value, dict):
            return default
        return int(value)

    @staticmethod
    def _safe_float(value: Any, default: float = 0.0) -> float:
        if not value or isinstance(value, dict):
            return default
        return float(value)
