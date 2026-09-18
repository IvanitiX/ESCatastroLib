from dataclasses import dataclass

from ...common.dtos_geometria import GeometriaDTO, PuntoDTO

@dataclass
class INSPIREParcelDTO:
    geometria: GeometriaDTO
    centroide: GeometriaDTO
    area: float