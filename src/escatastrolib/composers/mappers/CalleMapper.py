from __future__ import annotations

from ...models.Callejero import Calle, Municipio
from ...parsers.CatastroES.Callejero.dto import CalleDTO
from ...utils.Mappings import TIPOS_VIA


class CalleMapper:
    @staticmethod
    def map(dto: CalleDTO, municipio: Municipio) -> Calle:
        tipo_via = TIPOS_VIA.get(dto.tipoViaCatastral, dto.tipoViaCatastral)
        return Calle(
            municipio=municipio,
            tipo_via=tipo_via,
            calle=dto.nombreCatastral,
        )
