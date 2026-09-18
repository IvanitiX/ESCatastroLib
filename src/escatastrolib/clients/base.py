from abc import ABC, abstractmethod
from typing import Any


class BaseCatastroClient(ABC):
    @abstractmethod
    def obtener_provincias(self) -> Any: ...

    @abstractmethod
    def buscar_municipios(self, provincia: str, municipio: str) -> Any: ...

    @abstractmethod
    def buscar_calles(self, provincia: str, municipio: str, tipo_via: str, nombre_calle: str) -> Any: ...

    @abstractmethod
    def geocodificar(self, direccion: str, municipio: str) -> Any: ...

    @abstractmethod
    def rc_por_coordenadas(self, lat: float, lon: float) -> Any: ...

    @abstractmethod
    def coordenadas_por_rc(self, rc: str) -> Any: ...

    @abstractmethod
    def obtener_parcela_por_rc(self, rc: str) -> Any: ...

    @abstractmethod
    def obtener_parcela_por_polpar(self, provincia: str, municipio: str, poligono: int, parcela: int) -> Any: ...

    @abstractmethod
    def obtener_parcela_por_direccion(self, provincia: str, municipio: str, tipo_via: str, calle: str, numero: str) -> Any: ...
