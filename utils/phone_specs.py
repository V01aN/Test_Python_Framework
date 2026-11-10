from dataclasses import dataclass


@dataclass
class PhoneSpecs:
    os: str
    diagonal: float
    resolution: str
    ram_gb: float

    @property
    def diagonal_str(self) -> str:
        from utils.parser import format_screen_size
        return format_screen_size(self.diagonal)

    @property
    def ram_str(self) -> str:
        return f"{self.ram_gb} ГБ"