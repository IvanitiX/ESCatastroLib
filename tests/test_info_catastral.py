import pytest
import json
from escatastrolib import ParcelaCatastral, MetaParcela
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
        
def test_export_geojson_parcela():
    info = ParcelaCatastral(rc='28067A023001490000FJ')
    geojson_output = json.loads(info.to_json())
    assert isinstance(geojson_output, dict)  # Ensure output is a dictionary
    assert 'type' in geojson_output and geojson_output['type'] == 'FeatureCollection'
    assert 'features' in geojson_output and len(geojson_output['features']) > 0

def test_export_csv_parcela():
    info = ParcelaCatastral(rc='28067A023001490000FJ')
    csv_output = info.to_csv()
    assert isinstance(csv_output, str)  # Ensure output is a string
    assert 'rc' in csv_output  # Check if 'rc' is in the CSV output
    assert 'tipo' in csv_output  # Check if 'tipo' is in the CSV output

def test_export_geojson_metaparcela():
    info = MetaParcela(provincia='Madrid', municipio='Madrid', poligono='1', parcela='1')  # Assuming this is a valid metaparcela
    geojson_output = json.loads(info.to_json())
    assert isinstance(geojson_output, dict)  # Ensure output is a dictionary
    assert 'type' in geojson_output and geojson_output['type'] == 'FeatureCollection'
    assert 'features' in geojson_output and len(geojson_output['features']) > 0

def test_export_csv_metaparcela():
    info = MetaParcela(provincia='Madrid', municipio='Madrid', poligono='1', parcela='1')  # Assuming this is a valid metaparcela
    csv_output = info.to_csv()
    assert isinstance(csv_output, str)  # Ensure output is a string
    assert 'rc' in csv_output  # Check if 'rc' is in the CSV output
    assert 'tipo' in csv_output  # Check if 'tipo' is in the CSV output
