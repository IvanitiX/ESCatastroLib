from __future__ import annotations

from ...models.Documentacion import Documento
from ...parsers.CatastroES.Croquis.dto import CroquisDTO


class DocumentoMapper:
    @staticmethod
    def map(dto: CroquisDTO) -> Documento:
        return Documento(
            url=dto.url,
            descripcion="Croquis catastral",
        )
