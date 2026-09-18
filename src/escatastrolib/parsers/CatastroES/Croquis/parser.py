from .dto import CroquisDTO
from ...typing import to_str

class CroquisParser:
    """Parser para URLs de croquis de parcelas catastrales.

    Convierte las URLs obtenidas del servicio de croquis del Catastro
    en DTOs con la información del croquis.
    """
    def parse(self, data: str) -> CroquisDTO:
        return self.to_dto(data)
    
    def to_dto(self, data: str) -> CroquisDTO:
        return CroquisDTO(
            url=to_str(data)
        )
