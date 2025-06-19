import pytest
from escatastrolib import Municipio

def test_valid_municipio_initialization():
    municipio = Municipio(provincia='Madrid', municipio='Madrid')
    assert municipio.provincia == 'Madrid'
    assert municipio.municipio == 'Madrid'.upper()

def test_invalid_municipio_initialization():
    with pytest.raises(Exception):
        Municipio(provincia='Madrid', municipio='InvalidMunicipio')

def test_missing_municipio_initialization():
    with pytest.raises(Exception):
        Municipio(provincia='Madrid', municipio=None)
