from product import Product
from typing import Dict
from typing import List
from nutrient import Nutrient
import pprint

class Meal:
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]

    name: str
    products: Dict[Product, float]  # Dict[Proudct, number of grams in the meal]
    total_grams: float = 0.0            # total grams in the entire meal
    total_ml: float = 0.0           # total mLt in entire meal
    
    def __init__(self, name, products):    
        self.name = name 
        self.products = products
        
        # calculate total grams and milliliters
        for product in self.products:
            if product.servingSizeUnit == "g":
                self.total_grams += self.products[product]
            elif product.servingSizeUnit == "mlt":
                self.total_ml += self.products[product]
    
    # total macros the meal contains in dictionary format {energy: kcal, macro: grams}
    @property
    def total_macros(self):
        total_macros = { macro: 0.0 for macro in self.MACROS }

        for product in self.products:
            product_macros = product.get_macros_from_grams(self.products[product])
            
            for macro in product_macros:
                total_macros[macro] += product_macros[macro]

        return total_macros


    def get_macros_from_count(self, count: float):
        return { key: value*count for key, value in self.total_macros.items() }

    def print_details(self, show_products = False):
        """Prints verbose details of the meal."""
        print(self.name + ": " + str(self.total_macros)) 
        print("\tTotal Grams: " + str(self.total_grams))
        print("\tTotal mLt: " + str(self.total_ml))
        if show_products:
            print("\tProducts: ", end=""); pprint.pprint(str(self.products))

