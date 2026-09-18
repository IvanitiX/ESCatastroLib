import re
from enum import Enum


class Territorio(Enum):
    """Enumeración de territorios con sistema catastral propio.

    Identifica los diferentes territorios de España que tienen
    sistemas catastrales diferenciados (nacional, forales).
    """
    ESPANA = "espana"
    NAVARRA = "navarra"
    GUIPUZKOA = "gipuzkoa"
    ARABA = "araba"
    BIZKAIA = "bizkaia"
    DESCONOCIDO = "desconocido"


_RC_PATTERNS: list[tuple[Territorio, re.Pattern]] = [
    (Territorio.NAVARRA,   re.compile(r"^31\d{18}$")),
    (Territorio.BIZKAIA,   re.compile(r"^[A-Z]\d{7}[A-Z]$")),
    (Territorio.GUIPUZKOA, re.compile(r"^20\d{18}$")),
    (Territorio.ARABA,     re.compile(r"^01[A-Z0-9]{18}$")),
    (Territorio.ESPANA,    re.compile(r"^[0-9A-ZÑ]{20}$")),
]

_PROVINCIAS_TERRITORIO: dict[str, Territorio] = {
    "Navarra": Territorio.NAVARRA,
    "Nafarroa": Territorio.NAVARRA,
    "Gipuzkoa": Territorio.GUIPUZKOA,
    "Guipúzcoa": Territorio.GUIPUZKOA,
    "GUIPUZKOA": Territorio.GUIPUZKOA,
    "Araba": Territorio.ARABA,
    "Álava": Territorio.ARABA,
    "ARABA": Territorio.ARABA,
    "Bizkaia": Territorio.BIZKAIA,
    "Vizcaya": Territorio.BIZKAIA,
    "BIZKAIA": Territorio.BIZKAIA,
}


def detectar_territorio(rc: str) -> Territorio:
    rc = rc.strip().upper()

    if len(rc) == 9:
        return Territorio.BIZKAIA

    if len(rc) != 20:
        return Territorio.DESCONOCIDO

    if rc.isdigit() and rc.startswith("31"):
        return Territorio.NAVARRA

    if not rc.isdigit():
        return Territorio.ESPANA

    if rc.startswith("20"):
        return Territorio.DESCONOCIDO

    if rc.startswith("01"):
        return Territorio.DESCONOCIDO

    return Territorio.ESPANA


def territorio_por_provincia(nombre: str) -> Territorio:
    return _PROVINCIAS_TERRITORIO.get(nombre, Territorio.ESPANA)
