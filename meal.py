from product import Product
from typing import Dict
from typing import List
from nutrient import Nutrient

class Meal:
    MACROS = ["energy", "total lipid (fat)", "carbogydrate, by difference", "protein"]

    name: str
    servings: float                 # how many servings this meal is
    products: Dict[Product, float]  # Dict[Proudct, number of grams in the meal]
    total_grams: float              # total grams in the entire meal
    serving_size: float             # grams per serving (total_grams / servings)
    #nutrients: List[Nutrient]

    def __init__(self, name, servings, products):    
        self.name = name
        self.servings = servings
        self.products = products
        
        # calculate total grams and serving size
        self.total_grams = sum(self.products.values())
        self.serving_size = self.total_grams / self.servings

    def get_macros_from_grams(self, grams):
        total_macros = { macro: 0.0 for macro in self.MACROS }

        for product in self.products:
            product_macros = product.get_macros_from_grams(self.products[product])
            
            for macro in product_macros:
                total_macros[macro] += product_macros[macro]

        macros = { key: value * (grams/self.total_grams) for key, value in total_macros.items()}

        return macros



    def get_macros_from_servings(self, servings):
        grams = servings*self.serving_size

        return self.get_macros_from_grams(grams=grams)

    
        


# 'protein'
# 'total lipid (fat)'
# 'carbohydrate, by difference'
# 'energy'

# 'fiber, total dietary'
