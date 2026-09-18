import pytest
from unittest.mock import MagicMock
from escatastrolib.parsers.CatastroES.Coordenadas.parser import (
    RCaCoordenadasParser,
    CoordenadasaRCParser,
)
from escatastrolib.parsers.CatastroES.Coordenadas.dto import CentroideDTO, RefCatDTO


def make_response(data):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = data
    resp.raise_for_status = MagicMock()
    return resp


class TestRCaCoordenadasParser:
    def test_parse_rc_to_coordenadas(self):
        data = {
            "Consulta_CPMRCResult": {
                "coordenadas": {
                    "coord": [
                        {
                            "pc": {"pc1": "3182116", "pc2": "VK4738A"},
                            "geo": {"xcen": "443000", "ycen": "4478000", "srs": "EPSG:25830"},
                        }
                    ]
                }
            }
        }
        parser = RCaCoordenadasParser()
        result = parser.parse(make_response(data))

        assert len(result) == 1
        assert isinstance(result[0], CentroideDTO)
        assert result[0].x == "443000"
        assert result[0].y == "4478000"
        assert result[0].sr == "EPSG:25830"

    def test_parse_empty_coords(self):
        data = {"Consulta_CPMRCResult": {"coordenadas": {"coord": {}}}}
        parser = RCaCoordenadasParser()
        result = parser.parse(make_response(data))
        assert result == []

    def test_parse_multiple_coords(self):
        data = {
            "Consulta_CPMRCResult": {
                "coordenadas": {
                    "coord": [
                        {"pc": {"pc1": "1", "pc2": "A"}, "geo": {"xcen": "100", "ycen": "200", "srs": "EPSG:4326"}},
                        {"pc": {"pc1": "2", "pc2": "B"}, "geo": {"xcen": "300", "ycen": "400", "srs": "EPSG:4326"}},
                    ]
                }
            }
        }
        parser = RCaCoordenadasParser()
        result = parser.parse(make_response(data))
        assert len(result) == 2


class TestCoordenadasaRCParser:
    def test_parse_coordenadas_to_rc(self):
        data = {
            "Consulta_RCCOORResult": {
                "coordenadas": {
                    "coord": [
                        {
                            "pc": {"pc1": "3182116", "pc2": "VK4738A"},
                            "geo": {"xcen": "443000", "ycen": "4478000"},
                        }
                    ]
                }
            }
        }
        parser = CoordenadasaRCParser()
        result = parser.parse(make_response(data))

        assert len(result) == 1
        assert isinstance(result[0], RefCatDTO)
        assert result[0].rc == "3182116VK4738A"
