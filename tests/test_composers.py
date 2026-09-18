from escatastrolib.parsers.common.dtos_geometria import PuntoDTO, GeometriaDTO
from escatastrolib.parsers.CatastroES.Callejero.dto import (
    MunicipioDTO,
    ProvinciaDTO,
    RegionCatastralDTO,
    ParcelaCatastralDTO,
)
from escatastrolib.parsers.CatastroES.INSPIREParcels.dto import INSPIREParcelDTO
from escatastrolib.parsers.CatastroES.INSPIREBuildings.dto import (
    BuildingDTO,
    BuildingPartDTO,
    OtherConstructionDTO,
)
from escatastrolib.parsers.CatastroES.Croquis.dto import CroquisDTO
from escatastrolib.parsers.CatastroES.MapaValoresUrbanos.dto import ValorUrbanoDTO
from escatastrolib.parsers.CatastroES.MapaValoresRusticos.dto import ValoresRusticosDTO

from escatastrolib.composers.mappers.GeometriaMapper import GeometriaMapper
from escatastrolib.composers.mappers.MunicipioMapper import MunicipioMapper
from escatastrolib.composers.mappers.RegionCatastralMapper import RegionCatastralMapper
from escatastrolib.composers.mappers.ConstructionMapper import ConstructionMapper
from escatastrolib.composers.mappers.DocumentoMapper import DocumentoMapper
from escatastrolib.composers.mappers.ParcelaUrbanaMapper import ParcelaUrbanaMapper
from escatastrolib.composers.mappers.ParcelaRusticaMapper import ParcelaRusticaMapper
from escatastrolib.composers.mappers.ValorUrbanoMapper import ValorUrbanoMapper
from escatastrolib.composers.mappers.ValorRusticoMapper import ValorRusticoMapper
from escatastrolib.composers.ParcelaCatastral import ParcelaCatastralComposer

from escatastrolib.models.Construction import Building, BuildingPart, OtherConstruction


def _make_municipio_dto():
    return MunicipioDTO(nombreMunicipio="MADRID")


def _make_provincia_dto():
    return ProvinciaDTO(codigoProvincia=28, nombreProvincia="MADRID")


def _make_geometria_dto_punto():
    return GeometriaDTO(
        sr="EPSG:4326",
        tipo="Point",
        puntos=[PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[40.0, -3.0])],
    )


def _make_geometria_dto_poligono():
    return GeometriaDTO(
        sr="EPSG:4326",
        tipo="Polygon",
        puntos=[
            PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[0.0, 0.0]),
            PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[1.0, 0.0]),
            PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[1.0, 1.0]),
            PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[0.0, 1.0]),
            PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[0.0, 0.0]),
        ],
    )


def _make_parcela_dto_urbana():
    return ParcelaCatastralDTO(
        referenciaCatastral="3182116VK4738A",
        municipio=_make_municipio_dto(),
        provincia=_make_provincia_dto(),
        tipo="Urbano",
        calle="CL CHARCA VERDE",
        numero="16",
        escalera="T",
        planta="OD",
        puerta="OS",
        antiguedad="1940",
        superficie_economica=180.0,
        uso="Residencial",
        parcela=None,
        poligono=None,
        nombre_paraje=None,
        regiones=None,
        superficie_finca=179.0,
        superficie_solar=179.0,
    )


def _make_parcela_dto_rustica():
    return ParcelaCatastralDTO(
        referenciaCatastral="13033A02600058",
        municipio=MunicipioDTO(nombreMunicipio="CASTELLAR DE SANTIAGO"),
        provincia=ProvinciaDTO(codigoProvincia=13, nombreProvincia="CIUDAD REAL"),
        tipo="Rústico",
        calle=None,
        numero=None,
        escalera=None,
        planta=None,
        puerta=None,
        antiguedad=None,
        superficie_economica=0.0,
        uso="Agrario",
        parcela=58,
        poligono=26,
        nombre_paraje="LAS CORRALERAS",
        regiones=None,
    )


class TestGeometriaMapper:
    def test_map_point(self):
        dto = _make_geometria_dto_punto()
        geo = GeometriaMapper.map(dto)
        assert geo.tipo == "Point"
        assert geo.coordenadas == [(40.0, -3.0)]
        assert geo.sistema_referencia == "EPSG:4326"

    def test_map_polygon(self):
        dto = _make_geometria_dto_poligono()
        geo = GeometriaMapper.map(dto)
        assert geo.tipo == "Polygon"
        assert len(geo.coordenadas) == 5


class TestMunicipioMapper:
    def test_map(self):
        mun = _make_municipio_dto()
        prov = _make_provincia_dto()
        m = MunicipioMapper.map(mun, prov)
        assert m.municipio == "MADRID"
        assert m.provincia == "MADRID"


class TestRegionCatastralMapper:
    def test_map_basic(self):
        dto = RegionCatastralDTO(
            descripcion="VIVIENDA",
            superficie=60.0,
            escalera=None,
            planta=None,
            puerta=None,
        )
        r = RegionCatastralMapper.map(dto)
        assert r.descripcion == "VIVIENDA"
        assert r.superficie == 60.0

    def test_map_with_location(self):
        dto = RegionCatastralDTO(
            descripcion="VIVIENDA",
            superficie=60.0,
            escalera="T",
            planta="01",
            puerta="OS",
        )
        r = RegionCatastralMapper.map(dto)
        assert "Esc.T" in r.descripcion
        assert "Pl.01" in r.descripcion
        assert "Pu.OS" in r.descripcion

    def test_map_partial_location(self):
        dto = RegionCatastralDTO(
            descripcion="VIVIENDA",
            superficie=60.0,
            escalera=None,
            planta="02",
            puerta=None,
        )
        r = RegionCatastralMapper.map(dto)
        assert r.descripcion == "VIVIENDA - Pl.02"


class TestConstructionMapper:
    def test_map_building(self):
        geo_dto = _make_geometria_dto_poligono()
        dto = BuildingDTO(
            id="ES.SDGC.BU.3182116VK4738A",
            geometry=geo_dto,
            condition_of_construction="functional",
            current_use="residential",
            number_of_building_units=1,
            number_of_dwellings=1,
            number_of_floors_above_ground=3,
            official_area_value=150.0,
        )
        b = ConstructionMapper.map(dto)
        assert isinstance(b, Building)
        assert b.id == "ES.SDGC.BU.3182116VK4738A"
        assert b.uso_actual == "residential"
        assert b.num_plantas_sup == 3
        assert b.area_oficial == 150.0
        assert b.geometria is not None

    def test_map_building_part(self):
        dto = BuildingPartDTO(
            id="BP.1",
            condition_of_construction="functional",
            number_of_floors_above_ground=2,
            number_of_floors_below_ground=1,
            height_below_ground_m=3.0,
        )
        bp = ConstructionMapper.map(dto)
        assert isinstance(bp, BuildingPart)
        assert bp.num_plantas_sup == 2
        assert bp.num_plantas_inf == 1
        assert bp.altura_inf == 3.0

    def test_map_other_construction(self):
        dto = OtherConstructionDTO(
            id="OC.1",
            condition_of_construction="functional",
            construction_nature="valla",
        )
        oc = ConstructionMapper.map(dto)
        assert isinstance(oc, OtherConstruction)
        assert oc.naturaleza == "valla"

    def test_map_unknown_raises(self):
        class FakeDTO:
            id = "X"
            geometry = None
            condition_of_construction = None

        import pytest

        with pytest.raises(ValueError, match="desconocido"):
            ConstructionMapper.map(FakeDTO())


class TestDocumentoMapper:
    def test_map(self):
        dto = CroquisDTO(url="https://example.com/croquis")
        d = DocumentoMapper.map(dto)
        assert d.url == "https://example.com/croquis"
        assert d.descripcion == "Croquis catastral"


class TestParcelaUrbanaMapper:
    def test_map(self):
        dto = _make_parcela_dto_urbana()
        m = MunicipioMapper.map(dto.municipio, dto.provincia)
        p = ParcelaUrbanaMapper.map(dto, m, valor_m2=15.0)
        assert p.calle.tipo_via == "CL"
        assert p.calle.calle == "CHARCA VERDE"
        assert p.numero == 16
        assert p.antiguedad == 1940
        assert p.uso == "Residencial"
        assert p.valor_m2 == 15.0

    def test_map_no_calle(self):
        dto = _make_parcela_dto_rustica()
        dto.calle = None
        m = MunicipioMapper.map(dto.municipio, dto.provincia)
        p = ParcelaUrbanaMapper.map(dto, m)
        assert p.calle.tipo_via == ""
        assert p.calle.calle == ""


class TestParcelaRusticaMapper:
    def test_map(self):
        dto = _make_parcela_dto_rustica()
        p = ParcelaRusticaMapper.map(dto, valor_m2=0.5)
        assert p.poligono == 26
        assert p.parcela == 58
        assert p.nombre_paraje == "LAS CORRALERAS"
        assert p.valor_m2 == 0.5


class TestValorUrbanoMapper:
    def test_map(self):
        dto = ValorUrbanoDTO(
            tipologia="Residencial",
            superficie=150.0,
            val_suelo=1000.0,
            val_construccion_pt=2000.0,
            val_catastral=3000.0,
            val_tipo_m2=20.0,
        )
        v = ValorUrbanoMapper.map(dto)
        assert v.tipologia == "Residencial"
        assert v.superficie == 150.0
        assert v.val_suelo == 1000.0
        assert v.val_construccion == 2000.0
        assert v.val_catastral == 3000.0
        assert v.val_tipo_m2 == 20.0


class TestValorRusticoMapper:
    def test_map(self):
        dto = ValoresRusticosDTO(
            region="R001",
            nombre_region="TIERRAS DE LABOR",
            valor_m2_tierras_arables_secano=0.5,
            valor_m2_tierras_arables_regadio=0.8,
            valor_m2_huertos=1.0,
            valor_m2_cultivos_bajo_plastico=1.2,
            valor_m2_arrozales=0.3,
            valor_m2_citricos=0.9,
            valor_m2_frutales_carnosos_secano=0.7,
            valor_m2_frutos_secos_secano=0.6,
            valor_m2_cultivos_subtropicales_tropicales=1.1,
            valor_m2_plataneras=0.4,
            valor_m2_frutales_carnosos_regadio=0.85,
            valor_m2_frutos_secos_regadio=0.65,
            valor_m2_vinedos_secano=0.55,
            valor_m2_vinedos_regadio=0.75,
            valor_m2_olivares_secano=0.45,
            valor_m2_olivares_regadio=0.95,
            valor_m2_prados=0.35,
            valor_m2_pastizales=0.25,
        )
        v = ValorRusticoMapper.map(dto)
        assert v.region == "R001"
        assert v.valor_m2_tierras_arables_secano == 0.5
        assert v.valor_m2_olivares_regadio == 0.95


class TestParcelaCatastralComposer:
    def test_compose_minimal(self):
        dto = _make_parcela_dto_urbana()
        composer = ParcelaCatastralComposer()
        p = composer.compose(dto, completo=True)
        assert p.referencia_catastral == "3182116VK4738A"
        assert p.tipo == "Urbano"
        assert p.completo is True
        assert p.municipio.municipio == "MADRID"
        assert p.municipio.provincia == "MADRID"
        assert p.datos_urbanos is not None
        assert p.datos_urbanos.calle.tipo_via == "CL"
        assert p.datos_urbanos.calle.calle == "CHARCA VERDE"
        assert p.geometria is None
        assert p.regiones is None
        assert p.construcciones is None
        assert p.documentacion is None

    def test_compose_with_geometries(self):
        dto = _make_parcela_dto_urbana()
        geom_dto = _make_geometria_dto_poligono()
        insp = INSPIREParcelDTO(
            geometria=geom_dto,
            centroide=GeometriaDTO(sr="EPSG:4326", tipo="Point", puntos=[]),
            area=1.0,
        )

        composer = ParcelaCatastralComposer(include_geometries=True)
        p = composer.compose(dto, geometria_dto=insp)
        assert p.geometria is not None
        assert p.geometria.tipo == "Polygon"
        assert p.superficie_plana == 1.0

    def test_compose_with_regions(self):
        dto = _make_parcela_dto_urbana()
        dto.regiones = [
            RegionCatastralDTO("VIVIENDA", 60.0, None, "01", None),
            RegionCatastralDTO("VIVIENDA", 60.0, None, "02", None),
        ]
        composer = ParcelaCatastralComposer(include_regions=True)
        p = composer.compose(dto)
        assert p.regiones is not None
        assert len(p.regiones) == 2
        assert p.regiones[0].superficie == 60.0

    def test_compose_with_constructions(self):
        dto = _make_parcela_dto_urbana()
        building = BuildingDTO(
            id="B1",
            geometry=None,
            condition_of_construction="functional",
            current_use="residential",
        )
        composer = ParcelaCatastralComposer(include_constructions=True)
        p = composer.compose(dto, construcciones_dtos=[building])
        assert p.construcciones is not None
        assert len(p.construcciones) == 1
        assert p.construcciones[0].id == "B1"

    def test_compose_with_documentation(self):
        dto = _make_parcela_dto_urbana()
        croquis = CroquisDTO(url="https://example.com/croquis")
        composer = ParcelaCatastralComposer(include_documentation=True)
        p = composer.compose(dto, croquis_dtos=[croquis])
        assert p.documentacion is not None
        assert len(p.documentacion) == 1
        assert p.documentacion[0].url == "https://example.com/croquis"

    def test_compose_with_values_urbanos(self):
        dto = _make_parcela_dto_urbana()
        valor = ValorUrbanoDTO(
            tipologia="Residencial",
            superficie=150.0,
            val_tipo_m2=20.0,
        )
        composer = ParcelaCatastralComposer(include_values=True)
        p = composer.compose(dto, valor_urbano_dto=valor)
        assert p.valor_urbano is not None
        assert p.valor_urbano.val_tipo_m2 == 20.0
        assert p.datos_urbanos.valor_m2 == 20.0

    def test_compose_rustica(self):
        dto = _make_parcela_dto_rustica()
        composer = ParcelaCatastralComposer()
        p = composer.compose(dto)
        assert p.tipo == "Rústico"
        assert p.datos_rusticos is not None
        assert p.datos_rusticos.poligono == 26
        assert p.datos_rusticos.parcela == 58
        assert p.datos_urbanos is None

    def test_compose_all_flags(self):
        dto = _make_parcela_dto_urbana()
        dto.regiones = [
            RegionCatastralDTO("VIVIENDA", 60.0, None, "01", None),
        ]

        geom_dto = _make_geometria_dto_poligono()
        insp = INSPIREParcelDTO(
            geometria=geom_dto,
            centroide=GeometriaDTO(sr="EPSG:4326", tipo="Point", puntos=[]),
            area=1.0,
        )

        building = BuildingDTO(id="B1", geometry=None, condition_of_construction="functional")
        croquis = CroquisDTO(url="https://example.com/croquis")
        valor = ValorUrbanoDTO(tipologia="Residencial", val_tipo_m2=20.0)

        composer = ParcelaCatastralComposer(
            include_geometries=True,
            include_values=True,
            include_regions=True,
            include_constructions=True,
            include_documentation=True,
        )
        p = composer.compose(
            dto,
            geometria_dto=insp,
            croquis_dtos=[croquis],
            valor_urbano_dto=valor,
            construcciones_dtos=[building],
        )
        assert p.geometria is not None
        assert p.regiones is not None
        assert p.construcciones is not None
        assert p.documentacion is not None
        assert p.valor_urbano is not None
