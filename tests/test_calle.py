import pytest
from escatastrolib import Municipio, Calle

def test_valid_calle_initialization():
    municipio = Municipio(provincia='Madrid', municipio='Madrid')
    calle = Calle(municipio=municipio, nombre_calle='Gran Via', tipo_via='CL')
    assert calle.municipio == municipio
    assert calle.calle == 'Gran Via'.upper()  # Assuming the API returns this value

def test_missing_calle_name():
    municipio = Municipio(provincia='Madrid', municipio='Madrid')
    with pytest.raises(Exception):
        Calle(municipio=municipio, nombre_calle=None)

def test_multiple_calle_matches():
    municipio = Municipio(provincia='Madrid', municipio='Madrid')
    with pytest.raises(Exception):
        Calle(municipio=municipio, nombre_calle='AmbiguousName', tipo_via='CL')  # Assuming this name is ambiguous
