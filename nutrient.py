from dataclasses import dataclass

@dataclass(frozen=True)
class Nutrient:
    name: str
    #percentDailyValue: int
    unitName: str
    value: float
