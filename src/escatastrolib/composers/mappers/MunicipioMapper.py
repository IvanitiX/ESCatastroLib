from __future__ import annotations

from ...models.Callejero import Municipio
from ...parsers.CatastroES.Callejero.dto import MunicipioDTO, ProvinciaDTO


class MunicipioMapper:
    @staticmethod
    def map(municipio_dto: MunicipioDTO, provincia_dto: ProvinciaDTO) -> Municipio:
        return Municipio(
            municipio=municipio_dto.nombreMunicipio,
            provincia=provincia_dto.nombreProvincia,
        )
