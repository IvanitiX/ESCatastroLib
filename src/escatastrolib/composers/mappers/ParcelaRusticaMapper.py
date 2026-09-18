

from ...models.ParcelaCatastral import ParcelaRustica
from ...parsers.CatastroES.Callejero.dto import ParcelaCatastralDTO


class ParcelaRusticaMapper:
    """Mapper para convertir DTOs de parcela rústica a modelos de dominio.

    Transforma los DTOs de parcelas catastrales rústicas en objetos
    ParcelaRustica con la información de polígono, parcela y valor m².
    """
    @staticmethod
    def map(dto: ParcelaCatastralDTO, valor_m2: float = 0.0) -> ParcelaRustica:
        return ParcelaRustica(
            poligono=int(dto.poligono) if dto.poligono else 0,
            parcela=int(dto.parcela) if dto.parcela else 0,
            nombre_paraje=str(dto.nombre_paraje) if dto.nombre_paraje else "",
            valor_m2=valor_m2,
        )
