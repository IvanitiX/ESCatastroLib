from dataclasses import dataclass


@dataclass
class Municipio:
    """Representa un municipio español con su provincia.

    Attributes:
        municipio: Nombre del municipio.
        provincia: Nombre de la provincia.
    """

    municipio: str
    provincia: str


@dataclass
class Calle:
    """Representa una calle dentro de un municipio.

    Attributes:
        municipio: Municipio al que pertenece la calle.
        tipo_via: Tipo de vía (Calle, Avenida, Plaza, etc.).
        calle: Nombre de la calle según el Catastro.
    """

    municipio: Municipio
    tipo_via: str
    calle: str