import sys
from canal import Canal
from parser import Parser
API_KEY = "DEMO_KEY"
BARCODE = "021130409433"

"""
TODO
-add command to view daily macros
-add canal sub functionality where you can also specify meal name, barcode, or manual
 and it subtracts it (just use the add functions but negative somehow?)
-decouple parsing and Canal.  Create Parser class.  Do functionality like creating a meal in main.py
-make sure a daily file exists on program start in main.py or in Canal init
-make canal add [mealname] [-s or -g] [value] work ONLY IN THE CASE THAT the meal has
 one product only
 -COULD change -m flag to -p to represent product instead of manual, which would essentially
  be manually inputting a product, but then use -m to mean meal for creating a meal
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
                canal.add_macros(
                   parser.parse_add_manual()
            )

            else:
                canal.add_macros_by_meal(
                    *parser.parse_add_meal()
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

