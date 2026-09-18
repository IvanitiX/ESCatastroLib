import json
import re
from typing import Any

import requests

from .dto import CartoCiudadDTO
from ...typing import (
    to_bool,
    to_float,
    to_int,
    to_str,
)


class CartoCiudadParser:
    """
    Convierte respuestas JSON/JSONP de CartoCiudad
    en objetos CartoCiudadDTO.
    """

    def parse(self, response: requests.Response) -> CartoCiudadDTO | None:
        response.raise_for_status()

        data = self._parse_jsonp(response.text)

        if not data:
            return None

        if not isinstance(data, dict):
            raise ValueError(
                "La respuesta de CartoCiudad no tiene "
                "el formato esperado"
            )

        return self._to_dto(data)

    @staticmethod
    def _parse_jsonp(content: str) -> Any:
        """
        Convierte una respuesta JSON o JSONP a un objeto Python.
        """

        content = content.strip()

        if not content:
            return None

        # JSON puro
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # JSONP: callback({...});
        match = re.match(
            r"^[^(]+\((.*)\)\s*;?\s*$",
            content,
            flags=re.DOTALL,
        )

        if not match:
            raise ValueError(
                "La respuesta de CartoCiudad no es "
                "JSON ni JSONP válido"
            )

        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as error:
            raise ValueError(
                "No se pudo decodificar el JSON de CartoCiudad"
            ) from error

    def _to_dto(self, data: dict[str, Any]) -> CartoCiudadDTO:
        """
        Mapea las claves de CartoCiudad al DTO interno.
        """

        return CartoCiudadDTO(
            id=to_str(data.get("id")),
            provincia=to_str(data.get("province")),
            comunidad_autonoma=to_str(
                data.get("comunidadAutonoma")
            ),
            municipio=to_str(data.get("muni")),
            direccion=to_str(data.get("address")),
            codigo_postal=to_str(
                data.get("postalCode")
            ),
            longitud=to_float(data.get("lng")),
            latitud=to_float(data.get("lat")),
            numero=to_int(data.get("portalNumber")),
            sin_numero=to_bool(data.get("sinNumero")),
            extension=to_bool(data.get("extension")),
            referencia_catastral=to_str(
                data.get("refCatastral")
            ),
        )