import pytest
from escatastrolib.utils import listar_provincias, listar_municipios, comprobar_errores, ErrorServidorCatastro

def test_listar_municipios_valid_provincia():
    # Assuming 'Madrid' is a valid province in the MAPEOS_PROVINCIAS
    municipios = listar_municipios(provincia='Madrid')
    assert isinstance(municipios, list)

def test_listar_municipios_invalid_provincia():
    with pytest.raises(Exception):
        listar_municipios(provincia='InvalidProvincia')

def test_comprobar_errores_valid_response():
    response = {'test': None}
    assert comprobar_errores(response) is True

def test_comprobar_errores_invalid_response():
    response = {'data':{'lerr': {'err': [{'cod': 'some_error_code'}]}}}
    with pytest.raises(Exception):
        comprobar_errores(response)
