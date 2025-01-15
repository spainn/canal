from dataclasses import dataclass

@dataclass(frozen=True)
class Nutrient:
    name: str
    #percentDailyValue: int
    unitName: str
    value: float

    def __post_init__(self):
        if isinstance(self.value, str):
            object.__setattr__(self, 'value', float(self.value))
