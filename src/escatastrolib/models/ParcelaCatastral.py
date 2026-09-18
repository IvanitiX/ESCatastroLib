from __future__ import annotations

from dataclasses import dataclass

from .Callejero import Municipio, Calle
from .GeometriaCatastral import Geometria
from .RegionCatastral import RegionCatastral
from .Documentacion import Documento
from .Construction import Construction
from .ValorUrbano import ValorUrbano
from .ValorRustico import ValorRustico


@dataclass
class ParcelaUrbana:
    """Datos específicos de una parcela de tipo urbano.

    Attributes:
        calle: Calle donde se ubica la parcela.
        numero: Número de la parcela en la calle.
        antiguedad: Antigüedad de la construcción en años.
        uso: Uso principal de la parcela (ej. "Vivienda", "Comercial").
        valor_m2: Valor por metro cuadrado del suelo en euros.
    """

    calle: Calle
    numero: int
    antiguedad: int
    uso: str
    valor_m2: float


@dataclass
class ParcelaRustica:
    """Datos específicos de una parcela de tipo rústico.

    Attributes:
        poligono: Número de polígono catastral.
        parcela: Número de parcela dentro del polígono.
        nombre_paraje: Nombre del paraje o lugar donde se ubica.
        valor_m2: Valor por metro cuadrado del suelo en euros.
    """

    poligono: int
    parcela: int
    nombre_paraje: str
    valor_m2: float


@dataclass
class ParcelaCatastral:
    """Modelo principal que representa una parcela catastral completa.

    Modelo de dominio central de la librería. Integra toda la información
    disponible de una parcela: identificación, ubicación, superficies,
    construcciones, geometría, documentación y valoraciones.

    Attributes:
        referencia_catastral: Referencia catastral de la parcela (20 caracteres).
        municipio: Municipio al que pertenece la parcela.
        tipo: Tipo de parcela: "Urbano" o "Rústico".
        completo: True si la información es completa, False si es parcial.
        superficie_plana: Superficie de la parcela en m² (suelo).
        superficie_construida: Superficie total construida en m².
        datos_urbanos: Datos específicos urbanos, o None si es rústica.
        datos_rusticos: Datos específicos rústicos, o None si es urbana.
        regiones: Lista de regiones catastrales de la parcela.
        construcciones: Lista de construcciones sobre la parcela.
        geometria: Geometría de la parcela, o None si no está disponible.
        documentacion: Documentos asociados (croquis, planos, etc.).
        valor_urbano: Valoración urbana del suelo, o None.
        valor_rustico: Valoración rústica del suelo, o None.
    """

    referencia_catastral: str
    municipio: Municipio
    tipo: str
    completo: bool
    superficie_plana: float
    superficie_construida: float
    datos_urbanos: ParcelaUrbana | None
    datos_rusticos: ParcelaRustica | None
    regiones: list[RegionCatastral] | None
    construcciones: list[Construction] | None
    geometria: Geometria | None
    documentacion: list[Documento] | None
    valor_urbano: ValorUrbano | None
    valor_rustico: ValorRustico | None

    @property
    def perimetro(self) -> float:
        """Perímetro de la parcela en metros lineales."""
        return self.geometria.perimetro if self.geometria else 0.0
