from typing import Any

from .base import BaseCatastroClient


class NavarraClient(BaseCatastroClient):
    """Catastro de Navarra — https://catastro.navarra.es"""

    def __init__(self, **kwargs: Any) -> None:
        pass

    def obtener_provincias(self) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")

    def buscar_municipios(self, provincia: str, municipio: str) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")

    def buscar_calles(self, provincia: str, municipio: str, tipo_via: str, nombre_calle: str) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")

    def geocodificar(self, direccion: str, municipio: str) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")

    def rc_por_coordenadas(self, lat: float, lon: float) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")

    def coordenadas_por_rc(self, rc: str) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")

    def obtener_parcela_por_rc(self, rc: str) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")

    def obtener_parcela_por_polpar(self, provincia: str, municipio: str, poligono: int, parcela: int) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")

    def obtener_parcela_por_direccion(self, provincia: str, municipio: str, tipo_via: str, calle: str, numero: str) -> Any:
        raise NotImplementedError("NavarraClient pendiente de implementar")
