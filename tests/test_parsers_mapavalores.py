import pytest
from unittest.mock import MagicMock
from escatastrolib.parsers.CatastroES.MapaValoresRusticos.parser import ValoresRusticosParser
from escatastrolib.parsers.CatastroES.MapaValoresRusticos.dto import ValoresRusticosDTO
from escatastrolib.parsers.CatastroES.MapaValoresUrbanos.parser import ValoresUrbanosParser
from escatastrolib.parsers.CatastroES.MapaValoresUrbanos.dto import RecintoValorUrbanoDTO, ValorUrbanoDTO


def make_response(data):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = data
    resp.raise_for_status = MagicMock()
    return resp


class TestValoresRusticosParser:
    def test_parse(self):
        data = {
            "features": [
                {
                    "properties": {
                        "REGIONAL": "01",
                        "NOMBRE": "Andalucía",
                        "ARZ": 1.0,
                        "CIT": 2.0,
                        "CBP": 3.0,
                        "SBT": 4.0,
                        "FCR": 5.0,
                        "FCS": 6.0,
                        "FSR": 7.0,
                        "FSS": 8.0,
                        "HUE": 9.0,
                        "OLR": 10.0,
                        "OLS": 11.0,
                        "PST": 12.0,
                        "PLT": 13.0,
                        "PRD": 14.0,
                        "TAR": 15.0,
                        "TAS": 16.0,
                        "VIR": 17.0,
                        "VIS": 18.0,
                    }
                }
            ]
        }
        parser = ValoresRusticosParser()
        result = parser.parse(make_response(data))

        assert len(result) == 1
        v = result[0]
        assert isinstance(v, ValoresRusticosDTO)
        assert v.region == "01"
        assert v.nombre_region == "Andalucía"
        assert v.valor_m2_arrozales == 1.0
        assert v.valor_m2_citricos == 2.0
        assert v.valor_m2_cultivos_bajo_plastico == 3.0
        assert v.valor_m2_tierras_arables_regadio == 15.0
        assert v.valor_m2_vinedos_secano == 18.0

    def test_parse_empty(self):
        data = {"features": []}
        parser = ValoresRusticosParser()
        result = parser.parse(make_response(data))
        assert result == []


class TestValoresUrbanosParser:
    def test_parse(self):
        data = {
            "features": [
                {
                    "geometry": {"type": "Point", "coordinates": [-3.7, 40.4]},
                    "properties": {
                        "Ptipo0": {
                            "id_producto_tipo": "PT01",
                            "id_delegacion": "D01",
                            "id_municipio": "28079",
                            "fecha": "2024-01-01",
                            "id_recinto_valoracion": "RV01",
                            "orden": 1,
                            "num_inmueble": 10,
                            "codigo_uso": "U01",
                            "tipologia": "Vivienda",
                            "coef_propiedad": 0.5,
                            "categoria": "A",
                            "antiguedad": 10,
                            "conservacion": "Buena",
                            "superficie": 100.0,
                            "tipologia_anejos": "None",
                            "edificabilidad": 1.0,
                            "num_altura": 3,
                            "superficie_minima": 50.0,
                            "superficie_suelo": 200.0,
                            "porc_suelo_interior": 0.8,
                            "val_suelo": 1000.0,
                            "val_construccion_pt": 500.0,
                            "val_construccion_pe": 300.0,
                            "val_suelos_gar": 200.0,
                            "val_construccion_pt_garaje": 100.0,
                            "val_construccion_pe_garaje": 50.0,
                            "val_catastral": 2000.0,
                            "num_inmuebles_recinto": 50,
                            "num_garajes_recinto": 20,
                            "val_tipo": 1500.0,
                            "val_tipo_m2": 15.0,
                            "val_tipo_m2_min": 10.0,
                            "val_tipo_mostrar": "1500.00",
                            "val_estandar": 1800.0,
                            "val_estandar_m2": 18.0,
                        }
                    },
                }
            ]
        }
        parser = ValoresUrbanosParser()
        result = parser.parse(make_response(data))

        assert len(result) == 1
        r = result[0]
        assert isinstance(r, RecintoValorUrbanoDTO)
        assert r.geometry == {"type": "Point", "coordinates": [-3.7, 40.4]}
        assert len(r.ptipos) == 1
        pt = r.ptipos[0]
        assert isinstance(pt, ValorUrbanoDTO)
        assert pt.id_producto_tipo == "PT01"
        assert pt.codigo_uso == "U01"
        assert pt.tipologia == "Vivienda"
        assert pt.superficie == 100.0
        assert pt.val_catastral == 2000.0
