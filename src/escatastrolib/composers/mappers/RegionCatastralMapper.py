

from ...models.RegionCatastral import RegionCatastral
from ...parsers.CatastroES.Callejero.dto import RegionCatastralDTO


class RegionCatastralMapper:
    """Mapper para convertir DTOs de regiones catastrales a modelos de dominio.

    Transforma los DTOs de regiones catastrales (elementos de una parcela)
    en objetos RegionCatastral, concatenando descripción, escalera, planta y puerta.
    """
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
