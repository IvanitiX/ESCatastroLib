from dataclasses import dataclass

@dataclass
class ValoresRusticosDTO:
    region: str
    nombre_region: str

    # Cada tipo de tierra tiene su valor
    valor_m2_tierras_arables_secano: float
    valor_m2_tierras_arables_regadio: float
    valor_m2_huertos: float
    valor_m2_cultivos_bajo_plastico: float
    valor_m2_arrozales: float
    valor_m2_citricos: float
    valor_m2_frutales_carnosos_secano: float
    valor_m2_frutos_secos_secano: float
    valor_m2_cultivos_subtropicales_tropicales: float
    valor_m2_plataneras: float
    valor_m2_frutales_carnosos_regadio: float
    valor_m2_frutos_secos_regadio: float
    valor_m2_vinedos_secano: float
    valor_m2_vinedos_regadio: float
    valor_m2_olivares_secano: float
    valor_m2_olivares_regadio: float
    valor_m2_prados: float
    valor_m2_pastizales: float


