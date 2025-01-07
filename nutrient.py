from dataclasses import dataclass

@dataclass
class Nutrient:
    name: str
    #percentDailyValue: int
    unitName: str
    value: float
