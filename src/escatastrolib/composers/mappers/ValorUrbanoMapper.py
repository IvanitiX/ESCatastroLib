from __future__ import annotations

from ...models.ValorUrbano import ValorUrbano
from ...parsers.CatastroES.MapaValoresUrbanos.dto import ValorUrbanoDTO


class ValorUrbanoMapper:
    """Mapper para convertir DTOs de valores urbanos a modelos de dominio.

    Transforma los DTOs del mapa de valores urbanos del Catastro en
    objetos ValorUrbano con información de tipología, superficie y valores.
    """
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
