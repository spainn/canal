from dataclasses import dataclass
from typing import Dict
from nutrient import Nutrient 

@dataclass  #(order=True)
class Product:
    brandName: str
    description: str
    servingSize: float
    servingSizeUnit: str
    nutrients: Dict[str, Nutrient] # per 100g

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
