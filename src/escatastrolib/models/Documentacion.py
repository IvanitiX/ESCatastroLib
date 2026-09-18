from dataclasses import dataclass


@dataclass
class Documento:
    """Documento asociado a una parcela catastral (croquis, plano, etc.).

    Attributes:
        url: URL de descarga del documento.
        descripcion: Descripción del tipo de documento (ej. "Croquis catastral").
    """

    url: str
    descripcion: str