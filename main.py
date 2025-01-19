import sys
from canal import Canal
from parser import Parser
API_KEY = "DEMO_KEY"
BARCODE = "021130409433"

# milk barcode
# 078742351896
"""
TODO
-make canal add [mealname] [-s or -u] [value] work ONLY IN THE CASE THAT the meal has
 one product only
 -refactor product.py to use snake case isntead of camel case across the whole codebase
"""

"""
canal meal create [name] -p [product_name] [total_units] [kcal] [fats] [carbs] [proteins]
canal meal create [name] -b [barcode] [-s or -u] [count]
canal meal create [name] -m [meal_name] [count]

canal add [kcal] [fat] [carbs] [protein]
canal add -m [meal_name] [count]
canal add -m [meal_name] [-s or -u] [count]
canal add -b [barcode] [-s or -u] [count]

canal list

"""

"""
NEEDS TESTED
-meal create
    in particular when -meal egg 2 and -meal egg 3 are used or something similar
    where the overlap addition is tested
-

TESTED
-add -m
-add MANUAL INPUT (4 floats)
-add -b
"""
         
def main(): 
    canal = Canal()
    parser = Parser(sys.argv)

    # MAKE A PARSER CLASS that returns the variables you need to pass to a function in Canal.
    # canal is the tracker that handles tracking stuff
    #
    # parser handles reading arguments in order to get the variables.
    # add a new 
    if parser.command == "add":
            if parser.action == "-b":
                canal.add_macros_by_barcode(
                    *parser.parse_add_barcode()
            )

            elif parser.action == "-m":
                # is_servings is None if no -s or -u flags were passed

                meal_name, count, is_servings = parser.parse_add_meal()
                if is_servings == None:
                    canal.add_macros_by_meal(meal_name, count)
                else:
                    canal.add_macros_product_meal(meal_name, count, is_servings)
            

            else:
                canal.add_macros(
                   parser.parse_add_manual()
            )
    
    elif parser.command == "meal":
        if parser.action == "create":
            canal.create_meal(
                *parser.parse_meal_create()
            )
        elif parser.action == "rm":
            canal.remove_meal(
                parser.parse_meal_remove()
            )

        else:
            canal.display_meal(parser.action)

        #canal.handle_meal_arguments(args=args) 

    # list the name of all stored meals and their macronutrients / kcals
    elif parser.command == "list":
        canal.list_meals()
            #canal.list_meals()
    elif parser.command == "":
        canal.display_todays_macros()

    else:
        canal.display_meal(parser.command)

# command == meal
    # meal create [name] -b [barcode] [-s or -g] [value] ... [barcode] [-s or -g] [value]
    
    # NEED TOTAL GRAMS IN EXAMPLE BELOW so that we can calculate a total macros of a meal
    #     based on how much of that product is in the meal (the total grams)
    # meal create [name] -m [grams in meal (weight total)] [kcal] [fat] [carbs] [protein] ... -m ...
    # meal create [name] -meal [meal_to_add's name] [count]
    
    # save the meal dictionary and daily macro totals
    canal.save_state()

if __name__ == "__main__":
    main()

