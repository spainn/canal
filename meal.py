from product import Product
from typing import Dict

class Meal:
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]

    name: str
    products: Dict[Product, float]  # Dict[Proudct, number of grams in the meal]
    total_grams: float = 0.0            # total grams in the entire meal
    total_ml: float = 0.0           # total mLt in entire meal
    one_product: bool = False
    
    def __init__(self, name, products):    
        self.name = name 
        self.products = products
        
        # calculate total grams and milliliters
        for product in self.products:
            if product.servingSizeUnit == "g":
                self.total_grams += self.products[product]
            elif product.servingSizeUnit == "mlt":
                self.total_ml += self.products[product]

        if len(self.products) == 1:
            self.one_product = True
    
    # total macros the meal contains in dictionary format {energy: kcal, macro: grams}
    @property
    def total_macros(self):
        total_macros = { macro: 0.0 for macro in self.MACROS }

        for product in self.products:
            product_macros = product.get_macros_from_units(self.products[product])
            
            for macro in product_macros:
                total_macros[macro] += product_macros[macro]

        return total_macros


    def get_macros_from_count(self, count: float):
        return { key: value*count for key, value in self.total_macros.items() }

    def print_details(self):
        """Prints verbose details of a meal."""
        print("\nName: " + self.name)
        print("Total Grams: " + str(self.total_grams))
        print("Total Milliliters: " + str(self.total_ml))
        print("PRODUCTS:")
        for p in self.products:
            print("\tBrand Name: " + p.brand_name)
            print("\tDescription: " + p.description)

            macros = p.get_macros_from_units(self.products[p])
            
            print("\t\tMACRONUTRIENTS")
            for m in macros:
                print("\t\t\t" + m + ": " + str(macros[m]))

            print("\t\tALL NUTRIENTS")
            for n in p.nutrients:
                print("\t\t\t" + str(n.name) + ": " + str(n.value*self.products[p]/100))

            print()


