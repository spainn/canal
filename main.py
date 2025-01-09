import requests
import pprint
from product import Product
from nutrient import Nutrient
from canal import Canal

API_KEY = "DEMO_KEY"
#BARCODE = 850126007120
#BARCODE = 850018774123
BARCODE = "021130409433"        
         
def main(args = [str]):
    canal = Canal()

    if len(args) == 0:
        # print daily macronutrients and calories
        return
    
    # if args[0] is a barcode (12 digit integer that can start with 0)
    product = canal.get_product(BARCODE)

if __name__ == "__main__":
    main()

"""
potential project structure
data class for a product (barcode, name, etc.)
meal class (consists of many products with serving amounts)
somehow implement custom names (e.g. egg knows large white egg from walmart
    or someting)

"""
