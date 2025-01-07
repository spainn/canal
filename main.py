import requests
import pprint
from product import Product
from nutrient import Nutrient

API_KEY = "DEMO_KEY"
#BARCODE = 850126007120
#BARCODE = 850018774123
BARCODE = "021130409433"

def get_product(barcode):
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={barcode}&pageSize=10&api_key={API_KEY}"

    r = requests.get(url)
    if r.status_code == 200:
        raw_product_data = r.json()
        pprint.pprint(raw_product_data)
    else:
        raise Exception(f"request failed with status code {r.status_code}")
    
    food = raw_product_data['foods'][0]
    nutrients = dict()
    for nutrient in food['foodNutrients']:
        n = Nutrient(name = nutrient['nutrientName'].lower(),
                     #percentDailyValue = nutrient['percentDailyValue'],
                     unitName = nutrient['unitName'].lower(),
                     value = nutrient['value']) 
        nutrients.update({n.name: n})

    product = Product(brandName=food['brandName'].lower(),
                      description=food['description'],
                      servingSize=food['servingSize'],
                      servingSizeUnit=food['servingSizeUnit'].lower(),
                      nutrients=nutrients)
        
         
def main():
    product = get_product(BARCODE)

if __name__ == "__main__":
    main()

"""
potential project structure
data class for a product (barcode, name, etc.)
meal class (consists of many products with serving amounts)
somehow implement custom names (e.g. egg knows large white egg from walmart
    or someting)

"""
