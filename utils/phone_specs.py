import re
from dataclasses import dataclass

@dataclass
class PhoneSpecs:
    os: str
    diagonal: float
    resolution: str
    ram_gb: float

    @property
    def diagonal_str(self) -> str:
        return f"{self.diagonal:.1f}\""

    @property
    def ram_str(self) -> str:
        return f"{self.ram_gb} ГБ"