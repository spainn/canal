import requests
import pprint
from product import Product
from nutrient import Nutrient
import pickle
from datetime import datetime

class Canal:
    API_KEY = "DEMO_KEY"
    TODAY_FILE = datetime.today().strftime('%Y-%m-%d') + ".txt"
    
    def __init__(self):
        # load meals in form dict{name: Meal}
        with open ('meals.pickle', 'rb') as handle:
            self.meals = pickle.load(handle)
# [kcal], [fats], [carbs], [protein]
        with open (f"data/{self.TODAY_FILE}", "r") as handle:
            str_totals = handle.read().strip().split(", ")

        self.todays_macros = [float(i) for i in str_totals]

    def add_macros(self, args):
        if args[2] == "-b":
            barcode = args[3]
            product = self._get_product(barcode)

            if args[4] == "-s":
                servings = args[5]
                self._add_product_by_servings(product, float(servings))

            elif args[4] == "-g":
                grams = args[5]
                self._add_product_by_grams(product, float(grams))

        elif args[2] == "-m":
            None # manually add a product as add -m kcal fats carbs protein to daily total

        else:
            meal_name = args[2]

            if args[3] == "-s":
                servings = args[4]
                self._add_meal_by_servings(meal_name, servings)
            elif args[3] == "-g":
                grams = args[5]
                self._add_meal_by_grams(meal_name, grams)
            # means args[2] is a name rather than a flag
    def handle_meal_arguments(self, args):
        if args[2] == "create":
            name = args[3]
            servings = args[4]

            #if args[5] == "-m":
                #self.meals.update( {name: } )


    def list_meals(self):
        for meal in self.meals:
            print(meal)

    def save_state(self):
        with open("meals.pickle", "wb") as handle:
            pickle.dump(self.meals, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def _add_meal_by_grams(self, meal_name: str, grams: float):
        None

    def _add_meal_by_servings(self, meal_name: str, servings: float):
        meal = self.meals[meal_name]
        grams = meal.serving_size * servings
        self._add_meal_by_grams(meal_name=meal_name, grams=grams)

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
                          nutrients=nutrients)

        return product

    def _add_product_by_grams(self, product: Product, grams: float):
        None
        # read file with macro/kcal data.
        # date, name (if meal mealname, else null), kcal, fats, carbs, protein

    def _add_product_by_servings(self, product: Product, servings: float):
        self._add_product_by_grams(product, servings*product.serving_size)

def main():
    canal = Canal()

if __name__ == "__main__":
    main()
