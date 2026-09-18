

from ...models.ValorRustico import ValorRustico
from ...parsers.CatastroES.MapaValoresRusticos.dto import ValoresRusticosDTO


class ValorRusticoMapper:
    """Mapper para convertir DTOs de valores rústicos a modelos de dominio.

    Transforma los DTOs del mapa de valores rústicos del Catastro en
    objetos ValorRustico con los valores por m² de diferentes tipos de cultivo.
    """
    @staticmethod
    def map(dto: ValoresRusticosDTO) -> ValorRustico:
        return ValorRustico(
            region=dto.region,
            nombre_region=dto.nombre_region,
            valor_m2_tierras_arables_secano=dto.valor_m2_tierras_arables_secano,
            valor_m2_tierras_arables_regadio=dto.valor_m2_tierras_arables_regadio,
            valor_m2_huertos=dto.valor_m2_huertos,
            valor_m2_cultivos_bajo_plastico=dto.valor_m2_cultivos_bajo_plastico,
            valor_m2_arrozales=dto.valor_m2_arrozales,
            valor_m2_citricos=dto.valor_m2_citricos,
            valor_m2_frutales_carnosos_secano=dto.valor_m2_frutales_carnosos_secano,
            valor_m2_frutos_secos_secano=dto.valor_m2_frutos_secos_secano,
            valor_m2_cultivos_subtropicales_tropicales=dto.valor_m2_cultivos_subtropicales_tropicales,
            valor_m2_plataneras=dto.valor_m2_plataneras,
            valor_m2_frutales_carnosos_regadio=dto.valor_m2_frutales_carnosos_regadio,
            valor_m2_frutos_secos_regadio=dto.valor_m2_frutos_secos_regadio,
            valor_m2_vinedos_secano=dto.valor_m2_vinedos_secano,
            valor_m2_vinedos_regadio=dto.valor_m2_vinedos_regadio,
            valor_m2_olivares_secano=dto.valor_m2_olivares_secano,
            valor_m2_olivares_regadio=dto.valor_m2_olivares_regadio,
            valor_m2_prados=dto.valor_m2_prados,
            valor_m2_pastizales=dto.valor_m2_pastizales,
        )
