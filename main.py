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
    
    # add a new 
    if args[1] == "add":
       canal.add_macros(args=args) 
    
    elif args[1] == "meal":
       canal.handle_meal_arguments(args=args) 
    # list the name of all stored meals and their macronutrients / kcals
    elif args[1] == "list":
        canal.list_meals()

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
