

from ...models.Callejero import Calle, Municipio
from ...parsers.CatastroES.Callejero.dto import CalleDTO
from ...utils.Mappings import TIPOS_VIA


class CalleMapper:
    """Mapper para convertir DTOs de calle a modelos de dominio.

    Transforma los DTOs de calles del Catastro en objetos Calle
    del modelo de dominio, incluyendo el mapeo de tipos de vía.
    """
    @staticmethod
    def map(dto: CalleDTO, municipio: Municipio) -> Calle:
        tipo_via = TIPOS_VIA.get(dto.tipoViaCatastral, dto.tipoViaCatastral)
        return Calle(
            municipio=municipio,
            tipo_via=tipo_via,
            calle=dto.nombreCatastral,
        )
