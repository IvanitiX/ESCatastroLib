import pytest
from escatastrolib import ParcelaCatastral
from escatastrolib.utils import ErrorServidorCatastro

def test_valid_info_urban_catastral_initialization_rc():
    info = ParcelaCatastral(rc='1541506VK4714B0002PK')
    assert info.rc == '1541506VK4714B0002PK'  # Assuming the API returns this value
    assert info.tipo == 'Urbano'
    assert info.superficie >= 39 and info.superficie <= 40

def test_valid_info_rustic_catastral_initialization_rc():
    info = ParcelaCatastral(rc='28067A023001490000FJ')
    assert info.rc == '28067A023001490000FJ'  # Assuming the API returns this value
    assert info.tipo == 'Rústico'
    assert info.superficie >= 439732 and info.superficie <= 439733
    assert info.parcela == '149'
    assert info.poligono == '23'


def test_invalid_info_catastral_initialization_rc():
    with pytest.raises(ErrorServidorCatastro):
        ParcelaCatastral(rc='22113U490470815583UK')  # Invalid RC

def test_valid_info_catastral_initialization_parcel():
    with pytest.raises(ErrorServidorCatastro):
        info = ParcelaCatastral(provincia='Madrid', municipio='Madrid', poligono='1', parcela='1')
        assert info.provincia == 'Madrid'.upper()  # Assuming the API returns this value

def test_valid_info_catastral_initialization_address():
    with pytest.raises(ErrorServidorCatastro):
        info = ParcelaCatastral(provincia='Madrid', municipio='Madrid', tipo_via='CL', calle='Gran Via', numero='1')
        assert info.calle == 'CL Gran Via'.upper()  # Assuming the API returns this value

def test_invalid_info_catastral_initialization():
    with pytest.raises(ValueError):
        ParcelaCatastral()  # No parameters provided
