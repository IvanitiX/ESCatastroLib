from dataclasses import dataclass

@dataclass
class ProvinciaDTO:
    codigoProvincia: int
    nombreProvincia: str

@dataclass
class MunicipioDTO:
    nombreMunicipio: str

@dataclass
class CalleDTO:
    tipoViaCatastral: str
    nombreCatastral: str
    tipoViaINE: str
    nombreINE: str

@dataclass
class RegionCatastralDTO:
    descripcion: str
    superficie: float
    escalera: str | None
    planta: str | None
    puerta: str | None

@dataclass
class ParcelaCatastralDTO:
    referenciaCatastral: str
    municipio: str
    provincia: str
    tipo: str
    calle: str | None
    numero: str | None
    escalera: str | None
    planta: str | None
    puerta: str | None
    antiguedad: str | None
    superficie_economica: float | None
    uso: str | None
    parcela: int | None
    poligono: int | None
    nombre_paraje: int | None
    regiones: list[RegionCatastralDTO] | None
    superficie_finca: float | None = None
    superficie_solar: float | None = None

