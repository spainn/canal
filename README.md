simple calorie tracker for tracking macronutrients and calories

Data in daily .txt files structured in format:
[kcal], [fats], [carbs], [protein]

where fats, carbs, and protein are in grams

COMMANDS

canal meal create [name] -p [product_name] [total_units] [kcal] [fats] [carbs] [proteins]
canal meal create [name] -b [barcode] [-s or -u] [count]
canal meal create [name] -m [meal_name] [count]

canal add [kcal] [fat] [carbs] [protein]
canal add -m [meal_name] [count]
canal add -m [meal_name] [-s or -u] [count]         IF only 1 product in the meal
canal add -b [barcode] [-s or -u] [count]

canal list

You can string together -p, -b, and -m flags to create meals with many Products.
You can then add these meals macros using the add command.
-s and -u indicate servings or units.  units are always grams or milliliters
    depending on the item