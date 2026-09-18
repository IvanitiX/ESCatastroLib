from dataclasses import dataclass

@dataclass
class CentroideDTO:
    x: float
    y: float
    sr: int

@dataclass
class RefCatDTO:
    rc: str