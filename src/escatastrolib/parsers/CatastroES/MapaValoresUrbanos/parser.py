from typing import Any

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
                        id_producto_tipo=valores.get(
                            "id_producto_tipo"
                        ),
                        id_delegacion=valores.get(
                            "id_delegacion"
                        ),
                        id_municipio=valores.get(
                            "id_municipio"
                        ),
                        fecha=valores.get("fecha"),
                        id_recinto_valoracion=valores.get(
                            "id_recinto_valoracion"
                        ),
                        orden=valores.get("orden"),
                        num_inmueble=valores.get(
                            "num_inmueble"
                        ),

                        codigo_uso=valores.get("codigo_uso"),
                        tipologia=valores.get("tipologia"),
                        coef_propiedad=valores.get(
                            "coef_propiedad"
                        ),
                        categoria=valores.get("categoria"),
                        antiguedad=valores.get("antiguedad"),
                        conservacion=valores.get("conservacion"),
                        superficie=valores.get("superficie"),
                        tipologia_anejos=valores.get(
                            "tipologia_anejos"
                        ),
                        edificabilidad=valores.get(
                            "edificabilidad"
                        ),
                        num_altura=valores.get("num_altura"),
                        superficie_minima=valores.get(
                            "superficie_minima"
                        ),
                        superficie_suelo=valores.get(
                            "superficie_suelo"
                        ),
                        porc_suelo_interior=valores.get(
                            "porc_suelo_interior"
                        ),

                        val_suelo=valores.get("val_suelo"),
                        val_construccion_pt=valores.get(
                            "val_construccion_pt"
                        ),
                        val_construccion_pe=valores.get(
                            "val_construccion_pe"
                        ),
                        val_suelos_gar=valores.get(
                            "val_suelos_gar"
                        ),
                        val_construccion_pt_garaje=valores.get(
                            "val_construccion_pt_garaje"
                        ),
                        val_construccion_pe_garaje=valores.get(
                            "val_construccion_pe_garaje"
                        ),
                        val_catastral=valores.get(
                            "val_catastral"
                        ),

                        num_inmuebles_recinto=valores.get(
                            "num_inmuebles_recinto"
                        ),
                        num_garajes_recinto=valores.get(
                            "num_garajes_recinto"
                        ),

                        val_tipo=valores.get("val_tipo"),
                        val_tipo_m2=valores.get("val_tipo_m2"),
                        val_tipo_m2_min=valores.get(
                            "val_tipo_m2_min"
                        ),
                        val_tipo_mostrar=valores.get(
                            "val_tipo_mostrar"
                        ),
                        val_estandar=valores.get(
                            "val_estandar"
                        ),
                        val_estandar_m2=valores.get(
                            "val_estandar_m2"
                        ),
                    )
                )

            lista_dtos.append(
                RecintoValorUrbanoDTO(
                    geometry=geometry,
                    ptipos=ptipos,
                )
            )

        return lista_dtos
