from __future__ import annotations

from ...models.ParcelaCatastral import ParcelaUrbana
from ...models.Callejero import Calle, Municipio
from ...parsers.CatastroES.Callejero.dto import ParcelaCatastralDTO


class ParcelaUrbanaMapper:
    @staticmethod
    def map(dto: ParcelaCatastralDTO, municipio: Municipio, valor_m2: float = 0.0) -> ParcelaUrbana:
        calle_completa = dto.calle or ""
        partes = calle_completa.split(" ", 1)
        tipo_via = partes[0] if len(partes) > 1 else ""
        nombre_calle = partes[1] if len(partes) > 1 else calle_completa

        return ParcelaUrbana(
            calle=Calle(
                municipio=municipio,
                tipo_via=tipo_via,
                calle=nombre_calle,
            ),
            numero=int(dto.numero) if dto.numero else 0,
            antiguedad=int(dto.antiguedad) if dto.antiguedad else 0,
            uso=dto.uso or "",
            valor_m2=valor_m2,
        )
