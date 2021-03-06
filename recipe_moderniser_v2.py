# Recipe Moderniser v2 - Zarah Ayers

# import modules to be used...
import csv
import re

# --- Functions ---


# Not Blank function goes here
def not_blank(question, error_msg, num_ok):
    error = error_msg

    valid = False
    while not valid:
        response = input(question)
        has_errors = ""

        if num_ok != "yes":
            # look at each character in string and if it's a number, complain
            for letter in response:
                if letter.isdigit() == True:
                    has_errors = "yes"
                    break

        if response == "":
            print(error)
            continue

        elif has_errors != "":
            print(error)
            continue

        else:
            return response


# Number Checking Function goes here
def num_check(question):

    error = "Please enter a number that is more than zero"

    valid = False
    while not valid:
        try:
            response = float(input(question))

            if response <= 0:
                print(error)
            else:
                return response

        except ValueError:
            print(error)


def get_sf():
    serving_size = num_check("What is the recipe serving size? ")

    dodgy_sf = "yes"
    while dodgy_sf == "yes":

        desired_size = num_check("How many servings are needed? ")

        scale_factor = desired_size / serving_size

        if scale_factor < 0.25:
            dodgy_sf = input("Warning: This scale factor is very small and you "
                             "might struggle to accurately weigh the ingredients. \n"
                             "Do you want to fix this and make more servings? ").lower

        elif scale_factor > 4:
            dodgy_sf = input("Warning: This scale factor is quite large - you might "
                             "have issues with mixing bowl volumes and oven space \n"
                             "Do you want to fix this a make a smaller batch? ").lower

        else:
            dodgy_sf = "no"

    return scale_factor


def get_all_ingredients():
    all_ingredients = []

    stop = ""
    print("Please enter measurements, units and ingredients one line at a time. "
          "Type 'xxx' when you are done.")
    while stop != "xxx":

        # Ask user for ingredient (via not blank function)
        get_recipe_line = not_blank("Recipe Line (or 'xxx' to quit): ",
                                   "This can't be blank",
                                   "yes")

        # If exit code is typed and there are more than 2 ingredients
        if get_recipe_line.lower() == "xxx" and len(all_ingredients) > 1:
            break

        elif get_recipe_line.lower() == "xxx" and len(all_ingredients) < 2:
            print("You need at least two more ingredients in the list. "
                  "Please add more ingredients.")

        # If exit code is not entered, add ingredients to list
        else:
            all_ingredients.append(get_recipe_line)

    return all_ingredients


def general_converter(how_much, lookup, dictionary, conversion_factor):
    # if unit is in dictionary, convert to mL
    if lookup in dictionary:
        mult_by = dictionary.get(lookup)
        how_much = how_much * float(mult_by) / conversion_factor
        converted = "yes"
    else:
        converted = "no"

    return [how_much, converted]


def unit_checker(raw_unit):

    unit_tocheck = raw_unit

    # Abbreviation lists
    teaspoon = ["tsp", "teaspoon", "t", "teaspoons"]
    tablespoon = ["tbs", "tablespoon", "T", "tbsp", "tablespoons"]
    cup = ["cup", "c", "cups"]
    ounce = ["oz", "ounces", "fl oz", "ounce"]
    pint = ["p", "pt", "fl pt", "pint", "pints"]
    quart = ["q", "qt", "fl qt", "quart", "quarts"]
    mls = ["ml", "milliliter", "millilitre", "milliliters", "millilitres"]
    litre = ["litre", "liter", "l", "litres", "liters"]
    pound = ["pound", "lb", "#", "pounds"]
    grams = ["g", "gram", "grams"]

    if unit_tocheck == "":
        return unit_tocheck
    elif unit_tocheck.lower() in grams:
        return "g"
    elif unit_tocheck == "T" or unit_tocheck.lower() in tablespoon:
        return "tbs"
    elif unit_tocheck.lower() in teaspoon:
        return "tsp"
    elif unit_tocheck.lower() in cup:
        return "cup"
    elif unit_tocheck.lower() in ounce:
        return "ounce"
    elif unit_tocheck.lower() in pint:
        return "pint"
    elif unit_tocheck.lower() in quart:
        return "quart"
    elif unit_tocheck.lower() in mls:
        return "mls"
    elif unit_tocheck.lower() in litre:
        return "litre"
    elif unit_tocheck.lower() in pound:
        return "pound"


# rounder function
def rounding(rounder):

    # Round amount needed
    if rounder % 1 == 0:
        rounder = int(rounder)
    elif rounder * 10 % 1 == 0:
        rounder = "{:.1f}".format(rounder)
    else:
        rounder = "{:.2f}".format(rounder)

    return rounder
# -- Main Routine --

# set up Dictionaries

# set up list to hold 'modernised' ingredients
unit_central = {
    "tsp": 5,
    "tbs": 15,
    "cup": 237,
    "ounce": 28.35,
    "pint": 473,
    "quart": 946,
    "pound": 454,
    "litre": 1000,
    "ml": 1
}

# --- Generate Food Dictionary ---
# open file
groceries = open('01_ingredients_ml_to_g.csv')
# Read data into a list
csv_groceries = csv.reader(groceries)
# Create a dictionary to hold the data
food_dictionary = {}

# Add the data from the list into the dictionary
# (first item in row is key, next is definition)

for row in csv_groceries:
    food_dictionary[row[0]] = row[1]


# set up lists to hold original and 'modernised' recipes
modernised_recipe = []

# bold and reset are placeholders that can make text bold and not bold
bold = "\033[1m"
reset = "\033[0;0m"

# Explain program to user
print(bold, "--Ingredient Moderniser--", reset)
print()
print("This program helps you convert your ingredients into grams as")
print("having so many cups and spoons can become annoying so why not just use")
print(bold, "kitchen scales", reset, "!")
print()
print()

print("------------------")
# Ask user for recipe name and check its not blank
recipe_name = not_blank("What is the recipe name? ",
                   "The recipe can't be blank and can't contain numbers, ",
                   "no")

# Ask user where the recipe is originally from (numbers ok)
print()
source = not_blank("Where is the recipe from? ",
                   "The recipe source can't be blank, ",
                   "yes")
# Get serving sizes and scale factor
scale_factor = get_sf()

# Get amounts, units and ingredients from user
print()
full_recipe = get_all_ingredients()


# Split each line of the recipe into amount, unit and ingredient...
mixed_regex = "\d{1,3}\s\d{1,3}\/\d{1,3}"

for recipe_line in full_recipe:
    recipe_line = recipe_line.strip()

    if re.match(mixed_regex, recipe_line):

        # Get mixed number by matching regex
        pre_mixed_num = re.match(mixed_regex, recipe_line)
        mixed_num = pre_mixed_num.group()

        # Replace space with a + sign...
        amount = mixed_num.replace(" ", "+")
        # Change the string into a decimal
        amount = eval(amount)
        amount *= scale_factor

        # Get unit and ingredient
        compile_regrex = re.compile(mixed_regex)
        unit_ingredient = re.split(compile_regrex, recipe_line)
        unit_ingredient = (unit_ingredient[1]).strip()  # remove extra white space

    else:
        get_amount = recipe_line.split(" ", 1)

        try:
            amount = eval(get_amount[0])  # convert amount to float of possible
            amount *= scale_factor

        except NameError:
            amount = get_amount[0]
            modernised_recipe.append(recipe_line)
            continue

        except SyntaxError:
            modernised_recipe.append(recipe_line)
            continue

        unit_ingredient = get_amount[1]

    # Get unit and ingredient
    get_unit = unit_ingredient.split(" ", 1)  # splits text at first space

    num_spaces = recipe_line.count(" ")
    if num_spaces > 1:
        # Item has unit and ingredient
        unit = get_unit[0]
        ingredient = get_unit[1]
        unit = unit_checker(unit)

        # if unit is already in grams, add it to list
        if unit == "g":
            modernised_recipe.append("{:.0f} g {}".format(amount, ingredient))
            continue

        # convert to mls if possible...
        amount = general_converter(amount, unit, unit_central, 1)

        # If we converted to mls try and convert to grams
        if amount[1] == "yes":
            amount_2 = general_converter(amount[0], ingredient, food_dictionary, 250)

            if amount_2[1] == "yes":
                modernised_recipe.append("{:.0f} g {}".format(amount_2[0], ingredient))

            # if the ingredient is not in the list, leave the unit as ml
            else:
                modernised_recipe.append("{:.0f} g {}".format(amount[0], ingredient))
                continue
        # If the unit is not mls, leave the line unchanged
        else:
            rounded_amount = rounding(amount[0])

            modernised_recipe.append("{} {} {}".format(rounded_amount, unit,
            ingredient))  # Update list with scaled amount and original unit

    else:
        rounded_amount = rounding(amount)
        # Item only has ingredient (no unit given)
        modernised_recipe.append("{} {}".format(rounded_amount, unit_ingredient))


# Output ingredient list
print()
print("--------------------")
print("~{} Recipe~".format(recipe_name))
print("Source: {}".format(source))
print("--------------------")
print()
# Converted ingredients printed out to user
print(bold, "Converted Ingredients: ", reset)
print()
for item in modernised_recipe:
    print(item)
