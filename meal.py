from product import Product
from typing import Dict
from typing import List
from nutrient import Nutrient

class Meal:
    name: str
    servings: float
    products: Dict[Product, float]  # Dict[Proudct, number of grams in the meal]
    total_grams: float
    serving_size: float
    nutrients: List[Nutrient]

    def __init__(self, name, servings, products):    
        self.name = name
        self.servings = servings
        self.products = products
        
        # calculate total grams and serving size
        self.total_grams = sum(self.products.values())
        self.serving_size = self.total_grams / self.servings

        # calculate nutrients per 100g
        nutrients = dict()
        for product in products:
            for nutrient in product.nutrients:
                if nutrient.name in nutrients:
                    nutrients[nutrient.name].value += nutrient.value
                else:
                    nutrients[nutrient.name] = nutrient

        self.nutrients = list(nutrients.values())

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

    def get_macros_from_servings(self, servings):

    
        


# 'protein'
# 'total lipid (fat)'
# 'carbohydrate, by difference'
# 'energy'

# 'fiber, total dietary'
