from dataclasses import dataclass


@dataclass
class CartoCiudadDTO:
    id: str | None = None
    provincia: str | None = None
    comunidad_autonoma: str | None = None
    municipio: str | None = None
    direccion: str | None = None
    codigo_postal: str | None = None
    longitud: float | None = None
    latitud: float | None = None
    numero: int | None = None
    sin_numero: bool = False
    extension: bool = False
    referencia_catastral: str | None = None