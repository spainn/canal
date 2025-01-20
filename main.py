import sys
from canal import Canal
from parser import Parser

"""
TODO
 -refactor product.py to use snake case isntead of camel case across the whole codebase
 -add a command to set the round precision when writing the macros
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
        
def main(): 
    canal = Canal()
    parser = Parser(sys.argv)

    if parser.command == "add":
            if parser.action == "-b":
                canal.add_macros_by_barcode(
                    *parser.parse_add_barcode()
            )

            elif parser.action == "-m":

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

    # list the name of all stored meals and their macronutrients / kcals
    elif parser.command == "list":
        canal.list_meals()

    elif parser.command == "":
        canal.display_todays_macros()

    else:
        canal.display_meal(parser.command)
    
    # save the macros and meals after the command has been processed
    canal.save_state()

if __name__ == "__main__":
    main()

