from __future__ import annotations

from ...models.Documentacion import Documento
from ...parsers.CatastroES.Croquis.dto import CroquisDTO


class DocumentoMapper:
    """Mapper para convertir DTOs de documentos a modelos de dominio.

    Transforma los DTOs de croquis y otros documentos del Catastro
    en objetos Documento del modelo de dominio.
    """
    @staticmethod
    def map(dto: CroquisDTO) -> Documento:
        return Documento(
            url=dto.url,
            descripcion="Croquis catastral",
        )
