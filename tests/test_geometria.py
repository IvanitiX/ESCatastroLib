from escatastrolib.parsers.common.dtos_geometria import GeometriaDTO, PuntoDTO


class TestPuntoDTO:
    def test_create(self):
        p = PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[1.0, 2.0])
        assert p.coordenadas == [1.0, 2.0]
        assert p.dimensiones == 2
        assert p.sr == "EPSG:4326"

    def test_create_ints(self):
        p = PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[1, 2])
        assert p.coordenadas == [1, 2]


class TestGeometriaDTO:
    def test_create(self):
        geo = GeometriaDTO(
            sr="EPSG:4326",
            tipo="Point",
            puntos=[PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[0.0, 0.0])],
        )
        assert geo.sr == "EPSG:4326"
        assert geo.tipo == "Point"
        assert len(geo.puntos) == 1

    def test_to_shapely_point(self):
        geo = GeometriaDTO(
            sr="EPSG:4326",
            tipo="Point",
            puntos=[PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[1.0, 2.0])],
        )
        shapely = geo.to_shapely()
        assert shapely is not None
        assert shapely.geom_type == "Point"
        assert shapely.x == 1.0
        assert shapely.y == 2.0

    def test_to_shapely_polygon(self):
        geo = GeometriaDTO(
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
        shapely = geo.to_shapely()
        assert shapely is not None
        assert shapely.geom_type == "Polygon"
        assert shapely.is_valid
        assert shapely.area == 1.0

    def test_to_shapely_empty_points_returns_none(self):
        geo = GeometriaDTO(
            sr="EPSG:4326",
            tipo="Point",
            puntos=[],
        )
        assert geo.to_shapely() is None

    def test_to_shapely_unknown_tipo_returns_none(self):
        geo = GeometriaDTO(
            sr="EPSG:4326",
            tipo="LineString",
            puntos=[
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[0.0, 0.0]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[1.0, 1.0]),
            ],
        )
        assert geo.to_shapely() is None

    def test_to_shapely_polygon_centroid(self):
        geo = GeometriaDTO(
            sr="EPSG:4326",
            tipo="Polygon",
            puntos=[
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[0.0, 0.0]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[2.0, 0.0]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[2.0, 2.0]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[0.0, 2.0]),
                PuntoDTO(sr="EPSG:4326", dimensiones=2, coordenadas=[0.0, 0.0]),
            ],
        )
        shapely = geo.to_shapely()
        assert shapely.centroid.x == 1.0
        assert shapely.centroid.y == 1.0
