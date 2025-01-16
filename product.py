from dataclasses import dataclass
from typing import Dict
from nutrient import Nutrient
from typing import List

"""
raw data retrived for nutrients is first based as per
100g or per 100ml from the branded foods database
from the USDA
"""

@dataclass(frozen=True)  #(order=True)
class Product:
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]

    brandName: str
    description: str
    serving_size: float             # g or mL amount
    servingSizeUnit: str           # g or mL
    nutrients: tuple[Nutrient, ...] # per 100g or 100mL
    
    def __post_init__(self):
        if isinstance(self.serving_size, str):
            object.__setattr__(self, 'serving_size', float(self.serving_size))

#    @property
#    def nutrients_per_serving(self):
#        """Returns a Dict[str, Nutrient] of each nutrient's
#        name and value per serving rather than per 100g."""
#        
#        nutrients_per_serving = []
#        for n in self.nutrients:
#            new_nutrient = Nutrient(name=n.name, 
#                                    unitName=n.unitName,
#                                    value=n.value*(self.serving_size/100))
#        nutrients_per_serving.append(new_nutrient)
#
#        return nutrients_per_serving

    def get_macros_from_units(self, units):
        macros = dict()   

        for n in self.nutrients:
            if n.name in self.MACROS:
                macros.update( {n.name: n.value * (units/100) } )

        return macros

    def get_macros_from_servings(self, servings):
        grams = servings*self.serving_size

        return self.get_macros_from_grams(grams=grams)
"""
nutrientName
percentDailyValue
unitName
valuei
"""
