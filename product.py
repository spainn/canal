from dataclasses import dataclass
from typing import Dict
from nutrient import Nutrient 

"""
raw data retrived for nutrients is first based as per
100g or per 100ml from the branded foods database
from the USDA
"""

@dataclass(frozen=True)  #(order=True)
class Product:
    brandName: str
    description: str
    servingSize: float             # g or mL amount
    servingSizeUnit: str           # g or mL
    nutrients: Dict[str, Nutrient] # per 100g or 100mL

    @property
    def nutrients_per_serving(self):
        """Returns a Dict[str, Nutrient] of each nutrient's
        name and value per serving rather than per 100g."""
        
        nutrients_per_serving = dict()
        for n in self.nutrients:
            newNutrient = self.nutrients[n]
            newNutrient.value = newNutrient.value*(self.servingSize/100)

            nutrients_per_serving.update(
                {n: newNutrient}
            )

        return nutrients_per_serving


"""
nutrientName
percentDailyValue
unitName
valuei
"""
