from dataclasses import dataclass
from nutrient import Nutrient

"""
raw data retrived for nutrients is first based as per
100g or per 100ml from the branded foods database
from the USDA
"""

@dataclass(frozen=True)  #(order=True)
class Product:
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]

    brand_name: str
    description: str
    serving_size: float             # g or mLt amount
    serving_size_unit: str            # g or mLt
    nutrients: tuple[Nutrient, ...] # per 100g or 100mLt
    
    def __post_init__(self):
        if isinstance(self.serving_size, str):
            object.__setattr__(self, 'serving_size', float(self.serving_size))
    
    def get_macros_from_units(self, units):
        macros = dict()   

        for n in self.nutrients:
            if n.name in self.MACROS:
                macros.update( {n.name: n.value * (units/100) } )

        return macros

