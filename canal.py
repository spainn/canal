import requests
from meal import Meal
from product import Product
from nutrient import Nutrient
from typing import Dict
import pickle
from datetime import datetime

class Canal:
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]
    UNITS = ["kcal", "g", "g", "g"]
    API_KEY = "DEMO_KEY"
    TODAY_FILE = "data/" + datetime.today().strftime('%Y-%m-%d') + ".txt"
    ROUND_PRECISION = 1
    
    def __init__(self):
        # load meals in form dict{name: Meal}
        with open ('meals.pickle', 'rb') as handle:
            self.meals = pickle.load(handle)
# [kcal], [fats], [carbs], [protein]
        with open (self.TODAY_FILE, "r") as handle:
            str_totals = handle.read().strip().split(", ")

        self.todays_macros = dict(zip(self.MACROS, [float(i) for i in str_totals]))
    
    def add_macros_by_barcode(self, barcode, is_servings, count):
        product = self._get_product(barcode)
        if is_servings:
            self._add_product_by_units(product, count*product.serving_size)

    def add_macros(self, macros: list[float]):
            i = 0
            for key in self.todays_macros:
                self.todays_macros[key] += macros[i]

    def add_macros_by_meal(self, meal_name, count):
        meal = self.meals[meal_name]
        macros = meal.get_macros_from_count(count=count)

        self.todays_macros = {key: macros[key] + self.todays_macros[key] for key in macros.keys()}        

    def handle_meal_arguments(self, args):
        FLAGS = ["-b", "-m", "-meal"]
        if args[2] == "create":
            name = args[3] 
            
            flags = []  # list in format [flag, index, flag, index ...]
            for i in range(0, len(args)):
                if args[i] == "-b" or args[i] == "-m" or args[i] == "-meal":
                    flags.append(args[i])
                    flags.append(i)

            print("FLAGS: " + str(flags))
           
            products: Dict[Product, float] = dict()
            for i in range(0, len(flags), 2):
                flag_index = flags[i+1]

                if flags[i] == "-b":
                    barcode = args[flag_index+1]
                    s_or_g = args[flag_index+2]
                    value = float(args[flag_index+3])

                    #print("BAR, S_OR_G, VALUE: " + str(barcode) + str(s_or_g) + str(value) + str(type(value)))
                    
                    product = self._get_product(barcode=barcode)

                    if s_or_g == "-s":
                        if product in products:
                            products[product] += value*product.serving_size
                        else:
                            products.update( {product: value*product.serving_size} )

                    elif s_or_g == "-g":
                        if product in products:
                            products[product] += value
                        else:
                            products.update( {product: value} )

                elif flags[i] == "-m":
                    total_units = float(args[flag_index+1]) 
                    
                    # list of values in the same order as self.MACROS
                    values=[args[flag_index+2], # energy
                            args[flag_index+3], # fat
                            args[flag_index+4], # carbs
                            args[flag_index+5]] # protein

                    values = [float(value) for value in values]

                    # name, unitName, value: str, str, float
                    # take value*(100/total_grams) to format the nutrient values
                    #   by nutrients / 100 grams
                    nutrients = tuple(Nutrient(name, unit_name, value*(100/total_units))
                        for name, unit_name, value in zip(self.MACROS, self.UNITS, values))
                    
                    # create a filler product to hold the manually inputted macros
                    product = Product(brandName="",
                                      description="",
                                      serving_size=0.0,
                                      servingSizeUnit="g",
                                      nutrients=nutrients)
                    
                    if product in products:
                        products[product] += total_units
                    else:
                        products.update( {product: total_units} )

                    print(products)

                elif flags[i] == "-meal":
                    meal_to_add_name = args[flag_index+1]
                    count = float(args[flag_index+2])
                    
                    meal = self.meals[meal_to_add_name] 

                    for product in meal.products:
                        if product in products:
                            products[product] += meal.products[product]*count
                        else:
                            products.update( {product: meal.products[product]*count })


            meal = Meal(name=name, products=products)
            self.meals.update( {meal.name: meal} )
        
        # TESTED delete a meal
        elif args[2] == "rm":
            del self.meals[args[3]]
        
    def list_meals(self):
        for meal in self.meals:
            print(meal)

    def save_state(self):
        with open("meals.pickle", "wb") as handle:
            pickle.dump(self.meals, handle, protocol=pickle.HIGHEST_PROTOCOL)
       
        # round to 2 decimal places before write
        self.todays_macros = {key: round(value, self.ROUND_PRECISION) for key, value in self.todays_macros.items() }

        macro_data = ""

        for macro in self.MACROS[:-1]:
            macro_data += str(self.todays_macros[macro]) + ", "

        macro_data += str(self.todays_macros[self.MACROS[-1]]) + "\n" 
        
        with open(self.TODAY_FILE, "w") as handle:
            handle.write(macro_data) 

#    def _add_meal_by_count(self, meal_name: str, count: float):
#        meal = self.meals[meal_name]
#        macros = meal.get_macros_from_count(count=count)
#
#        self.todays_macros = {key: macros[key] + self.todays_macros[key] for key in macros.keys()}

    def _add_product_by_units(self, product: Product, units: float):
        macros = product.get_macros_from_units(units=units)
        self.todays_macros = {key: macros[key] + self.todays_macros[key] for key in macros}

    #def _add_product_by_servings(self, product: Product, servings: float):
    #    self._add_product_by_units(product, servings*product.serving_size) 

    def _get_product(self, barcode):
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={barcode}&pageSize=10&api_key={self.API_KEY}"
        
        # validate request and barcode
        r = requests.get(url)
        if r.status_code == 200:
            raw_product_data = r.json()
         #   pprint.pprint(raw_product_data)
        else:
            raise Exception(f"request failed with status code {r.status_code}")

        if raw_product_data['foods'] == []:
            raise Exception(f"Barcode {barcode} invalid.  Could not find any foods.")

        # create product
        food = raw_product_data['foods'][0]
        nutrients = []
        for nutrient in food['foodNutrients']:
            n = Nutrient(name = nutrient['nutrientName'].lower(),
                         #percentDailyValue = nutrient['percentDailyValue'],
                         unitName = nutrient['unitName'].lower(),
                         value = nutrient['value']) 
            nutrients.append(n)
        product = Product(brandName=food['brandName'].lower(),
                          description=food['description'],
                          serving_size=food['servingSize'],
                          servingSizeUnit=food['servingSizeUnit'].lower(),
                          nutrients=tuple(nutrients))

        return product

def main():
    canal = Canal()

if __name__ == "__main__":
    main()
