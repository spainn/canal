import requests
import pprint
from meal import Meal
from product import Product
from nutrient import Nutrient
from typing import Dict
import pickle
from datetime import datetime

class Canal:
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]
    API_KEY = "DEMO_KEY"
    TODAY_FILE = "data/" + datetime.today().strftime('%Y-%m-%d') + ".txt"
    ROUND_PRECISION = 2
    
    def __init__(self):
        # load meals in form dict{name: Meal}
        with open ('meals.pickle', 'rb') as handle:
            self.meals = pickle.load(handle)
# [kcal], [fats], [carbs], [protein]
        with open (self.TODAY_FILE, "r") as handle:
            str_totals = handle.read().strip().split(", ")

        self.todays_macros = dict(zip(self.MACROS, [float(i) for i in str_totals]))

    def add_macros(self, args):
        if args[2] == "-b":
            barcode = args[3]
            product = self._get_product(barcode)

            if args[4] == "-s":
                servings = args[5]
                print("todays_macros: " + str(self.todays_macros))
                self._add_product_by_servings(product, float(servings))


            elif args[4] == "-g":
                grams = args[5]
                self._add_product_by_grams(product, float(grams))

        elif args[2] == "-m":
            # manually add a product as add -m kcal fats carbs protein to daily total
            macros = [float(args[3]), float(args[4]), float(args[5]), float(args[6])]

            i = 0
            for key in self.todays_macros:
                self.todays_macros[key] += macros[i]
                i += 1

        # UNTESTED STILL
        else:
            meal_name = args[2]
            try:
                if args[3] == "-s":
                    servings = float(args[4])
                    self._add_meal_by_servings(meal_name, servings)
                elif args[3] == "-g":
                    grams = float(args[4])
                    self._add_meal_by_grams(meal_name, grams)
                elif args[3] == "-t":
                    self._add_total_meal(meal_name)
            except IndexError:
                self._add_total_meal(meal_name)
            # means args[2] is a name rather than a flag

    def handle_meal_arguments(self, args):
        if args[2] == "create":
            name = args[3]
            servings = args[4]
            
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
                        products.update( {product: value*product.serving_size} )

                    elif s_or_g == "-g":
                        products.update( {product: value} )

            meal = Meal(name=name, servings=servings, products=products)
            self.meals.update( {meal.name: meal} )


            #if args[5] == "-m":
                #self.meals.update( {name: } )


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

    def _add_meal_by_grams(self, meal_name: str, grams: float):
        meal = self.meals[meal_name]
        macros = meal.get_macros_from_grams(grams=grams)

        self.todays_macros = {key: macros[key] + self.todays_macros[key] for key in macros}

    def _add_meal_by_servings(self, meal_name: str, servings: float):
        meal = self.meals[meal_name]
        grams = meal.serving_size * servings
        self._add_meal_by_grams(meal_name=meal_name, grams=grams)

    def _add_total_meal(self, meal_name: str):
        meal = self.meals[meal_name]

        self._add_meal_by_grams(meal_name=meal_name, grams=meal.total_grams) 

    def _add_product_by_grams(self, product: Product, grams: float):
        macros = product.get_macros_from_grams(grams=grams)

        print("macros: " + str(macros))

        self.todays_macros = {key: macros[key] + self.todays_macros[key] for key in macros}

        print("todays_macros: " + str(self.todays_macros))
        # read file with macro/kcal data.
        # date, name (if meal mealname, else null), kcal, fats, carbs, protein

    def _add_product_by_servings(self, product: Product, servings: float):
        self._add_product_by_grams(product, servings*product.serving_size)

        print("_add_product_by_servings: " + str(servings*product.serving_size))

    def _get_product(self, barcode):
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={barcode}&pageSize=10&api_key={self.API_KEY}"
        
        # validate request and barcode
        r = requests.get(url)
        if r.status_code == 200:
            raw_product_data = r.json()
            pprint.pprint(raw_product_data)
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
