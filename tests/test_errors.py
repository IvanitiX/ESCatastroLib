import pytest
from unittest.mock import MagicMock
from escatastrolib.errors.ErrorServidorDGC import comprobar_errores, ErrorServidorSedeCatastro


class TestComprobarErrores:
    def test_status_not_200_raises(self):
        @comprobar_errores
        def fake_func():
            resp = MagicMock()
            resp.status_code = 500
            resp.content = b""
            return resp

        with pytest.raises(ErrorServidorSedeCatastro, match="Status no es 200"):
            fake_func()

    def test_empty_content_raises(self):
        @comprobar_errores
        def fake_func():
            resp = MagicMock()
            resp.status_code = 200
            resp.content = b""
            return resp

        with pytest.raises(ErrorServidorSedeCatastro, match="Resultado vacio"):
            fake_func()

    def test_lerr_with_err_raises(self):
        @comprobar_errores
        def fake_func():
            resp = MagicMock()
            resp.status_code = 200
            resp.content = b'{"key": "value"}'
            resp.json.return_value = {
                "consultaResult": {
                    "lerr": {
                        "err": [{"des": "Error de prueba"}]
                    }
                }
            }
            return resp

        with pytest.raises(ErrorServidorSedeCatastro, match="Error de prueba"):
            fake_func()

    def test_lerr_list_raises(self):
        @comprobar_errores
        def fake_func():
            resp = MagicMock()
            resp.status_code = 200
            resp.content = b'{"key": "value"}'
            resp.json.return_value = {
                "consultaResult": {
                    "lerr": [{"des": "Error en lista"}]
                }
            }
            return resp

        with pytest.raises(ErrorServidorSedeCatastro, match="Error en lista"):
            fake_func()

    def test_valid_response_returns(self):
        @comprobar_errores
        def fake_func():
            resp = MagicMock()
            resp.status_code = 200
            resp.content = b'{"key": "value"}'
            resp.json.return_value = {"consultaResult": {"data": "ok"}}
            return resp

        result = fake_func()
        assert result is not None

    def test_non_dict_response_returns(self):
        @comprobar_errores
        def fake_func():
            resp = MagicMock()
            resp.status_code = 200
            resp.content = b'"just a string"'
            resp.json.return_value = "just a string"
            return resp

        result = fake_func()
        assert result is not None


class TestErrorServidorSedeCatastro:
    def test_message(self):
        exc = ErrorServidorSedeCatastro(mensaje="test error")
        assert "test error" in str(exc)
        assert "Error del Catastro" in str(exc)

    def test_default_message(self):
        exc = ErrorServidorSedeCatastro()
        assert "Error del Catastro" in str(exc)
