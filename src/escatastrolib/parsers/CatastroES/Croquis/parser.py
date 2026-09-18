from .dto import CroquisDTO
from ...typing import to_str

class CroquisParser:
    def parse(self, data: str) -> CroquisDTO:
        return self.to_dto(data)
    
    def to_dto(self, data: str) -> CroquisDTO:
        return CroquisDTO(
            url=to_str(data)
        )
