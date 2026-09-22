from typing import Any
from ...typing import to_str, to_float

import requests

from .dto import ValoresRusticosDTO

class ValoresRusticosParser:
    """Parser para valores catastrales rústicos.

    Parsea las respuestas JSON del servicio de mapa de valores rústicos
    del Catastro y extrae los valores por m² de diferentes tipos de cultivo.
    """
    def parse(self, response: requests.Response) -> list[ValoresRusticosDTO]:
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError as error:
            raise ValueError(
                "La respuesta no contiene un JSON válido"
            ) from error

        if not data:
            return []

        return self._to_dtos(data)
     
    def _to_dtos(self, data: dict[str, Any]) -> list[ValoresRusticosDTO]:
        features = data.get('features',{})
        lista_dtos = []

        for feature in features:
            propiedades = feature.get('properties',{})

            lista_dtos.append(ValoresRusticosDTO(
                region=to_str(propiedades.get('REGIONAL')),
                nombre_region=to_str(propiedades.get('NOMBRE')),
                valor_m2_arrozales=to_float(propiedades.get('ARZ')),
                valor_m2_citricos=to_float(propiedades.get('CIT')),
                valor_m2_cultivos_bajo_plastico=to_float(propiedades.get('CBP')),
                valor_m2_cultivos_subtropicales_tropicales=to_float(propiedades.get('SBT')),
                valor_m2_frutales_carnosos_regadio=to_float(propiedades.get('FCR')),
                valor_m2_frutales_carnosos_secano=to_float(propiedades.get('FCS')),
                valor_m2_frutos_secos_regadio=to_float(propiedades.get('FSR')),
                valor_m2_frutos_secos_secano=to_float(propiedades.get('FSS')),
                valor_m2_huertos=to_float(propiedades.get('HUE')),
                valor_m2_olivares_regadio=to_float(propiedades.get('OLR')),
                valor_m2_olivares_secano=to_float(propiedades.get('OLS')),
                valor_m2_pastizales=to_float(propiedades.get('PST')),
                valor_m2_plataneras=to_float(propiedades.get('PLT')),
                valor_m2_prados=to_float(propiedades.get('PRD')),
                valor_m2_tierras_arables_regadio=to_float(propiedades.get('TAR')),
                valor_m2_tierras_arables_secano=to_float(propiedades.get('TAS')),
                valor_m2_vinedos_regadio=to_float(propiedades.get('VIR')),
                valor_m2_vinedos_secano=to_float(propiedades.get('VIS'))
            ))

        return lista_dtos
