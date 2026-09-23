from typing import Any

from ..utils.territories import (
    Territorio,
    detectar_territorio,
    territorio_por_provincia,
)
from ..errors.ErrorServidorDGC import ErrorServidorSedeCatastro


_ORDEN_TRIAL_ERROR = [
    Territorio.ESPANA,
    Territorio.GUIPUZKOA,
    Territorio.ARABA,
]


class ParcelaCatastral:
    """Servicio de parcelas catastrales con interfaz de constructor directo.

    Permite consultar parcelas catastrales de forma similar al original:
    se instancia con los parámetros de búsqueda y los datos se cargan
    automáticamente en self.parcelas.

    Args:
        rc: Referencia catastral (20 caracteres).
        provincia: Nombre o código de la provincia.
        municipio: Nombre o código del municipio.
        poligono: Número de polígono (búsqueda por parcela).
        parcela: Número de parcela (búsqueda por parcela).
        tipo_via: Tipo de vía (búsqueda por dirección).
        calle: Nombre de la calle (búsqueda por dirección).
        numero: Número de la dirección (búsqueda por dirección).
        projection: Sistema de referencia espacial. Default "EPSG:4326".
        include_geometries: Si True, incluye geometría INSPIRE.
        include_values: Si True, incluye valoración del suelo.
        anio_valores: Año de consulta para valores catastrales.
        include_regions: Si True, incluye regiones catastrales.
        include_constructions: Si True, incluye construcciones.
        include_documentation: Si True, incluye documentos (croquis).
        force_complete: Si True, re-consulta por RC cuando hay múltiples resultados.

    Raises:
        ValueError: Si no se proporciona suficiente información para la búsqueda.

    Attributes:
        parcelas: Lista de parcelas catastrales encontradas (list[ParcelaCatastralModel]).
    """

    def __init__(
        self,
        rc: str | None = None,
        provincia: str | None = None,
        municipio: str | None = None,
        poligono: int | None = None,
        parcela: int | None = None,
        tipo_via: str | None = None,
        calle: str | None = None,
        numero: str | None = None,
        query_direccion: str | None = None,
        projection: str = "EPSG:4326",
        include_geometries: bool = False,
        include_values: bool = False,
        anio_valores: int | None = None,
        include_regions: bool = False,
        include_constructions: bool = False,
        include_documentation: bool = False,
        force_complete: bool = False,
    ) -> None:
        self._options = dict(
            proyeccion=projection,
            include_geometries=include_geometries,
            include_values=include_values,
            anio_valores=anio_valores,
            include_regions=include_regions,
            include_constructions=include_constructions,
            include_documentation=include_documentation,
            force_complete=force_complete,
        )
        self._cliente = None
        self._territorio: Territorio | None = None
        self.resultados: list[Any] = []

        if rc:
            self._create_from_rc(rc)
        elif provincia and municipio and poligono and parcela:
            self._create_from_parcel(provincia, municipio, poligono, parcela)
        elif provincia and municipio and tipo_via and calle and numero:
            self._create_from_address(provincia, municipio, tipo_via, calle, numero)
        elif query_direccion and municipio:
            self._create_from_rc(rc=self.geocodificar(query_direccion, municipio).referencia_catastral)
        else:
            raise ValueError(
                "No se ha proporcionado suficiente información para realizar la búsqueda. "
                "Usa rc, o provincia+municipio+poligono+parcela; o "
                "provincia+municipio+tipo_via+calle+numero; o query_direccion+municipio."
            )

    # ── Client management ───────────────────────────────────

    def _instanciar_cliente(self, territorio: Territorio):
        match territorio:
            case Territorio.ESPANA:
                from ..clients.CatastroES import CatastroESClient
                return CatastroESClient(**self._options)
            case Territorio.NAVARRA:
                from ..clients.Navarra import NavarraClient
                return NavarraClient(**self._options)
            case Territorio.GUIPUZKOA:
                from ..clients.Gipuzkoa import GipuzkoaClient
                return GipuzkoaClient(**self._options)
            case Territorio.ARABA:
                from ..clients.Araba import ArabaClient
                return ArabaClient(**self._options)
            case Territorio.BIZKAIA:
                from ..clients.Bizkaia import BizkaiaClient
                return BizkaiaClient(**self._options)
            case _:
                raise ValueError(f"Territorio no soportado: {territorio}")

    def _usar_cliente(self, territorio: Territorio) -> None:
        if territorio != self._territorio:
            self._territorio = territorio
            self._cliente = self._instanciar_cliente(territorio)

    def _trial_and_error(self, metodo: str, *args: Any, **kwargs: Any) -> Any:
        for territorio in _ORDEN_TRIAL_ERROR:
            try:
                cliente = self._instanciar_cliente(territorio)
                return getattr(cliente, metodo)(*args, **kwargs)
            except (ErrorServidorSedeCatastro, NotImplementedError):
                continue
        raise ValueError(
            f"Ningún cliente pudo resolver la consulta para: {args}"
        )

    # ── Creation methods ────────────────────────────────────

    def _create_from_rc(self, rc: str) -> None:
        territorio = detectar_territorio(rc)
        if territorio == Territorio.DESCONOCIDO:
            self.resultados = self._trial_and_error("obtener_parcela_por_rc", rc)
        else:
            self._usar_cliente(territorio)
            self.resultados = self._cliente.obtener_parcela_por_rc(rc)

    def _create_from_parcel(self, provincia: str, municipio: str, poligono: int, parcela: int) -> None:
        territorio = territorio_por_provincia(provincia)
        self._usar_cliente(territorio)
        self.resultados = self._cliente.obtener_parcela_por_polpar(
            provincia, municipio, poligono, parcela
        )

    def _create_from_address(self, provincia: str, municipio: str, tipo_via: str, calle: str, numero: str) -> None:
        territorio = territorio_por_provincia(provincia)
        self._usar_cliente(territorio)
        self.resultados = self._cliente.obtener_parcela_por_direccion(
            provincia, municipio, tipo_via, calle, numero
        )

    # ── Callejero (delegates) ───────────────────────────────

    def _requiere_cliente(self) -> None:
        if self._cliente is None:
            raise ValueError(
                "No hay cliente inicializado. Primero crea una parcela "
                "(rc, polígono o dirección) o instancia con territorio explícito."
            )

    def obtener_provincias(self) -> Any:
        """Consulta la lista de provincias españolas."""
        self._requiere_cliente()
        return self._cliente.obtener_provincias()

    def buscar_municipios(self, provincia: str, municipio: str) -> Any:
        """Busca municipios por provincia y nombre."""
        self._requiere_cliente()
        return self._cliente.buscar_municipios(provincia, municipio)

    def buscar_calles(self, provincia: str, municipio: str, tipo_via: str = "", nombre_calle: str = "") -> Any:
        """Busca calles dentro de un municipio."""
        self._requiere_cliente()
        return self._cliente.buscar_calles(provincia, municipio, tipo_via, nombre_calle)

    # ── Geocoding (delegates) ───────────────────────────────

    def geocodificar(self, direccion: str, municipio: str) -> Any:
        """Geocodifica una dirección usando CartoCiudad."""
        self._usar_cliente(territorio=Territorio.ESPANA)
        return self._cliente.geocodificar(direccion, municipio)

    # ── Coordenadas (delegates) ─────────────────────────────

    def rc_por_coordenadas(self, lat: float, lon: float) -> Any:
        """Obtiene la referencia catastral a partir de coordenadas."""
        self._requiere_cliente()
        return self._cliente.rc_por_coordenadas(lat, lon)

    def coordenadas_por_rc(self, rc: str) -> Any:
        """Convierte una referencia catastral a coordenadas."""
        self._requiere_cliente()
        return self._cliente.coordenadas_por_rc(rc)
