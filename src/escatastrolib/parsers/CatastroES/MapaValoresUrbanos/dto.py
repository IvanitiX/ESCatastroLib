

from dataclasses import dataclass
from datetime import datetime

from typing import Any

@dataclass
class ValorUrbanoDTO:
    # Identificación
    id_producto_tipo: str | None = None
    id_delegacion: str | None = None
    id_municipio: str | None = None
    fecha: datetime | None = None
    id_recinto_valoracion: str | None = None
    orden: int | None = None
    num_inmueble: int | None = None

    # Características del inmueble
    codigo_uso: str | None = None
    tipologia: str | None = None
    coef_propiedad: float | None = None
    categoria: str | None = None
    antiguedad: int | None = None
    conservacion: str | None = None
    superficie: float | None = None
    tipologia_anejos: str | None = None
    edificabilidad: float | None = None
    num_altura: int | None = None
    superficie_minima: float | None = None
    superficie_suelo: float | None = None
    porc_suelo_interior: float | None = None

    # Valores económicos
    val_suelo: float | None = None
    val_construccion_pt: float | None = None
    val_construccion_pe: float | None = None
    val_suelos_gar: float | None = None
    val_construccion_pt_garaje: float | None = None
    val_construccion_pe_garaje: float | None = None
    val_catastral: float | None = None

    # Datos agregados del recinto
    num_inmuebles_recinto: int | None = None
    num_garajes_recinto: int | None = None

    # Valores del tipo y del estándar
    val_tipo: float | None = None
    val_tipo_m2: float | None = None
    val_tipo_m2_min: float | None = None
    val_tipo_mostrar: str | None = None
    val_estandar: float | None = None
    val_estandar_m2: float | None = None

@dataclass
class RecintoValorUrbanoDTO:
    ptipos: list[ValorUrbanoDTO]
    geometry: dict[str, Any] | None = None
