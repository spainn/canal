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

"""
TODO
-maek add_product methods and get_product methods private in Canal(), then write functions
 for each set of arguments, then pass those arguments to canal
-make a create_meal method
-make a create_meal_manual method
-write the add product method
-
"""
         
def main(args = [str]):
    args = sys.argv
    canal = Canal()

    if len(args) == 0:
        # print daily macronutrients and calories
        return
    
    # if args[1] is a barcode (12 digit integer that can start with 0)
    #product = canal.get_product(BARCODE)
    
    # add a new 
    if args[1] == "add":
        if args[2] == "-b":
            barcode = args[3]
            product = canal.get_product(barcode)

            if args[4] == "-s":
                servings = args[5]
                canal.add_product_by_servings(product, float(servings))

            elif args[4] == "-g":
                grams = args[5]
                canal.add_product_by_grams(product, float(grams))

        elif args[2] == "-m":
            None # manually add a product as add -m kcal fats carbs protein to daily total

        else:
            mealName = args[2]

            if args[3] == "-s":
                servings = args[4]
            elif args[3] == "-g":
                grams = args[5]
            # means args[2] is a name rather than a flag
    
    # list the name of all stored meals and their macronutrients / kcals
    elif args[1] == "list":
        canal.list_meals()

    elif args[1] == "meal":
        if args[2] == "create":
            name = args[3]
            servings = args[4]

            if args[5] == "-m":
                canal.meals.update( {name: } )
# args[1] == meal
    # meal create [name] [servings] [barcode] [-s or -g] [value] ... [barcode] [-s or -g] [value]
    # meal create [name] [servings] [serving_size] -m [kcal] [fat] [carbs] [protein]
    #for i in args:
        #print(i)
    
    # save the meal dictionary
    canal.save_state()

if __name__ == "__main__":
    main()

"""
potential project structure
data class for a product (barcode, name, etc.)
meal class (consists of many products with serving amounts)
somehow implement custom names (e.g. egg knows large white egg from walmart
    or someting)

"""
