import requests
from meal import Meal
from product import Product
from nutrient import Nutrient
from typing import Dict
import pickle
from datetime import datetime
import os

class Canal:
    MACROS = ["energy", "total lipid (fat)", "carbohydrate, by difference", "protein"]
    UNITS = ["kcal", "g", "g", "g"]
    API_KEY = "DEMO_KEY"
    TODAY_FILE = "data/" + datetime.today().strftime('%Y-%m-%d') + ".txt"
    PICKLE_FILE = "data/" + "meals.pickle"
    ROUND_PRECISION = 2
    
    def __init__(self):
        # create daily file if it doesn't exist
        if not os.path.exists(self.TODAY_FILE):
            with open(self.TODAY_FILE, "w") as handle:
                handle.write("0.0, 0.0, 0.0, 0.0")

        # create meals file if it doesn't exst
        if not os.path.exists(self.PICKLE_FILE):
            with open(self.PICKLE_FILE, "wb") as handle:
                pickle.dump(dict(), handle, protocol=pickle.HIGHEST_PROTOCOL)

        # load meals in form dict{name: Meal}
        with open (self.PICKLE_FILE, 'rb') as handle:
            self.meals = pickle.load(handle)

        # [kcal], [fats], [carbs], [protein]
        with open (self.TODAY_FILE, "r") as handle:
            str_totals = handle.read().strip().split(", ")

        self.todays_macros = dict(zip(self.MACROS, [float(i) for i in str_totals]))
    
    def add_macros(self, macros: Dict[str, float]):
        for key, value in macros.items():
            self.todays_macros[key] += value

    def add_macros_by_barcode(self, barcode, is_servings, count):
        product = self._get_product(barcode)
        if is_servings:
            macros = product.get_macros_from_units(units=count*product.serving_size)
        else:
            macros = product.get_macros_from_units(units=count)

        self.add_macros(macros)

    def add_macros_by_meal(self, meal_name, count):
        meal = self.meals[meal_name]
        macros = meal.get_macros_from_count(count=count)
      
        self.add_macros(macros)

    def add_macros_product_meal(self, meal_name, count, is_servings):
        meal = self.meals[meal_name]
        if meal.one_product == False:
            raise Exception(f"The meal '{meal}' consists of more than 1 Product, so it can not " +
                             "be added with '-s' or '-u' flags.")

        product = next(iter(meal.products.keys()))
        if is_servings:
            macros = product.get_macros_from_units(units=count*product.serving_size)
        else:
            macros = product.get_macros_from_units(units=count)

        self.add_macros(macros)

    def create_meal(self, meal_name, barcodes, manuals, meals):
        products = dict()
        
        # generate list of products
        for b in barcodes:
            p = self._get_product(b[0])
            is_servings = b[1]
            count = b[2] if not is_servings else b[2]*p.serving_size 

            products[p] = products.get(p, 0.0) + count

        for m in manuals:
            # total_grams, kcal, fats, carbs, proteins
            product_name, total_units, kcal, fats, carbs, proteins = m[0], m[1], m[2], m[3], m[4], m[5]
            
            # ratio for calculating correct nutrients / 100 units as the nutrients list requires
            ratio = 100/total_units
            nutrients = (Nutrient(self.MACROS[0], "kcal", kcal*ratio),
                         Nutrient(self.MACROS[1], "g", fats*ratio),
                         Nutrient(self.MACROS[2], "g", carbs*ratio),
                         Nutrient(self.MACROS[3], "g", proteins*ratio))

            p = Product(product_name, "", total_units, "unknown", nutrients)

            products[p] = products.get(p, 0.0) + total_units

        for m in meals:
            meal = self.meals[m[0]]
            count = m[1]

            for p in meal.products:
                products[p] = products.get(p, 0.0) + meal.products[p]*count

        # create meal from dictionary of products
        meal = Meal(meal_name, products)
        self.meals.update( {meal_name: meal} )

    def remove_meal(self, meal_name):
            del self.meals[meal_name]
        
    def list_meals(self):
        for meal in self.meals:
            print(meal)

    def display_meal(self, meal_name: str):
        self.meals[meal_name].print_details()

    def display_todays_macros(self):
        display_strings = ["calories", "fats", "carbs", "protein"]
        macros = zip(display_strings, self.todays_macros.values(), self.UNITS)
        print()
        print(f"{'Macro':<14} | {'Amount':>10}")
        print("-"*33)
        for key, value, unit in macros:
            print(f" {key:<13} | {value:>10.2f}" + " " + unit)
        print("-"*33)

    def save_state(self):
        with open(self.PICKLE_FILE, "wb") as handle:
            pickle.dump(self.meals, handle, protocol=pickle.HIGHEST_PROTOCOL)
       
        # round to 2 decimal places before write
        self.todays_macros = {key: round(value, self.ROUND_PRECISION) for key, value in self.todays_macros.items() }

        macro_data = ""

        for macro in self.MACROS[:-1]:
            macro_data += str(self.todays_macros[macro]) + ", "

        macro_data += str(self.todays_macros[self.MACROS[-1]]) + "\n" 
        
        with open(self.TODAY_FILE, "w") as handle:
            handle.write(macro_data) 

    def _get_product(self, barcode):
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={barcode}&pageSize=10&api_key={self.API_KEY}"
        
        # validate request and barcode
        r = requests.get(url)
        if r.status_code == 200:
            raw_product_data = r.json()
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
        product = Product(brand_name=food['brandName'].lower(),
                          description=food['description'],
                          serving_size=food['servingSize'],
                          serving_size_unit=food['servingSizeUnit'].lower(),
                          nutrients=tuple(nutrients))

        return product

def main():
    canal = Canal()

if __name__ == "__main__":
    main()
