import pytest
from escatastrolib.clients.CatastroES import CatastroESClient, CatastroESProviders
from escatastrolib.utils.Mappings import SISTEMAS_REFERENCIA


class TestCatastroESClientConstructor:
    def test_defaults(self):
        client = CatastroESClient()
        assert client.proyeccion == "EPSG:4326"
        assert client.include_geometries is False
        assert client.include_values is False
        assert client.include_regions is False
        assert client.include_constructions is False
        assert client.include_documentation is False
        assert client.force_complete is False

    def test_custom_flags(self):
        client = CatastroESClient(
            proyeccion="EPSG:25830",
            include_geometries=True,
            include_values=True,
            include_regions=True,
            include_constructions=True,
            include_documentation=True,
            force_complete=True,
            anio_valores=2023,
        )
        assert client.proyeccion == "EPSG:25830"
        assert client.include_geometries is True
        assert client.include_values is True
        assert client.include_regions is True
        assert client.include_constructions is True
        assert client.include_documentation is True
        assert client.force_complete is True
        assert client.anio_valores == 2023

    def test_invalid_projection_raises(self):
        with pytest.raises(ValueError, match="Proyección no soportada"):
            CatastroESClient(proyeccion="EPSG:99999")

    def test_valid_projections(self):
        for sr in SISTEMAS_REFERENCIA:
            client = CatastroESClient(proyeccion=sr)
            assert client.proyeccion == sr

    def test_providers_exposed(self):
        client = CatastroESClient()
        assert isinstance(client.providers, CatastroESProviders)
        assert client.providers.callejero is not None
        assert client.providers.cartociudad is not None
        assert client.providers.coordenadas is not None
        assert client.providers.inspire_parcelas is not None
        assert client.providers.inspire_buildings is not None
        assert client.providers.valores_urbanos is not None
        assert client.providers.valores_rusticos is not None
        assert client.providers.croquis is not None


class TestCatastroESClientCallejero:
    def test_obtener_provincias(self):
        client = CatastroESClient()
        provincias = client.obtener_provincias()
        assert len(provincias) > 0
        assert provincias[0].codigoProvincia is not None
        assert provincias[0].nombreProvincia is not None

    def test_buscar_municipios(self):
        client = CatastroESClient()
        municipios = client.buscar_municipios("MADRID", "madr")
        assert len(municipios) > 0

    def test_buscar_calles(self):
        client = CatastroESClient()
        calles = client.buscar_calles("MADRID", "MADRID", nombre_calle="Alcala")
        assert len(calles) > 0
        assert calles[0].nombreCatastral is not None


class TestCatastroESClientGeocoding:
    def test_geocodificar(self):
        client = CatastroESClient()
        resultado = client.geocodificar("Calle Alcala 1", "Madrid")
        assert resultado is not None
        assert resultado.latitud is not None
        assert resultado.longitud is not None


class TestCatastroESClientCoordenadas:
    def test_coordenadas_por_rc(self):
        client = CatastroESClient()
        coords = client.coordenadas_por_rc("3182116VK4738A")
        assert len(coords) > 0
        assert coords[0].x is not None
        assert coords[0].y is not None


class TestCatastroESClientParcela:
    def test_parcela_por_rc(self):
        client = CatastroESClient()
        parcelas = client.obtener_parcela_por_rc("3182116VK4738A")
        assert len(parcelas) > 0
        p = parcelas[0]
        assert p.referencia_catastral.startswith("3182116VK4738A")
        assert p.tipo is not None
        assert p.municipio is not None

    def test_parcela_por_rc_rustica(self):
        client = CatastroESClient()
        parcelas = client.obtener_parcela_por_rc("13033A02600058")
        assert len(parcelas) > 0
        p = parcelas[0]
        assert "stico" in p.tipo.lower()


class TestCatastroESClientOpciones:
    def test_con_geometrias(self):
        client = CatastroESClient(include_geometries=True)
        parcelas = client.obtener_parcela_por_rc("3182116VK4738A")
        assert len(parcelas) > 0
        p = parcelas[0]
        assert p.geometria is not None
        assert len(p.geometria.coordenadas) > 0

    def test_con_documentacion(self):
        client = CatastroESClient(include_documentation=True)
        parcelas = client.obtener_parcela_por_rc("3182116VK4738A")
        assert len(parcelas) > 0

    def test_con_valores_urbanos(self):
        client = CatastroESClient(include_values=True)
        parcelas = client.obtener_parcela_por_rc("3182116VK4738A")
        assert len(parcelas) > 0

    def test_force_complete(self):
        client = CatastroESClient(force_complete=True)
        parcelas = client.obtener_parcela_por_rc("3182116VK4738A")
        assert len(parcelas) >= 1

    def test_proyeccion_utm30n(self):
        client = CatastroESClient(proyeccion="EPSG:25830")
        parcelas = client.obtener_parcela_por_rc("3182116VK4738A")
        assert len(parcelas) > 0


class TestCalcularBbox:
    def test_bbox_static(self):
        from escatastrolib.parsers.common.dtos_geometria import PuntoDTO, GeometriaDTO

        geo = GeometriaDTO(
            sr="EPSG:4326",
            tipo="Polygon",
            puntos=[
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[-3.7, 40.4]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[-3.6, 40.4]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[-3.6, 40.5]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[-3.7, 40.5]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[-3.7, 40.4]),
            ],
        )
        bbox = CatastroESClient._calcular_bbox_3857(geo, "EPSG:4326")
        parts = bbox.split(",")
        assert len(parts) == 4
        xs = [float(p) for p in parts[:2]]
        ys = [float(p) for p in parts[2:]]
        assert all(isinstance(v, float) for v in xs + ys)
