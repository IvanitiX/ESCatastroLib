from datetime import datetime
from dataclasses import dataclass

import requests
from pyproj import Transformer

from ..providers.CatastroES.Callejero import CallejeroAPIProvider
from ..providers.CatastroES.CartoCiudad import CartoCiudadProvider
from ..providers.CatastroES.Coordenadas import CoordenadasAPIProvider
from ..providers.CatastroES.Croquis import CroquisAPIProvider
from ..providers.CatastroES.INSPIREBuildings import InspireBuildingsProvider
from ..providers.CatastroES.INSPIREParcelas import InspireParcelasProvider
from ..providers.CatastroES.MapaValoresRusticos import MapaValoresRusticosProvider
from ..providers.CatastroES.MapaValoresUrbanos import MapaValoresUrbanosProvider

from ..parsers.CatastroES.Callejero.parser import (
    CallejeroProvinciaParser,
    CallejeroMunicipioParser,
    CallejeroCalleParser,
    CallejeroParser,
    ParcelaCatastralRCParser,
    ParcelaCatastralPolParParser,
    ParcelaCatastralDirParser,
)
from ..parsers.CatastroES.Callejero.dto import (
    ProvinciaDTO,
    MunicipioDTO,
    CalleDTO,
    ParcelaCatastralDTO,
)
from ..parsers.CatastroES.CartoCiudad.parser import CartoCiudadParser
from ..parsers.CatastroES.CartoCiudad.dto import CartoCiudadDTO
from ..parsers.CatastroES.Coordenadas.parser import (
    RCaCoordenadasParser,
    CoordenadasaRCParser,
)
from ..parsers.CatastroES.Coordenadas.dto import CentroideDTO, RefCatDTO
from ..parsers.CatastroES.Croquis.parser import CroquisParser
from ..parsers.CatastroES.INSPIREBuildings.parser import INSPIREConstructionParser
from ..parsers.CatastroES.INSPIREParcels.parser import INSPIREParcelParser
from ..parsers.CatastroES.MapaValoresUrbanos.parser import ValoresUrbanosParser
from ..parsers.CatastroES.MapaValoresRusticos.parser import ValoresRusticosParser

from ..models.ParcelaCatastral import ParcelaCatastral
from ..composers.ParcelaCatastral import ParcelaCatastralComposer
from ..utils.Mappings import SISTEMAS_REFERENCIA
from .base import BaseCatastroClient


@dataclass
class CatastroESProviders:
    """Contenedor de todos los providers de acceso a APIs del Catastro.

    Agrupa las instancias de los providers HTTP que conectan con los
    diferentes servicios de la Sede Electrónica del Catastro y servicios
    complementarios.

    Attributes:
        callejero: Provider del API de callejero (provincias, municipios, calles, parcelas).
        cartociudad: Provider del geocodificador CartoCiudad.
        coordenadas: Provider del API de coordenadas del Catastro.
        inspire_parcelas: Provider INSPIRE CP para geometrías de parcelas.
        inspire_buildings: Provider INSPIRE BU para construcciones y edificios.
        valores_urbanos: Provider del Mapa de Valores Urbanos (GeoJSON).
        valores_rusticos: Provider del Mapa de Valores Rústicos (WMS).
        croquis: Provider para obtención de croquis catastrales.
    """

    callejero: CallejeroAPIProvider
    cartociudad: CartoCiudadProvider
    coordenadas: CoordenadasAPIProvider
    inspire_parcelas: InspireParcelasProvider
    inspire_buildings: InspireBuildingsProvider
    valores_urbanos: MapaValoresUrbanosProvider
    valores_rusticos: MapaValoresRusticosProvider
    croquis: CroquisAPIProvider


class CatastroESClient(BaseCatastroClient):
    """Cliente principal para consultar el Catastro español.

    Punto de entrada principal de la librería. Orquesta providers, parsers
    y composers para ofrecer una API simplificada de consulta catastral.
    Hereda de ``BaseCatastroClient`` para funcionalidad compartida.

    Ejemplo::

        client = CatastroESClient(include_geometries=True)
        parcelas = client.obtener_parcela_por_rc("12345678901234AA1234F")

    Args:
        proyeccion: Sistema de referencia para coordenadas (default "EPSG:4326").
            Debe ser uno de los soportados en SISTEMAS_REFERENCIA.
        include_geometries: Si True, incluye la geometría INSPIRE de la parcela.
        include_values: Si True, incluye valoración del suelo (urbano o rústico).
        anio_valores: Año de consulta para valores catastrales. Default: año actual.
        include_regions: Si True, incluye las regiones catastrales.
        include_constructions: Si True, incluye construcciones (edificios, partes, etc.).
        include_documentation: Si True, incluye documentos asociados (croquis).
        force_complete: Si True, cuando hay múltiples resultados en una búsqueda
            por polígono/dirección, reconsulta individualmente por RC para
            obtener datos completos.

    Attributes:
        providers: Contenedor de providers HTTP para cada API.
        composer: Composer para ensamblar el modelo ParcelaCatastral.
    """
    def __init__(
        self,
        *,
        proyeccion: str = "EPSG:4326",
        include_geometries: bool = False,
        include_values: bool = False,
        anio_valores: int | None = None,
        include_regions: bool = False,
        include_constructions: bool = False,
        include_documentation: bool = False,
        force_complete: bool = False,
    ) -> None:
        if proyeccion not in SISTEMAS_REFERENCIA:
            raise ValueError(
                f"Proyección no soportada: {proyeccion}. "
                f"Usar una de: {list(SISTEMAS_REFERENCIA.keys())}"
            )

        self.proyeccion = proyeccion
        self.include_values = include_values
        self.include_geometries = include_geometries
        self.include_regions = include_regions
        self.include_constructions = include_constructions
        self.include_documentation = include_documentation
        self.anio_valores = anio_valores or datetime.now().year
        self.force_complete = force_complete

        self.providers = CatastroESProviders(
            callejero=CallejeroAPIProvider(),
            cartociudad=CartoCiudadProvider(),
            coordenadas=CoordenadasAPIProvider(),
            inspire_parcelas=InspireParcelasProvider(),
            inspire_buildings=InspireBuildingsProvider(),
            valores_urbanos=MapaValoresUrbanosProvider(),
            valores_rusticos=MapaValoresRusticosProvider(),
            croquis=CroquisAPIProvider(),
        )
        self.composer = ParcelaCatastralComposer(
            include_geometries=include_geometries,
            include_values=include_values,
            include_regions=include_regions,
            include_constructions=include_constructions,
            include_documentation=include_documentation,
        )

    # ── Callejero ──────────────────────────────────────────

    def obtener_provincias(self) -> list[ProvinciaDTO]:
        """Consulta la lista de provincias españolas del Catastro.

        Returns:
            list[ProvinciaDTO]: Lista de provincias con código y nombre.
        """
        response = self.providers.callejero.consulta_provincias()
        return CallejeroProvinciaParser().parse(response)

    def buscar_municipios(self, provincia: str, municipio: str) -> list[MunicipioDTO]:
        """Busca municipios por provincia y nombre.

        Args:
            provincia: Código de provincia (2 dígitos) o nombre.
            municipio: Nombre del municipio a buscar.

        Returns:
            list[MunicipioDTO]: Lista de municipios que coinciden con la búsqueda.
        """
        response = self.providers.callejero.consulta_municipios(provincia, municipio)
        return CallejeroMunicipioParser().parse(response)

    def buscar_calles(self, provincia: str, municipio: str, tipo_via: str = '', nombre_calle: str = '') -> list[CalleDTO]:
        """Busca calles dentro de un municipio.

        Args:
            provincia: Código de provincia o nombre.
            municipio: Nombre del municipio.
            tipo_via: Tipo de vía para filtrar (ej. "Calle", "Avenida").
                Vacío para buscar todos los tipos.
            nombre_calle: Nombre de la calle a buscar. Vacío para listar todas.

        Returns:
            list[CalleDTO]: Lista de calles encontradas.
        """
        response = self.providers.callejero.consulta_calles(
            provincia, municipio, tipo_via, nombre_calle
        )
        return CallejeroCalleParser().parse(response)

    # ── Geocoding ──────────────────────────────────────────

    def geocodificar(self, direccion: str, municipio: str) -> CartoCiudadDTO | None:
        """Geocodifica una dirección usando CartoCiudad.

        Convierte una dirección textual en coordenadas geográficas y
        referencia catastral.

        Args:
            direccion: Dirección a geocodificar (ej. "Calle Mayor 1").
            municipio: Nombre del municipio.

        Returns:
            CartoCiudadDTO | None: Resultado con coordenadas, referencia
                catastral y código postal, o None si no se encuentra.
        """
        response = self.providers.cartociudad.consulta_por_direccion(direccion, municipio)
        return CartoCiudadParser().parse(response)

    # ── Coordenadas ────────────────────────────────────────

    def rc_por_coordenadas(self, lat: float, lon: float) -> list[RefCatDTO]:
        """Obtiene la referencia catastral a partir de coordenadas geográficas.

        Args:
            lat: Latitud en grados decimales.
            lon: Longitud en grados decimales.

        Returns:
            list[RefCatDTO]: Lista de referencias catastrales que contienen
                las coordenadas proporcionadas.
        """
        response = self.providers.coordenadas.consulta_rc_por_coordenadas(
            lat, lon, self.proyeccion
        )
        return CoordenadasaRCParser().parse(response)

    def coordenadas_por_rc(self, rc: str) -> list[CentroideDTO]:
        """Convierte una referencia catastral a coordenadas geográficas.

        Args:
            rc: Referencia catastral (14 primeros caracteres del parcelario).

        Returns:
            list[CentroideDTO]: Lista de centroides con coordenadas y
                sistema de referencia.
        """
        response = self.providers.coordenadas.convertir_rc_a_coordenadas(
            rc, self.proyeccion
        )
        return RCaCoordenadasParser().parse(response)

    # ── Parcela ────────────────────────────────────────────

    def obtener_parcela_por_rc(self, rc: str) -> list[ParcelaCatastral]:
        """Obtiene la información completa de una parcela por su referencia catastral.

        Este es el método principal para obtener datos de una parcela. Si
        están habilitadas las opciones (geometrías, valores, construcciones,
        documentación), realiza las consultas adicionales necesarias.

        Args:
            rc: Referencia catastral de 20 caracteres (ej. "12345678901234AA1234F").

        Returns:
            list[ParcelaCatastral]: Lista con una o más parcelas que coinciden
                con la referencia.
        """
        response = self.providers.callejero.consulta_parcela_por_rc(rc)
        return self._obtener_parcelas(response, ParcelaCatastralRCParser())

    def obtener_parcela_por_polpar(self, provincia: str, municipio: str, poligono: int, parcela: int) -> list[ParcelaCatastral]:
        """Obtiene información de parcelas por polígono y número de parcela.

        Busca todas las parcelas dentro de un polígono catastral de un municipio.
        Si ``force_complete`` está activado y hay múltiples resultados, consulta
        individualmente cada parcela por RC para obtener datos completos.

        Args:
            provincia: Código de provincia o nombre.
            municipio: Nombre del municipio.
            poligono: Número de polígono catastral.
            parcela: Número de parcela dentro del polígono.

        Returns:
            list[ParcelaCatastral]: Lista de parcelas encontradas.
        """
        response = self.providers.callejero.consulta_parcela_por_polpar(
            provincia=provincia, municipio=municipio, poligono=poligono, parcela=parcela
        )
        return self._obtener_parcelas(response, ParcelaCatastralPolParParser())

    def obtener_parcela_por_direccion(self, provincia: str, municipio: str, tipo_via: str, calle: str, numero: str) -> list[ParcelaCatastral]:
        """Obtiene información de una parcela por su dirección completa.

        Busca la parcela que se encuentra en la dirección indicada. Si
        ``force_complete`` está activado y hay múltiples resultados, consulta
        individualmente cada parcela por RC para obtener datos completos.

        Args:
            provincia: Código de provincia o nombre.
            municipio: Nombre del municipio.
            tipo_via: Tipo de vía (ej. "Calle", "Avenida", "Plaza").
            calle: Nombre de la calle.
            numero: Número de la parcela en la calle.

        Returns:
            list[ParcelaCatastral]: Lista de parcelas encontradas en la dirección.
        """
        response = self.providers.callejero.consulta_parcela_por_direccion(
            provincia=provincia, municipio=municipio, tipo_via=tipo_via, calle=calle, numero=numero
        )
        return self._obtener_parcelas(response, ParcelaCatastralDirParser())

    # ── Internos ───────────────────────────────────────────

    def _obtener_parcelas(self, response: requests.Response, parser: CallejeroParser, *, _force_complete: bool = True) -> list[ParcelaCatastral]:
        dtos = parser.parse(response)

        if self.force_complete and _force_complete and len(dtos) > 1:
            resultados = []
            for dto in dtos:
                resultados.extend(
                    self.obtener_parcela_por_rc(dto.referenciaCatastral)
                )
            return resultados

        return [self._ensamblar_parcela(dto) for dto in dtos]

    def _ensamblar_parcela(self, dto: ParcelaCatastralDTO) -> ParcelaCatastral:
        geometria_dto = None
        croquis_dtos = None
        valor_urbano_dto = None
        valor_rustico_dto = None
        construcciones_dtos = None

        if self.include_geometries:
            resp = self.providers.inspire_parcelas.consultar_coordenadas_parcela(
                dto.referenciaCatastral, self.proyeccion
            )
            geometria_dto = INSPIREParcelParser().parse(resp)

        if self.include_values:
            if dto.tipo == "Urbano":
                resp = self.providers.coordenadas.convertir_rc_a_coordenadas(
                    dto.referenciaCatastral[:14], self.proyeccion
                )
                coords = RCaCoordenadasParser().parse(resp)
                if coords:
                    sr_num = self.proyeccion.split(":")[1]
                    resp = self.providers.valores_urbanos.consultar_valores_urbanos_m2(
                        coords[0].x, coords[0].y, self.anio_valores, srs=sr_num
                    )
                    valor_urbano_dtos = ValoresUrbanosParser().parse(resp)
                    if valor_urbano_dtos and valor_urbano_dtos[0].ptipos:
                        valor_urbano_dto = valor_urbano_dtos[0].ptipos[0]
            else:
                if geometria_dto:
                    bbox = self._calcular_bbox_3857(
                        geometria_dto.geometria, self.proyeccion
                    )
                    resp = self.providers.valores_rusticos.consulta_valores_rusticos_m2(
                        self.anio_valores, bbox
                    )
                    valor_rustico_dto = ValoresRusticosParser().parse(resp)

        if self.include_constructions:
            resp = self.providers.inspire_buildings.consulta_edificios(
                dto.referenciaCatastral, srsname=self.proyeccion
            )
            construcciones_dtos = INSPIREConstructionParser().parse(resp)

        if self.include_documentation:
            url = self.providers.croquis.consulta_url_croquis(
                dto.referenciaCatastral
            )
            croquis_dtos = [CroquisParser().parse(url)]

        return self.composer.compose(
            dto,
            geometria_dto=geometria_dto,
            croquis_dtos=croquis_dtos,
            valor_urbano_dto=valor_urbano_dto,
            valor_rustico_dto=valor_rustico_dto,
            construcciones_dtos=construcciones_dtos,
        )

    @staticmethod
    def _calcular_bbox_3857(geometria_dto: 'GeometriaDTO', proyeccion_origen: str) -> str:
        transformer = Transformer.from_crs(
            proyeccion_origen, "EPSG:3857", always_xy=True
        )
        xs, ys = [], []
        for punto in geometria_dto.puntos:
            x, y = transformer.transform(float(punto.coordenadas[0]), float(punto.coordenadas[1]))
            xs.append(x)
            ys.append(y)
        return f"{min(xs)},{min(ys)},{max(xs)},{max(ys)}"
