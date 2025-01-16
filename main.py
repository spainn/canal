import sys
from canal import Canal

API_KEY = "DEMO_KEY"
BARCODE = "021130409433"

"""
TODO
-add command to view daily macros
-add canal sub functionality where you can also specify meal name, barcode, or manual
 and it subtracts it (just use the add functions but negative somehow?)
-decouple parsing and Canal.  Create Parser class.  Do functionality like creating a meal in main.py
-make sure a daily file exists on program start in main.py or in Canal init
"""
         
def main(args = [str]):
    args = sys.argv
    canal = Canal()

    if len(args) == 0:
        # print daily macronutrients and calories
        return 
    
    command = args[1]
    #action = args[2]

    # MAKE A PARSER CLASS that returns the variables you need to pass to a function in Canal.
    # canal is the tracker that handles tracking stuff
    #
    # parser handles reading arguments in order to get the variables.
    # add a new 
    if command == "add":
       canal.add_macros(args=args)
        #       canal.add_macros(parser.parse_add(args))
    
    elif command == "meal":
       canal.handle_meal_arguments(args=args) 
    # list the name of all stored meals and their macronutrients / kcals
    elif command == "list":
        canal.list_meals()


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

