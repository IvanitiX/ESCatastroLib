import pytest
from unittest.mock import MagicMock
from escatastrolib.parsers.CatastroES.INSPIREBuildings.parser import INSPIREConstructionParser
from escatastrolib.parsers.CatastroES.INSPIREBuildings.dto import (
    BuildingDTO,
    BuildingPartDTO,
    OtherConstructionDTO,
)
from escatastrolib.parsers.common.dtos_geometria import GeometriaDTO


INSPIRE_BUILDING_PART_XML = """<?xml version="1.0" encoding="UTF-8"?>
<gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:bu-ext2d="http://inspire.ec.europa.eu/schemas/bu-ext2d/4.0"
    xmlns:bu-core2d="http://inspire.ec.europa.eu/schemas/bu-core2d/4.0"
    xmlns:base="http://inspire.ec.europa.eu/schemas/base/4.0">
    <gml:featureMember>
        <bu-ext2d:BuildingPart gml:id="BP.1">
            <bu-core2d:inspireId>
                <base:Identifier>
                    <base:localId>1</base:localId>
                    <base:namespace>ES.IGN.BP</base:namespace>
                </base:Identifier>
            </bu-core2d:inspireId>
            <bu-core2d:beginLifespanVersion>2020-01-01T00:00:00Z</bu-core2d:beginLifespanVersion>
            <bu-core2d:conditionOfConstruction>functional</bu-core2d:conditionOfConstruction>
            <bu-ext2d:geometry>
                <bu-core2d:BuildingGeometry>
                    <bu-core2d:geometry>
                        <gml:Surface gml:id="geom.1">
                            <gml:patches>
                                <gml:PolygonPatch>
                                    <gml:exterior>
                                        <gml:LinearRing>
                                            <gml:posList srsDimension="2">0 0 1 0 1 1 0 1 0 0</gml:posList>
                                        </gml:LinearRing>
                                    </gml:exterior>
                                </gml:PolygonPatch>
                            </gml:patches>
                        </gml:Surface>
                    </bu-core2d:geometry>
                    <bu-core2d:horizontalGeometryEstimatedAccuracy>0.1</bu-core2d:horizontalGeometryEstimatedAccuracy>
                    <bu-core2d:horizontalGeometryReference>point</bu-core2d:horizontalGeometryReference>
                    <bu-core2d:referenceGeometry>true</bu-core2d:referenceGeometry>
                </bu-core2d:BuildingGeometry>
            </bu-ext2d:geometry>
            <bu-ext2d:numberOfFloorsAboveGround>2</bu-ext2d:numberOfFloorsAboveGround>
            <bu-ext2d:numberOfFloorsBelowGround>1</bu-ext2d:numberOfFloorsBelowGround>
            <bu-ext2d:heightBelowGround uom="m">3.0</bu-ext2d:heightBelowGround>
        </bu-ext2d:BuildingPart>
    </gml:featureMember>
</gml:FeatureCollection>"""


class TestINSPIREConstructionParser:
    def test_parse_building_part(self):
        resp = MagicMock()
        resp.content = INSPIRE_BUILDING_PART_XML.encode("utf-8")

        parser = INSPIREConstructionParser()
        result = parser.parse(resp)

        assert len(result) == 1
        bp = result[0]
        assert isinstance(bp, BuildingPartDTO)
        assert bp.id == "BP.1"
        assert bp.local_id == "1"
        assert bp.namespace == "ES.IGN.BP"
        assert bp.condition_of_construction == "functional"
        assert bp.number_of_floors_above_ground == 2
        assert bp.number_of_floors_below_ground == 1
        assert bp.height_below_ground_m == 3.0
        assert bp.geometry is not None
        assert isinstance(bp.geometry, GeometriaDTO)
        assert bp.geometry.tipo == "Polygon"
        assert len(bp.geometry.puntos) == 5

    def test_parse_empty_raises(self):
        resp = MagicMock()
        resp.content = b""

        parser = INSPIREConstructionParser()
        with pytest.raises(ValueError, match="No hay información"):
            parser.parse(resp)

    def test_parse_exception_report(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
        <ExceptionReport>
            <Exception>
                <ExceptionText>Error de prueba</ExceptionText>
            </Exception>
        </ExceptionReport>"""
        resp = MagicMock()
        resp.content = xml.encode("utf-8")

        parser = INSPIREConstructionParser()
        with pytest.raises(ValueError, match="Error de prueba"):
            parser.parse(resp)

    def test_geometry_to_shapely(self):
        resp = MagicMock()
        resp.content = INSPIRE_BUILDING_PART_XML.encode("utf-8")

        parser = INSPIREConstructionParser()
        result = parser.parse(resp)

        shapely = result[0].geometry.to_shapely()
        assert shapely is not None
        assert shapely.geom_type == "Polygon"
        assert shapely.is_valid
        assert shapely.area == 1.0
