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
    brandName: str
    description: str
    serving_size: float             # g or mL amount
    servingSizeUnit: str           # g or mL
    nutrients: List[Nutrient] # per 100g or 100mL

    @property
    def nutrients_per_serving(self):
        """Returns a Dict[str, Nutrient] of each nutrient's
        name and value per serving rather than per 100g."""
        
        nutrients_per_serving = []
        for n in self.nutrients:
            new_nutrient = n
            new_nutrient.value = new_nutrient.value*(self.serving_size/100)
            nutrients_per_serving.append(new_nutrient)

        return nutrients_per_serving

    def get_macros_from_grams(self, grams):
        macros = dict()
        
        macros.update( {"protein": self.nutrients["protein"].value * (grams/100)} )
        macros.update( {"fats": self.nutrients["total lipid (fat)"].value * (grams/100)} )
        macros.update( {"carbs": self.nutrients["carbohydrate, by difference"].value * (grams/100)} )
        macros.update( {"kcals": self.nutrients["energy"].value * (grams/100)} )

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
