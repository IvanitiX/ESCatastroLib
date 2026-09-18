from __future__ import annotations

from ...models.ValorUrbano import ValorUrbano
from ...parsers.CatastroES.MapaValoresUrbanos.dto import ValorUrbanoDTO


class ValorUrbanoMapper:
    @staticmethod
    def map(dto: ValorUrbanoDTO) -> ValorUrbano:
        return ValorUrbano(
            tipologia=dto.tipologia,
            superficie=dto.superficie,
            val_suelo=dto.val_suelo,
            val_construccion=dto.val_construccion_pt,
            val_catastral=dto.val_catastral,
            val_tipo_m2=dto.val_tipo_m2,
        )
