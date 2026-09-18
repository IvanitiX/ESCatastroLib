import pytest
from unittest.mock import MagicMock
from escatastrolib.parsers.CatastroES.CartoCiudad.parser import CartoCiudadParser
from escatastrolib.parsers.CatastroES.CartoCiudad.dto import CartoCiudadDTO


def make_response(text, status_code=200):
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.raise_for_status = MagicMock()
    return resp


class TestCartoCiudadParser:
    def test_parse_json(self):
        text = '{"id":"1","province":"Madrid","muni":"Madrid","address":"Calle Alcala","lat":40.4,"lng":-3.7}'
        parser = CartoCiudadParser()
        result = parser.parse(make_response(text))

        assert isinstance(result, CartoCiudadDTO)
        assert result.id == "1"
        assert result.provincia == "Madrid"
        assert result.municipio == "Madrid"
        assert result.direccion == "Calle Alcala"
        assert result.latitud == 40.4
        assert result.longitud == -3.7

    def test_parse_jsonp(self):
        text = 'callback({"id":"1","province":"Madrid","muni":"Madrid"});'
        parser = CartoCiudadParser()
        result = parser.parse(make_response(text))

        assert isinstance(result, CartoCiudadDTO)
        assert result.id == "1"

    def test_parse_empty_returns_none(self):
        parser = CartoCiudadParser()
        result = parser.parse(make_response(""))
        assert result is None

    def test_parse_whitespace_only_returns_none(self):
        parser = CartoCiudadParser()
        result = parser.parse(make_response("   "))
        assert result is None

    def test_parse_invalid_format_raises(self):
        parser = CartoCiudadParser()
        with pytest.raises(ValueError, match="no es JSON ni JSONP válido"):
            parser.parse(make_response("not valid at all"))

    def test_parse_non_dict_raises(self):
        parser = CartoCiudadParser()
        with pytest.raises(ValueError, match="formato esperado"):
            parser.parse(make_response("[1,2,3]"))

    def test_parse_with_optional_fields(self):
        text = '{"id":"1","province":"Madrid","postalCode":"28001","portalNumber":5,"sinNumero":true,"extension":false,"refCatastral":"12345"}'
        parser = CartoCiudadParser()
        result = parser.parse(make_response(text))

        assert result.codigo_postal == "28001"
        assert result.numero == 5
        assert result.sin_numero is True
        assert result.extension is False
        assert result.referencia_catastral == "12345"

    def test_parse_comunidad_autonoma(self):
        text = '{"id":"1","comunidadAutonoma":"Comunidad de Madrid"}'
        parser = CartoCiudadParser()
        result = parser.parse(make_response(text))
        assert result.comunidad_autonoma == "Comunidad de Madrid"
