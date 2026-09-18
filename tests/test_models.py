from escatastrolib.models.GeometriaCatastral import Geometria
from escatastrolib.models.Callejero import Municipio, Calle
from escatastrolib.models.RegionCatastral import RegionCatastral
from escatastrolib.models.Documentacion import Documento
from escatastrolib.models.Construction import (
    Construction,
    Building,
    BuildingPart,
    OtherConstruction,
)
from escatastrolib.models.ValorUrbano import ValorUrbano
from escatastrolib.models.ValorRustico import ValorRustico
from escatastrolib.models.ParcelaCatastral import (
    ParcelaUrbana,
    ParcelaRustica,
    ParcelaCatastral,
)


class TestGeometria:
    def test_create_point(self):
        geo = Geometria(
            sistema_referencia="EPSG:4326",
            coordenadas=[(40.0, -3.0)],
            tipo="Point",
        )
        assert geo.tipo == "Point"
        assert geo.coordenadas == [(40.0, -3.0)]

    def test_create_polygon(self):
        coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=coords, tipo="Polygon")
        assert geo.tipo == "Polygon"
        assert len(geo.coordenadas) == 5

    def test_to_shapely_point(self):
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=[(1.0, 2.0)], tipo="Point")
        s = geo.to_shapely()
        assert s is not None
        assert s.geom_type == "Point"
        assert s.x == 1.0
        assert s.y == 2.0

    def test_to_shapely_polygon(self):
        coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=coords, tipo="Polygon")
        s = geo.to_shapely()
        assert s is not None
        assert s.geom_type == "Polygon"
        assert s.is_valid

    def test_area_polygon(self):
        coords = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=coords, tipo="Polygon")
        assert geo.area == 4.0

    def test_perimetro_polygon(self):
        coords = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=coords, tipo="Polygon")
        assert geo.perimetro == 4.0

    def test_area_point_returns_0(self):
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=[(1.0, 2.0)], tipo="Point")
        assert geo.area == 0.0

    def test_perimetro_point_returns_0(self):
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=[(1.0, 2.0)], tipo="Point")
        assert geo.perimetro == 0.0

    def test_to_shapely_empty_returns_none(self):
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=[], tipo="Point")
        assert geo.to_shapely() is None

    def test_area_empty_returns_0(self):
        geo = Geometria(sistema_referencia="EPSG:4326", coordenadas=[], tipo="Polygon")
        assert geo.area == 0.0


class TestMunicipio:
    def test_create(self):
        m = Municipio(municipio="MADRID", provincia="MADRID")
        assert m.municipio == "MADRID"
        assert m.provincia == "MADRID"


class TestCalle:
    def test_create(self):
        m = Municipio(municipio="MADRID", provincia="MADRID")
        c = Calle(municipio=m, tipo_via="CL", calle="ALCALA")
        assert c.tipo_via == "CL"
        assert c.calle == "ALCALA"
        assert c.municipio.municipio == "MADRID"


class TestRegionCatastral:
    def test_create(self):
        r = RegionCatastral(descripcion="VIVIENDA", superficie=60.0)
        assert r.descripcion == "VIVIENDA"
        assert r.superficie == 60.0


class TestDocumento:
    def test_create(self):
        d = Documento(url="https://example.com", descripcion="Croquis")
        assert d.url == "https://example.com"
        assert d.descripcion == "Croquis"


class TestConstruction:
    def test_create_base(self):
        c = Construction(id="C1", condition="functional")
        assert c.id == "C1"
        assert c.condition == "functional"
        assert c.geometria is None

    def test_create_building(self):
        b = Building(
            id="B1",
            uso_actual="residential",
            num_unidades=1,
            num_plantas_sup=3,
            area_oficial=150.0,
        )
        assert b.id == "B1"
        assert b.uso_actual == "residential"
        assert b.num_unidades == 1
        assert b.building_parts == []

    def test_create_building_with_parts(self):
        part = BuildingPart(id="BP1", num_plantas_sup=2)
        building = Building(id="B1", building_parts=[part])
        assert len(building.building_parts) == 1
        assert building.building_parts[0].num_plantas_sup == 2

    def test_create_building_part(self):
        bp = BuildingPart(id="BP1", num_plantas_sup=2, num_plantas_inf=1, altura_inf=3.0)
        assert bp.num_plantas_sup == 2
        assert bp.num_plantas_inf == 1
        assert bp.altura_inf == 3.0

    def test_create_other_construction(self):
        oc = OtherConstruction(id="OC1", naturaleza="valla")
        assert oc.naturaleza == "valla"


class TestValorUrbano:
    def test_create(self):
        v = ValorUrbano(
            tipologia="Residencial",
            superficie=150.0,
            val_suelo=1000.0,
            val_construccion=2000.0,
            val_catastral=3000.0,
            val_tipo_m2=20.0,
        )
        assert v.tipologia == "Residencial"
        assert v.val_tipo_m2 == 20.0

    def test_defaults_none(self):
        v = ValorUrbano()
        assert v.tipologia is None
        assert v.val_suelo is None
        assert v.val_tipo_m2 is None


class TestValorRustico:
    def test_create(self):
        v = ValorRustico(
            region="R001",
            nombre_region="TIERRAS DE LABOR",
            valor_m2_tierras_arables_secano=0.5,
        )
        assert v.region == "R001"
        assert v.valor_m2_tierras_arables_secano == 0.5

    def test_defaults_zero(self):
        v = ValorRustico(region="R001", nombre_region="TEST")
        assert v.valor_m2_huertos == 0.0
        assert v.valor_m2_olivares_secano == 0.0


class TestParcelaUrbana:
    def test_create(self):
        m = Municipio(municipio="MADRID", provincia="MADRID")
        c = Calle(municipio=m, tipo_via="CL", calle="ALCALA")
        p = ParcelaUrbana(calle=c, numero=10, antiguedad=1990, uso="Residencial", valor_m2=15.0)
        assert p.numero == 10
        assert p.calle.calle == "ALCALA"


class TestParcelaRustica:
    def test_create(self):
        p = ParcelaRustica(poligono=26, parcela=58, nombre_paraje="LAS CORRALERAS", valor_m2=0.5)
        assert p.poligono == 26
        assert p.nombre_paraje == "LAS CORRALERAS"


class TestParcelaCatastral:
    def _make_urbana(self):
        m = Municipio(municipio="MADRID", provincia="MADRID")
        c = Calle(municipio=m, tipo_via="CL", calle="CHARCA VERDE")
        geo = Geometria(
            sistema_referencia="EPSG:4326",
            coordenadas=[(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)],
            tipo="Polygon",
        )
        return ParcelaCatastral(
            referencia_catastral="3182116VK4738A",
            municipio=m,
            tipo="Urbano",
            completo=True,
            superficie_plana=179.0,
            superficie_construida=180.0,
            datos_urbanos=ParcelaUrbana(calle=c, numero=16, antiguedad=1940, uso="Residencial", valor_m2=15.0),
            datos_rusticos=None,
            regiones=None,
            construcciones=None,
            geometria=geo,
            documentacion=None,
            valor_urbano=None,
            valor_rustico=None,
        )

    def test_create_urbana(self):
        p = self._make_urbana()
        assert p.referencia_catastral == "3182116VK4738A"
        assert p.tipo == "Urbano"
        assert p.datos_urbanos is not None
        assert p.datos_rusticos is None

    def test_perimetro_with_geometry(self):
        p = self._make_urbana()
        assert p.perimetro == 4.0

    def test_perimetro_without_geometry_returns_0(self):
        m = Municipio(municipio="MADRID", provincia="MADRID")
        p = ParcelaCatastral(
            referencia_catastral="RC1",
            municipio=m,
            tipo="Urbano",
            completo=False,
            superficie_plana=0.0,
            superficie_construida=0.0,
            datos_urbanos=None,
            datos_rusticos=None,
            regiones=None,
            construcciones=None,
            geometria=None,
            documentacion=None,
            valor_urbano=None,
            valor_rustico=None,
        )
        assert p.perimetro == 0.0

    def test_completo(self):
        p = self._make_urbana()
        assert p.completo is True
