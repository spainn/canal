from dataclasses import dataclass

@dataclass(frozen=True)
class Nutrient:
    name: str
    unitName: str
    value: float
    
    # verify value is a float
    def __post_init__(self):
        if isinstance(self.value, str):
            object.__setattr__(self, 'value', float(self.value))
