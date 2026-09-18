

from ...models.Callejero import Municipio
from ...parsers.CatastroES.Callejero.dto import MunicipioDTO, ProvinciaDTO


class MunicipioMapper:
    """Mapper para convertir DTOs de municipio a modelos de dominio.

    Transforma los DTOs obtenidos del parseo de respuestas del Catastro
    en objetos Municipio del modelo de dominio.
    """
    @staticmethod
    def map(municipio_dto: MunicipioDTO, provincia_dto: ProvinciaDTO) -> Municipio:
        return Municipio(
            municipio=municipio_dto.nombreMunicipio,
            provincia=provincia_dto.nombreProvincia,
        )
