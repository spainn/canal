import requests
import pprint
from product import Product
from nutrient import Nutrient
import pickle
from datetime import datetime



class Canal:
    API_KEY = "DEMO_KEY"
    TODAY = datetime.today().strftime('%Y-%m-%d')
    
    def __init__(self):
        # load meals in form dict{name: Meal}
        with open ('meals.pickle', 'rb') as handle:
            self.meals = pickle.load(handle)

    def get_product(self, barcode):
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

    def add_product_by_grams(self, product: Product, grams: float):
        None
        # read file with macro/kcal data.
        # date, name (if meal mealname, else null), protein, carbs, fats, kcal

    def add_product_by_servings(self, product: Product, servings: float):
        self.add_product_by_grams(product, servings*product.serving_size)
    
    def save_state(self):
        with open("meals.pickle", "wb") as handle:
            pickle.dump(self.meals, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def list_meals(self):
        for meal in self.meals:
            print(meal)
