from __future__ import annotations

from ...models.RegionCatastral import RegionCatastral
from ...parsers.CatastroES.Callejero.dto import RegionCatastralDTO


class RegionCatastralMapper:
    @staticmethod
    def map(dto: RegionCatastralDTO) -> RegionCatastral:
        desc_parts = [dto.descripcion]
        if dto.escalera:
            desc_parts.append(f"Esc.{dto.escalera}")
        if dto.planta:
            desc_parts.append(f"Pl.{dto.planta}")
        if dto.puerta:
            desc_parts.append(f"Pu.{dto.puerta}")

        return RegionCatastral(
            descripcion=" - ".join(desc_parts),
            superficie=dto.superficie,
        )
