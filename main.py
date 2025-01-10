import requests
import pprint
import sys
from product import Product
from nutrient import Nutrient
from canal import Canal

API_KEY = "DEMO_KEY"
#BARCODE = 850126007120
#BARCODE = 850018774123
BARCODE = "021130409433"        
         
def main(args = [str]):
    args = sys.argv
    canal = Canal()

    if len(args) == 0:
        # print daily macronutrients and calories
        return
    
    # if args[1] is a barcode (12 digit integer that can start with 0)
    #product = canal.get_product(BARCODE)
    
    if args[1] == "add":
        if args[2] == "-b":
            barcode = args[3]
            product = canal.get_product(barcode)

            if args[4] == "-s":
                servings = args[5]
                canal.add_servings(product, float(servings))

            elif args[4] == "-g":
                grams = args[5]
                canal.add_grams(product, float(grams))



        else:
            mealName = args[2]

            if args[3] == "-s":
                None
            elif args[3] == "-g":
                None
            # means args[2] is a name rather than a flag

    for i in args:
        print(i)

if __name__ == "__main__":
    main()

"""
potential project structure
data class for a product (barcode, name, etc.)
meal class (consists of many products with serving amounts)
somehow implement custom names (e.g. egg knows large white egg from walmart
    or someting)

"""
