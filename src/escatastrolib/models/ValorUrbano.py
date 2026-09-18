from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValorUrbano:
    """Valoración de suelo urbano procedente del Mapa de Valores del Catastro.

    Attributes:
        tipologia: Tipo de construcción (ej. "Vivienda", "Local comercial").
        superficie: Superficie del suelo en m².
        val_suelo: Valor del suelo en euros.
        val_construccion: Valor de la construcción en euros.
        val_catastral: Valor catastral total en euros.
        val_tipo_m2: Valor por metro cuadrado en euros.
    """

    tipologia: str | None = None
    superficie: float | None = None
    val_suelo: float | None = None
    val_construccion: float | None = None
    val_catastral: float | None = None
    val_tipo_m2: float | None = None
