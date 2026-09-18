from dataclasses import dataclass


@dataclass
class ValorRustico:
    """Valoración de suelo rústico por tipo de cultivo y región.

    Contiene los valores por metro cuadrado de los diferentes tipos de
    cultivo y aprovechamiento del suelo rústico en una región concreta.

    Attributes:
        region: Código de la región catastral.
        nombre_region: Nombre descriptivo de la región.
        valor_m2_tierras_arables_secano: Valor m² tierras arables de secano.
        valor_m2_tierras_arables_regadio: Valor m² tierras arables de regadío.
        valor_m2_huertos: Valor m² de huertos.
        valor_m2_cultivos_bajo_plastico: Valor m² de cultivos bajo plástico.
        valor_m2_arrozales: Valor m² de arrozales.
        valor_m2_citricos: Valor m² de cítricos.
        valor_m2_frutales_carnosos_secano: Valor m² frutales carnosos de secano.
        valor_m2_frutos_secos_secano: Valor m² frutos secos de secano.
        valor_m2_cultivos_subtropicales_tropicales: Valor m² cultivos subtropicales y tropicales.
        valor_m2_plataneras: Valor m² de plataneras.
        valor_m2_frutales_carnosos_regadio: Valor m² frutales carnosos de regadío.
        valor_m2_frutos_secos_regadio: Valor m² frutos secos de regadío.
        valor_m2_vinedos_secano: Valor m² de viñedos de secano.
        valor_m2_vinedos_regadio: Valor m² de viñedos de regadío.
        valor_m2_olivares_secano: Valor m² de olivares de secano.
        valor_m2_olivares_regadio: Valor m² de olivares de regadío.
        valor_m2_prados: Valor m² de prados.
        valor_m2_pastizales: Valor m² de pastizales.
    """

    region: str
    nombre_region: str
    valor_m2_tierras_arables_secano: float = 0.0
    valor_m2_tierras_arables_regadio: float = 0.0
    valor_m2_huertos: float = 0.0
    valor_m2_cultivos_bajo_plastico: float = 0.0
    valor_m2_arrozales: float = 0.0
    valor_m2_citricos: float = 0.0
    valor_m2_frutales_carnosos_secano: float = 0.0
    valor_m2_frutos_secos_secano: float = 0.0
    valor_m2_cultivos_subtropicales_tropicales: float = 0.0
    valor_m2_plataneras: float = 0.0
    valor_m2_frutales_carnosos_regadio: float = 0.0
    valor_m2_frutos_secos_regadio: float = 0.0
    valor_m2_vinedos_secano: float = 0.0
    valor_m2_vinedos_regadio: float = 0.0
    valor_m2_olivares_secano: float = 0.0
    valor_m2_olivares_regadio: float = 0.0
    valor_m2_prados: float = 0.0
    valor_m2_pastizales: float = 0.0
