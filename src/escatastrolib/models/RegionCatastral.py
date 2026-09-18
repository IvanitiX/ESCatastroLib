from dataclasses import dataclass


@dataclass
class RegionCatastral:
    """Región catastral de una parcela (vivienda, local, parcela rústica).

    Representa una subdivisión catastral dentro de una parcela, como una
    vivienda individual en un edificio, un local comercial, o una parcela
    rústica concreta.

    Attributes:
        descripcion: Descripción de la región (ej. "Esc. A - Pl. 3 - Pu. 2").
        superficie: Superficie de la región en metros cuadrados.
    """

    descripcion: str
    superficie: float
