import pytest
from unittest.mock import patch, MagicMock
from escatastrolib.providers.CatastroES.Callejero import CallejeroAPIProvider
from escatastrolib.providers.CatastroES.CartoCiudad import CartoCiudadProvider
from escatastrolib.providers.CatastroES.Coordenadas import CoordenadasAPIProvider
from escatastrolib.providers.CatastroES.Croquis import CroquisAPIProvider
from escatastrolib.providers.CatastroES.INSPIREBuildings import InspireBuildingsProvider
from escatastrolib.providers.CatastroES.INSPIREParcelas import InspireParcelasProvider
from escatastrolib.providers.CatastroES.MapaValoresRusticos import MapaValoresRusticosProvider
from escatastrolib.providers.CatastroES.MapaValoresUrbanos import MapaValoresUrbanosProvider


def make_ok_response(data=None):
    resp = MagicMock()
    resp.status_code = 200
    resp.content = b'{"ok": true}' if data is None else b'ok'
    resp.json.return_value = data or {"ok": True}
    resp.raise_for_status = MagicMock()
    return resp


class TestCallejeroAPIProvider:
    @patch("escatastrolib.providers.CatastroES.Callejero.requests.get")
    def test_consulta_provincias(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CallejeroAPIProvider()
        result = provider.consulta_provincias()
        assert result.status_code == 200

    @patch("escatastrolib.providers.CatastroES.Callejero.requests.get")
    def test_consulta_municipios(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CallejeroAPIProvider()
        result = provider.consulta_municipios(provincia="MADRID", municipio="madr")
        assert result.status_code == 200
        call_params = mock_get.call_args[1]["params"]
        assert call_params["provincia"] == "MADRID"
        assert call_params["municipio"] == "madr"

    @patch("escatastrolib.providers.CatastroES.Callejero.requests.get")
    def test_consulta_calles(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CallejeroAPIProvider()
        result = provider.consulta_calles(
            provincia="MADRID", municipio="MADRID", nombre_calle="Alcala"
        )
        assert result.status_code == 200

    @patch("escatastrolib.providers.CatastroES.Callejero.requests.get")
    def test_consulta_parcela_por_rc(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CallejeroAPIProvider()
        result = provider.consulta_parcela_por_rc(rc="3182116VK4738A")
        assert result.status_code == 200
        call_params = mock_get.call_args[1]["params"]
        assert call_params["RefCat"] == "3182116VK4738A"

    @patch("escatastrolib.providers.CatastroES.Callejero.requests.get")
    def test_consulta_parcela_por_polpar(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CallejeroAPIProvider()
        result = provider.consulta_parcela_por_polpar(
            municipio="MADRID", provincia="MADRID", poligono=1, parcela=1
        )
        assert result.status_code == 200

    @patch("escatastrolib.providers.CatastroES.Callejero.requests.get")
    def test_consulta_parcela_por_direccion(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CallejeroAPIProvider()
        result = provider.consulta_parcela_por_direccion(
            municipio="MADRID", provincia="MADRID", tipo_via="CL",
            calle="ALCALA", numero="1"
        )
        assert result.status_code == 200


class TestCoordenadasAPIProvider:
    @patch("escatastrolib.providers.CatastroES.Coordenadas.requests.get")
    def test_consulta_rc_por_coordenadas(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CoordenadasAPIProvider()
        result = provider.consulta_rc_por_coordenadas(lat=40.4, lon=-3.7)
        assert result.status_code == 200
        call_params = mock_get.call_args[1]["params"]
        assert call_params["CoorX"] == -3.7
        assert call_params["CoorY"] == 40.4

    @patch("escatastrolib.providers.CatastroES.Coordenadas.requests.get")
    def test_convertir_rc_a_coordenadas(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CoordenadasAPIProvider()
        result = provider.convertir_rc_a_coordenadas(rc="3182116VK4738A")
        assert result.status_code == 200


class TestCartoCiudadProvider:
    @patch("escatastrolib.providers.CatastroES.CartoCiudad.requests.get")
    def test_consulta_por_direccion(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = CartoCiudadProvider()
        result = provider.consulta_por_direccion(
            direccion="Calle Alcala 1", municipio="Madrid"
        )
        assert result.status_code == 200
        call_params = mock_get.call_args[1]["params"]
        assert "Alcala 1" in call_params["q"]
        assert "Madrid" in call_params["q"]


class TestCroquisAPIProvider:
    @patch("escatastrolib.providers.CatastroES.Croquis.requests.get")
    def test_consulta_url_croquis(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.url = "https://www.example.com/croquis.png"
        mock_get.return_value = mock_resp
        provider = CroquisAPIProvider()
        result = provider.consulta_url_croquis(rc="3182116VK4738A")
        assert result == "https://www.example.com/croquis.png"


class TestInspireBuildingsProvider:
    @patch("escatastrolib.providers.CatastroES.INSPIREBuildings.requests.get")
    def test_consulta_partes_edificios(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = InspireBuildingsProvider()
        result = provider.consulta_partes_edificios(rc="3182116VK4738A")
        assert result.status_code == 200
        call_params = mock_get.call_args[1]["params"]
        assert call_params["STOREDQUERIE_ID"] == "GetBuildingPartByParcel"

    @patch("escatastrolib.providers.CatastroES.INSPIREBuildings.requests.get")
    def test_consulta_edificios(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = InspireBuildingsProvider()
        result = provider.consulta_edificios(rc="3182116VK4738A")
        assert result.status_code == 200
        call_params = mock_get.call_args[1]["params"]
        assert call_params["STOREDQUERIE_ID"] == "GetBuildingByParcel"

    @patch("escatastrolib.providers.CatastroES.INSPIREBuildings.requests.get")
    def test_consulta_otras_construcciones(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = InspireBuildingsProvider()
        result = provider.consulta_otras_construcciones(rc="3182116VK4738A")
        assert result.status_code == 200
        call_params = mock_get.call_args[1]["params"]
        assert call_params["STOREDQUERIE_ID"] == "GetOtherBuildingByParcel"


class TestInspireParcelasProvider:
    @patch("escatastrolib.providers.CatastroES.INSPIREParcelas.requests.get")
    def test_consultar_coordenadas_parcela(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = InspireParcelasProvider()
        result = provider.consultar_coordenadas_parcela(
            rc="3182116VK4738A", projection="EPSG:4326"
        )
        assert result.status_code == 200
        call_params = mock_get.call_args[1]["params"]
        assert call_params["refcat"] == "3182116VK4738A"
        assert call_params["srsname"] == "EPSG:4326"


class TestMapaValoresRusticosProvider:
    @patch("escatastrolib.providers.CatastroES.MapaValoresRusticos.requests.get")
    def test_consulta_valores_rusticos_m2(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = MapaValoresRusticosProvider()
        result = provider.consulta_valores_rusticos_m2(
            anio=2024, bbox_3857="0,0,100,100"
        )
        assert result.status_code == 200


class TestMapaValoresUrbanosProvider:
    @patch("escatastrolib.providers.CatastroES.MapaValoresUrbanos.requests.get")
    def test_consultar_valores_urbanos_m2(self, mock_get):
        mock_get.return_value = make_ok_response()
        provider = MapaValoresUrbanosProvider()
        result = provider.consultar_valores_urbanos_m2(
            x=-3.7, y=40.4, anio=2024
        )
        assert result.status_code == 200
