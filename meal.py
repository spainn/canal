from product import Product
from typing import Dict
from typing import List
from nutrient import Nutrient
import pprint

class Meal:
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]

    name: str
    servings: float                 # how many servings this meal is
    products: Dict[Product, float]  # Dict[Proudct, number of grams in the meal]
    total_grams: float = 0.0            # total grams in the entire meal
    total_ml: float = 0.0           # total mLt in entire meal
    serving_size: float             # grams per serving (total_grams / servings)
    #nutrients: List[Nutrient]

    def __init__(self, name, servings, products):    
        self.name = name
        self.servings = float(servings)
        self.products = products
        
        # calculate total grams and serving size
        for product in self.products:
            if product.servingSizeUnit == "g":
                self.total_grams += self.products[product]
            elif product.servingSizeUnit == "mlt":
                self.total_ml += self.products[product]

        #self.total_grams = sum(self.products.values())
        self.serving_size = self.total_grams / self.servings

    #def get_macros_from_grams(self, grams):
    @property
    def total_macros(self):
        total_macros = { macro: 0.0 for macro in self.MACROS }

        for product in self.products:
            product_macros = product.get_macros_from_grams(self.products[product])
            
            for macro in product_macros:
                total_macros[macro] += product_macros[macro]

        #macros = { key: value * (grams/self.total_grams) for key, value in total_macros.items()}

        return total_macros


    def get_macros_from_servings(self, servings: float):
        percent_of_macros = servings/self.servings

        macros = self.total_macros

        return { key: value*percent_of_macros for key, value in self.total_macros.items() }

    def print_details(self, show_products = False):
        """Prints verbose details of the meal."""
        print(self.name + ": " + str(self.total_macros))
        print("\tServings: " + str(self.servings))
        print("\tTotal Grams: " + str(self.total_grams))
        print("\tTotal mLt: " + str(self.total_ml))
        print("\tServing Size: " + str(self.serving_size))
        if show_products:
            print("\tProducts: ", end=""); pprint.pprint(str(self.products))
    
        


# 'protein'
# 'total lipid (fat)'
# 'carbohydrate, by difference'
# 'energy'

# 'fiber, total dietary'
