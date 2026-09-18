from escatastrolib.parsers.CatastroES.Croquis.parser import CroquisParser
from escatastrolib.parsers.CatastroES.Croquis.dto import CroquisDTO


class TestCroquisParser:
    def test_parse_url(self):
        parser = CroquisParser()
        result = parser.parse("https://www.example.com/croquis/123.png")
        assert isinstance(result, CroquisDTO)
        assert result.url == "https://www.example.com/croquis/123.png"

    def test_parse_none_returns_none(self):
        parser = CroquisParser()
        result = parser.parse(None)
        assert result.url is None

    def test_parse_empty_string(self):
        parser = CroquisParser()
        result = parser.parse("")
        assert result.url is None
