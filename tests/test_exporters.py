import json
import os
import tempfile

import pytest

from escatastrolib.models.Callejero import Calle, Municipio
from escatastrolib.models.Construction import Building, BuildingPart
from escatastrolib.models.GeometriaCatastral import Geometria
from escatastrolib.models.ParcelaCatastral import (
    ParcelaCatastral,
    ParcelaRustica,
    ParcelaUrbana,
)
from escatastrolib.models.RegionCatastral import RegionCatastral


# ── Fixtures ────────────────────────────────────────────────


@pytest.fixture
def municipio():
    return Municipio(municipio="Madrid", provincia="Madrid")


@pytest.fixture
def geometria():
    return Geometria(
        sistema_referencia="EPSG:4258",
        coordenadas=[
            (40.4168, -3.7038),
            (40.4168, -3.7030),
            (40.4175, -3.7030),
            (40.4175, -3.7038),
            (40.4168, -3.7038),
        ],
        tipo="Polygon",
    )


@pytest.fixture
def parcela_urbana(municipio, geometria):
    calle = Calle(municipio=municipio, tipo_via="Calle", calle="Mayor")
    return ParcelaCatastral(
        referencia_catastral="28079A00100001",
        municipio=municipio,
        tipo="Urbano",
        completo=True,
        superficie_plana=500.0,
        superficie_construida=350.0,
        datos_urbanos=ParcelaUrbana(
            calle=calle, numero=1, antiguedad=50, uso="Vivienda", valor_m2=1200.0
        ),
        datos_rusticos=None,
        regiones=[RegionCatastral(descripcion="Esc. A", superficie=150.0)],
        construcciones=None,
        geometria=geometria,
        documentacion=None,
        valor_urbano=None,
        valor_rustico=None,
    )


@pytest.fixture
def parcela_rustica(municipio, geometria):
    return ParcelaCatastral(
        referencia_catastral="28079A00200002",
        municipio=municipio,
        tipo="Rustico",
        completo=True,
        superficie_plana=12000.0,
        superficie_construida=0.0,
        datos_urbanos=None,
        datos_rusticos=ParcelaRustica(
            poligono=26, parcela=58, nombre_paraje="Las Corraleras", valor_m2=0.5
        ),
        regiones=None,
        construcciones=None,
        geometria=geometria,
        documentacion=None,
        valor_urbano=None,
        valor_rustico=None,
    )


@pytest.fixture
def parcela_con_construcciones(municipio, geometria):
    calle = Calle(municipio=municipio, tipo_via="Av", calle="Gran Via")
    part = BuildingPart(id="BP1", num_plantas_sup=2, num_plantas_inf=1)
    building = Building(
        id="B1",
        geometria=None,
        condition="Functional",
        uso_actual="Residencial",
        num_unidades=4,
        num_viviendas=4,
        num_plantas_sup=3,
        area_oficial=400.0,
        building_parts=[part],
    )
    return ParcelaCatastral(
        referencia_catastral="28079A00300003",
        municipio=municipio,
        tipo="Urbano",
        completo=True,
        superficie_plana=600.0,
        superficie_construida=400.0,
        datos_urbanos=ParcelaUrbana(
            calle=calle, numero=5, antiguedad=2005, uso="Residencial", valor_m2=1800.0
        ),
        datos_rusticos=None,
        regiones=None,
        construcciones=[building],
        geometria=geometria,
        documentacion=None,
        valor_urbano=None,
        valor_rustico=None,
    )


@pytest.fixture
def parcela_sin_geometria(municipio):
    return ParcelaCatastral(
        referencia_catastral="28079A00400004",
        municipio=municipio,
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


@pytest.fixture
def parcelas(parcela_urbana, parcela_rustica):
    return [parcela_urbana, parcela_rustica]


# ── JSON ────────────────────────────────────────────────────


class TestToJson:
    def test_returns_string(self, parcelas):
        from escatastrolib.exporters import to_json

        result = to_json(parcelas)
        assert isinstance(result, str)

    def test_valid_json(self, parcelas):
        from escatastrolib.exporters import to_json

        data = json.loads(to_json(parcelas))
        assert isinstance(data, list)
        assert len(data) == 2

    def test_contains_rc(self, parcelas):
        from escatastrolib.exporters import to_json

        data = json.loads(to_json(parcelas))
        rcs = [p["referencia_catastral"] for p in data]
        assert "28079A00100001" in rcs
        assert "28079A00200002" in rcs

    def test_geometry_included_by_default(self, parcelas):
        from escatastrolib.exporters import to_json

        data = json.loads(to_json(parcelas))
        assert data[0]["geometria"] is not None
        assert data[0]["geometria"]["tipo"] == "Polygon"

    def test_geometry_excluded(self, parcelas):
        from escatastrolib.exporters import to_json

        data = json.loads(to_json(parcelas, include_geometry=False))
        assert data[0]["geometria"] is None

    def test_constructions_included(self, parcela_con_construcciones):
        from escatastrolib.exporters import to_json

        data = json.loads(to_json([parcela_con_construcciones]))
        assert data[0]["construcciones"] is not None
        assert len(data[0]["construcciones"]) == 1

    def test_constructions_excluded(self, parcela_con_construcciones):
        from escatastrolib.exporters import to_json

        data = json.loads(to_json([parcela_con_construcciones], include_constructions=False))
        assert data[0]["construcciones"] is None

    def test_export_to_file(self, parcelas):
        from escatastrolib.exporters import to_json

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.json")
            result = to_json(parcelas, path)
            assert os.path.exists(path)
            assert str(result) == path
            data = json.loads(open(path).read())
            assert len(data) == 2

    def test_none_geometry_returns_empty_string(self, parcela_sin_geometria):
        from escatastrolib.exporters import to_json

        data = json.loads(to_json([parcela_sin_geometria]))
        assert data[0]["geometria"] is None

    def test_indent(self, parcelas):
        from escatastrolib.exporters import to_json

        compact = to_json(parcelas, indent=None)
        pretty = to_json(parcelas, indent=4)
        assert len(pretty) > len(compact)


# ── CSV ─────────────────────────────────────────────────────


class TestToCsv:
    def test_returns_string(self, parcelas):
        from escatastrolib.exporters import to_csv

        result = to_csv(parcelas)
        assert isinstance(result, str)

    def test_has_header(self, parcelas):
        from escatastrolib.exporters import to_csv

        lines = to_csv(parcelas).strip().split("\n")
        header = lines[0]
        assert "referencia_catastral" in header
        assert "municipio" in header

    def test_row_count(self, parcelas):
        from escatastrolib.exporters import to_csv

        lines = to_csv(parcelas).strip().split("\n")
        assert len(lines) == 3  # header + 2 rows

    def test_rc_values(self, parcelas):
        from escatastrolib.exporters import to_csv

        csv_str = to_csv(parcelas)
        assert "28079A00100001" in csv_str
        assert "28079A00200002" in csv_str

    def test_wkt_geometry_included(self, parcelas):
        from escatastrolib.exporters import to_csv

        csv_str = to_csv(parcelas)
        assert "POLYGON" in csv_str

    def test_wkt_geometry_excluded(self, parcelas):
        from escatastrolib.exporters import to_csv

        csv_str = to_csv(parcelas, include_geometry=False)
        assert "POLYGON" not in csv_str

    def test_export_to_file(self, parcelas):
        from escatastrolib.exporters import to_csv

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.csv")
            result = to_csv(parcelas, path)
            assert os.path.exists(path)
            assert str(result) == path

    def test_custom_delimiter(self, parcelas):
        from escatastrolib.exporters import to_csv

        csv_str = to_csv(parcelas, delimiter=";")
        assert ";" in csv_str

    def test_urbana_fields(self, parcela_urbana):
        from escatastrolib.exporters import to_csv

        csv_str = to_csv([parcela_urbana])
        assert "Mayor" in csv_str
        assert "Vivienda" in csv_str

    def test_rustica_fields(self, parcela_rustica):
        from escatastrolib.exporters import to_csv

        csv_str = to_csv([parcela_rustica])
        assert "Las Corraleras" in csv_str

    def test_empty_list(self):
        from escatastrolib.exporters import to_csv

        result = to_csv([])
        assert result == ""


# ── GeoJSON ─────────────────────────────────────────────────


class TestToGeojson:
    def test_returns_dict(self, parcelas):
        from escatastrolib.exporters import to_geojson

        result = to_geojson(parcelas)
        assert isinstance(result, dict)

    def test_feature_collection(self, parcelas):
        from escatastrolib.exporters import to_geojson

        result = to_geojson(parcelas)
        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == 2

    def test_feature_has_geometry(self, parcelas):
        from escatastrolib.exporters import to_geojson

        result = to_geojson(parcelas)
        for feature in result["features"]:
            assert feature["type"] == "Feature"
            assert feature["geometry"] is not None
            assert feature["geometry"]["type"] == "Polygon"

    def test_feature_has_properties(self, parcelas):
        from escatastrolib.exporters import to_geojson

        result = to_geojson(parcelas)
        props = result["features"][0]["properties"]
        assert "referencia_catastral" in props
        assert "municipio" in props
        assert "superficie_plana" in props

    def test_constructions_in_properties(self, parcela_con_construcciones):
        from escatastrolib.exporters import to_geojson

        result = to_geojson([parcela_con_construcciones])
        props = result["features"][0]["properties"]
        assert "construcciones" in props
        assert len(props["construcciones"]) == 1

    def test_constructions_excluded(self, parcela_con_construcciones):
        from escatastrolib.exporters import to_geojson

        result = to_geojson([parcela_con_construcciones], include_constructions=False)
        props = result["features"][0]["properties"]
        assert "construcciones" not in props

    def test_coordinate_precision(self, parcelas):
        from escatastrolib.exporters import to_geojson

        result = to_geojson(parcelas, coordinate_precision=3)
        coords = result["features"][0]["geometry"]["coordinates"][0]
        for x, y in coords:
            assert len(str(x).split(".")[-1]) <= 3
            assert len(str(y).split(".")[-1]) <= 3

    def test_reprojection(self, parcelas):
        from escatastrolib.exporters import to_geojson

        result = to_geojson(parcelas, target_crs="EPSG:25830")
        assert result["type"] == "FeatureCollection"
        coords = result["features"][0]["geometry"]["coordinates"][0]
        for x, y in coords:
            assert 200000 < x < 700000  # UTM zone 30N easting
            assert 3000000 < y < 5500000  # UTM zone 30N northing

    def test_no_geometry_raises(self, parcela_sin_geometria):
        from escatastrolib.exporters import to_geojson

        with pytest.raises(ValueError, match="no tiene geometría"):
            to_geojson([parcela_sin_geometria])

    def test_export_to_file(self, parcelas):
        from escatastrolib.exporters import to_geojson

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.geojson")
            result = to_geojson(parcelas, path)
            assert os.path.exists(path)
            assert str(result) == path
            data = json.loads(open(path).read())
            assert data["type"] == "FeatureCollection"

    def test_urbana_properties(self, parcela_urbana):
        from escatastrolib.exporters import to_geojson

        result = to_geojson([parcela_urbana])
        props = result["features"][0]["properties"]
        assert props["calle"] == "Mayor"
        assert props["tipo_via"] == "Calle"
        assert props["numero"] == 1
        assert props["uso"] == "Vivienda"

    def test_rustica_properties(self, parcela_rustica):
        from escatastrolib.exporters import to_geojson

        result = to_geojson([parcela_rustica])
        props = result["features"][0]["properties"]
        assert props["poligono"] == 26
        assert props["nombre_paraje"] == "Las Corraleras"


# ── GeoPackage (conditional) ────────────────────────────────


class TestToGeopackage:
    @pytest.fixture(autouse=True)
    def _requires_fudgeo(self):
        pytest.importorskip("fudgeo", reason="fudgeo no instalado")

    def test_export(self, parcelas):
        from escatastrolib.exporters import to_geopackage

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.gpkg")
            result = to_geopackage(parcelas, path)
            assert os.path.exists(path)
            assert str(result) == path
            assert os.path.getsize(path) > 0

    def test_path_none_raises(self, parcelas):
        from escatastrolib.exporters import to_geopackage

        with pytest.raises(ValueError, match="requiere una ruta"):
            to_geopackage(parcelas)

    def test_reprojection(self, parcelas):
        from escatastrolib.exporters import to_geopackage

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.gpkg")
            result = to_geopackage(parcelas, path, target_crs="EPSG:25830")
            assert os.path.exists(path)


# ── Shapefile (conditional) ─────────────────────────────────


class TestToShapefile:
    @pytest.fixture(autouse=True)
    def _requires_pyshp(self):
        pytest.importorskip("shapefile", reason="pyshp no instalado")

    def test_export(self, parcelas):
        from escatastrolib.exporters import to_shapefile

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out")
            result = to_shapefile(parcelas, path)
            assert os.path.exists(path + ".shp")
            assert os.path.exists(path + ".dbf")
            assert str(result) == path

    def test_prj_created(self, parcelas):
        from escatastrolib.exporters import to_shapefile

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out")
            to_shapefile(parcelas, path)
            assert os.path.exists(path + ".prj")

    def test_path_none_raises(self, parcelas):
        from escatastrolib.exporters import to_shapefile

        with pytest.raises(ValueError, match="requiere una ruta"):
            to_shapefile(parcelas)

    def test_reprojection(self, parcelas):
        from escatastrolib.exporters import to_shapefile

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out")
            result = to_shapefile(parcelas, path, target_crs="EPSG:25830")
            assert os.path.exists(path + ".shp")


# ── DataFrame (conditional) ─────────────────────────────────


class TestToDataframe:
    @pytest.fixture(autouse=True)
    def _requires_pandas(self):
        pytest.importorskip("pandas", reason="pandas no instalado")

    def test_returns_dataframe(self, parcelas):
        from escatastrolib.exporters import to_dataframe

        df = to_dataframe(parcelas)
        assert len(df) == 2
        assert "referencia_catastral" in df.columns

    def test_flat_columns(self, parcelas):
        from escatastrolib.exporters import to_dataframe

        df = to_dataframe(parcelas)
        assert "municipio" in df.columns
        assert "provincia" in df.columns
        assert "superficie_plana" in df.columns

    def test_geometry_wkt_column(self, parcelas):
        from escatastrolib.exporters import to_dataframe

        df = to_dataframe(parcelas, include_geometry=True)
        assert "geometria_wkt" in df.columns
        assert df["geometria_wkt"].str.contains("POLYGON").any()

    def test_no_geometry_column(self, parcelas):
        from escatastrolib.exporters import to_dataframe

        df = to_dataframe(parcelas, include_geometry=False)
        assert "geometria_wkt" not in df.columns

    def test_export_csv(self, parcelas):
        from escatastrolib.exporters import to_dataframe

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.csv")
            result = to_dataframe(parcelas, path, format="csv")
            assert os.path.exists(path)
            assert str(result) == path

    def test_export_parquet(self, parcelas):
        from escatastrolib.exporters import to_dataframe

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.parquet")
            result = to_dataframe(parcelas, path, format="parquet")
            assert os.path.exists(path)

    def test_invalid_format_raises(self, parcelas):
        from escatastrolib.exporters import to_dataframe

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "out.xyz")
            with pytest.raises(ValueError, match="Formato no soportado"):
                to_dataframe(parcelas, path, format="xyz")
