from typing import Any
from ...typing import to_float, to_str, to_int

import requests

from .dto import RecintoValorUrbanoDTO, ValorUrbanoDTO


class ValoresUrbanosParser:
    """Parser para valores catastrales urbanos.

    Parsea las respuestas JSON del servicio de mapa de valores urbanos
    del Catastro y extrae los valores de suelo, construcción y catastrales
    de los inmuebles urbanos.
    """
    def parse(self, response: requests.Response) -> list[RecintoValorUrbanoDTO]:
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

    def _to_dtos(self, data: dict[str, Any]) -> list[RecintoValorUrbanoDTO]:
        features = data.get("features", [])
        lista_dtos = []

        for feature in features:
            propiedades = feature.get("properties", {})
            geometry = feature.get("geometry")

            ptipos = []

            for nombre, valores in propiedades.items():
                if not nombre.startswith("Ptipo"):
                    continue

                if not isinstance(valores, dict):
                    continue

                ptipos.append(
                    ValorUrbanoDTO(
                        id_producto_tipo=to_str(valores.get(
                            "id_producto_tipo"
                        )),
                        id_delegacion=to_str(valores.get(
                            "id_delegacion"
                        )),
                        id_municipio=to_str(valores.get(
                            "id_municipio"
                        )),
                        fecha=valores.get("fecha"),
                        id_recinto_valoracion=to_str(valores.get(
                            "id_recinto_valoracion"
                        )),
                        orden=to_int(valores.get("orden")),
                        num_inmueble=to_int(valores.get(
                            "num_inmueble"
                        )),

                        codigo_uso=to_str(valores.get("codigo_uso")),
                        tipologia=to_str(valores.get("tipologia")),
                        coef_propiedad=to_float(valores.get(
                            "coef_propiedad"
                        )),
                        categoria=to_str(valores.get("categoria")),
                        antiguedad=to_int(valores.get("antiguedad")),
                        conservacion=to_str(valores.get("conservacion")),
                        superficie=to_int(valores.get("superficie")),
                        tipologia_anejos=to_str(valores.get(
                            "tipologia_anejos"
                        )),
                        edificabilidad=to_str(valores.get(
                            "edificabilidad"
                        )),
                        num_altura=to_int(valores.get("num_altura")),
                        superficie_minima=to_float(valores.get(
                            "superficie_minima"
                        )),
                        superficie_suelo=to_float(valores.get(
                            "superficie_suelo"
                        )),
                        porc_suelo_interior=to_float(valores.get(
                            "porc_suelo_interior"
                        )),

                        val_suelo=to_float(valores.get("val_suelo")),
                        val_construccion_pt=to_float(valores.get(
                            "val_construccion_pt"
                        )),
                        val_construccion_pe=to_float(valores.get(
                            "val_construccion_pe"
                        )),
                        val_suelos_gar=to_float(valores.get(
                            "val_suelos_gar"
                        )),
                        val_construccion_pt_garaje=to_float(valores.get(
                            "val_construccion_pt_garaje"
                        )),
                        val_construccion_pe_garaje=to_float(valores.get(
                            "val_construccion_pe_garaje"
                        )),
                        val_catastral=to_float(valores.get(
                            "val_catastral"
                        )),

                        num_inmuebles_recinto=to_int(valores.get(
                            "num_inmuebles_recinto"
                        )),
                        num_garajes_recinto=to_int(valores.get(
                            "num_garajes_recinto"
                        )),

                        val_tipo=to_float(valores.get("val_tipo")),
                        val_tipo_m2=to_float(valores.get("val_tipo_m2")),
                        val_tipo_m2_min=to_float(valores.get(
                            "val_tipo_m2_min"
                        )),
                        val_tipo_mostrar=to_str(valores.get(
                            "val_tipo_mostrar"
                        )),
                        val_estandar=to_float(valores.get(
                            "val_estandar"
                        )),
                        val_estandar_m2=to_float(valores.get(
                            "val_estandar_m2"
                        )),
                    )
                )

            lista_dtos.append(
                RecintoValorUrbanoDTO(
                    geometry=geometry,
                    ptipos=ptipos,
                )
            )

        return lista_dtos
