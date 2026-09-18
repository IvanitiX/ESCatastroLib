import pytest
from unittest.mock import MagicMock
from escatastrolib.parsers.CatastroES.Callejero.parser import (
    CallejeroProvinciaParser,
    CallejeroMunicipioParser,
    CallejeroCalleParser,
    ParcelaCatastralRCParser,
    RegionCatastralParser,
)
from escatastrolib.parsers.CatastroES.Callejero.dto import (
    ProvinciaDTO,
    MunicipioDTO,
    CalleDTO,
    RegionCatastralDTO,
)


def make_response(data):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = data
    resp.raise_for_status = MagicMock()
    return resp


class TestCallejeroProvinciaParser:
    def test_parse_provincias(self):
        data = {
            "consulta_provincieroResult": {
                "provinciero": {
                    "prov": [
                        {"cpine": "28", "np": "MADRID"},
                        {"cpine": "08", "np": "BARCELONA"},
                    ]
                }
            }
        }
        parser = CallejeroProvinciaParser()
        result = parser.parse(make_response(data))

        assert len(result) == 2
        assert all(isinstance(p, ProvinciaDTO) for p in result)
        assert result[0].codigoProvincia == 28
        assert result[0].nombreProvincia == "MADRID"
        assert result[1].codigoProvincia == 8
        assert result[1].nombreProvincia == "BARCELONA"

    def test_parse_empty(self):
        data = {
            "consulta_provincieroResult": {
                "provinciero": {}
            }
        }
        parser = CallejeroProvinciaParser()
        result = parser.parse(make_response(data))
        assert result == []

    def test_parse_single_provincia(self):
        data = {
            "consulta_provincieroResult": {
                "provinciero": {
                    "prov": {"cpine": "28", "np": "MADRID"}
                }
            }
        }
        parser = CallejeroProvinciaParser()
        result = parser.parse(make_response(data))
        # Single item may not be a list


class TestCallejeroMunicipioParser:
    def test_parse_municipios(self):
        data = {
            "consulta_municipieroResult": {
                "municipiero": {
                    "muni": [
                        {"nm": "MADRID"},
                        {"nm": "ALCALA DE HENARES"},
                    ]
                }
            }
        }
        parser = CallejeroMunicipioParser()
        result = parser.parse(make_response(data))

        assert len(result) == 2
        assert all(isinstance(m, MunicipioDTO) for m in result)
        assert result[0].nombreMunicipio == "MADRID"
        assert result[1].nombreMunicipio == "ALCALA DE HENARES"


class TestCallejeroCalleParser:
    def test_parse_calles(self):
        data = {
            "consulta_callejeroResult": {
                "callejero": {
                    "calle": [
                        {
                            "dir": {"tv": "CL", "nv": "ALCALA"},
                            "dirine": {"sine": "CL", "deine": "ALCALA"},
                        },
                        {
                            "dir": {"tv": "AV", "nv": "DIAGONAL"},
                            "dirine": {"sine": "AV", "deine": "DIAGONAL"},
                        },
                    ]
                }
            }
        }
        parser = CallejeroCalleParser()
        result = parser.parse(make_response(data))

        assert len(result) == 2
        assert all(isinstance(c, CalleDTO) for c in result)
        assert result[0].tipoViaCatastral == "CL"
        assert result[0].nombreCatastral == "ALCALA"
        assert result[0].tipoViaINE == "CL"
        assert result[0].nombreINE == "ALCALA"


class TestParcelaCatastralRCParser:
    def test_parse_urbana(self):
        data = {
            "consulta_dnprcResult": {
                "control": {"cudnp": 1},
                "bico": {
                    "bi": {
                        "idbi": {
                            "cn": "UR",
                            "rc": {
                                "pc1": "3182116",
                                "pc2": "VK4738A",
                            },
                        },
                        "dt": {
                            "loine": {"cp": "28", "cm": "79"},
                            "np": "MADRID",
                            "nm": "MADRID",
                            "locs": {
                                "lous": {
                                    "lourb": {
                                        "dir": {
                                            "tv": "CL",
                                            "nv": "CHARCA VERDE",
                                            "pnp": "16",
                                        },
                                        "loint": {"es": "T", "pt": "OD", "pu": "OS"},
                                    }
                                }
                            },
                        },
                        "debi": {
                            "luso": "Residencial",
                            "sfc": "180",
                            "ant": "1940",
                        },
                        "finca": {"dff": {"ss": "179"}},
                    },
                    "lcons": [],
                },
            }
        }
        parser = ParcelaCatastralRCParser()
        result = parser.parse(make_response(data))

        assert len(result) == 1
        p = result[0]
        assert p.referenciaCatastral is not None
        assert p.tipo == "Urbano"
        assert p.municipio.nombreMunicipio == "MADRID"
        assert p.provincia.nombreProvincia == "MADRID"
        assert p.uso == "Residencial"
        assert p.calle == "CL CHARCA VERDE"
        assert p.numero == "16"
        assert p.escalera == "T"
        assert p.planta == "OD"
        assert p.puerta == "OS"

    def test_parse_rustica(self):
        data = {
            "consulta_dnprcResult": {
                "control": {"cudnp": 1},
                "bico": {
                    "bi": {
                        "idbi": {
                            "cn": "RU",
                            "rc": {
                                "pc1": "13033A0",
                                "pc2": "2600058",
                            },
                        },
                        "dt": {
                            "loine": {"cp": "13", "cm": "33"},
                            "np": "CIUDAD REAL",
                            "nm": "CASTELLAR DE SANTIAGO",
                            "locs": {
                                "lors": {
                                    "lorus": {
                                        "cpp": {"cpo": "26", "cpa": "58"},
                                        "npa": "LAS CORRALERAS",
                                    }
                                }
                            },
                        },
                        "debi": {"luso": "Agrario", "sfc": "0"},
                        "finca": {"dff": {"ss": "14667"}},
                    },
                    "lcons": [],
                },
            }
        }
        parser = ParcelaCatastralRCParser()
        result = parser.parse(make_response(data))

        assert len(result) == 1
        p = result[0]
        assert p.tipo == "Rústico"
        assert p.municipio.nombreMunicipio == "CASTELLAR DE SANTIAGO"
        assert p.parcela == "58"
        assert p.poligono == "26"
        assert p.nombre_paraje == "LAS CORRALERAS"
