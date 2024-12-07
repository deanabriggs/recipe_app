import os
from db import *

# Clears the terminal view (Windows OS)
def clear():
    os.system("cls") # clears the terminal

# Used in main.py, view_recipe, edit_recipe, delete_recipe
def sample_data_prompt(db):
    choice = input("Would you like to import sample recipes? (y/n) => ")
    if choice.lower() == "y":
        sample_data(db)
    clear()

# Program heading with list of existing recipes
def heading(db):
    clear()
    print("MY FAVORITE RECIPES")
    if has_recipes(db) == True:
        recipes = get_titles(db)
        for recipe in recipes:
            print(f" - {recipe[0]}")
    else:
        print("  - no recipes yet")

# Provides menu options and returns choice
def options():
    # provide menu options
    print('''
Choose an Option:
  1. View Recipe Details
  2. Add New Recipe
  3. Edit Existing Recipe
  4. Delete Recipe
  5. Exit''')
    choice = input("\n=> ")  # store choice in variable
    return choice            # returns chosen value (text)

# View Recipe Options
def view_recipe(db):
    if has_recipes(db):                     # Checks that there are recipes
        recipe_id = choose_recipe(db)       # Prompts for a choice from numbered list and returns recipe_id
        print_recipe(db, recipe_id)         # Prints the Recipe Info
        input("")                     # Waits for user input to exit the view
    else:
        clear()
        print("There are no existing recipes to view.")
        sample_data_prompt(db)
    
# Displays numbered list of recipes, prompts for choice, returns recipe_id
def choose_recipe(db):
    clear() # Clear the Terminal
    print("Choose a recipe:")

    # Provides recipes in a numbered list
    recipes = get_titles_id(db)  
    for i, recipe in enumerate(recipes, start=1):
        print(f" {i}. {recipe[1]}")

    choice = int(input("\nEnter number => "))      # saves choice to a variable
    recipe_id = recipes[choice-1][0]               # identifies recipe_id in the table
    return recipe_id                               # returns recipe_id

# Displays recipe details with related ingredients
def print_recipe(db, recipe_id): 
    recipe = get_recipe(db, recipe_id)
    clear() # Clear the Terminal

    # Prints Recipe Info
    print(f'{recipe[1].upper()} RECIPE\n')
    print(f"Description:  {recipe[2]}")
    print(f"Servings:     {recipe[3]}")
    print(f"Prep Time:    {recipe[4]} minutes")
    print(f"Directions:   {recipe[5]}")
    
    # Retrieve Ingredients
    ingredients = get_ingredients(db, recipe_id)    

    # Print Ingredients
    print("Ingredients:")
    if not ingredients:
        print("              No ingredients provided")
    else:
        for item in ingredients:
            print(f"        {item[3]:>3} {item[4]:<6} {item[1]} {item[2]}")

def add_recipe (db):
    # Prompts user input for recipe
    title = input("What is the recipe name => ")
    desc = input("Describe the recipe => ")
    servings = int(input("How many servings will it make => "))
    min = int(input("How many minutes does it require to make => "))
    directions = input("Give detailed instructions => ")
    
    # Stores user inputs in a single variable
    recipe = title, desc, servings, min, directions
    
    # Adds entry to database & retrieves the recipe_id for the new recipe just entered
    recipe_id = new_recipe(db, recipe)
    print("Recipe Added!\n")

    # Starts function to add incredients, relates to the new recipe with recipe_id
    add_ingredients(db, recipe_id)

def add_ingredients(db, recipe_id):
    # Prompts user to enter ingredients
    print("Add ingredients needed for your recipe: ")
    qty = int(input("Item Qauntity => "))
    measurement = input("Item Measurement (tsp, TBLS, cups, items) => ")
    item = input("Ingredient => ")
    specs = input("Item details (melted, brand, type) => ")

    # Stores ingredient details in a single variable
    ingredient = item, specs, qty, measurement, recipe_id
    
    # Adds entry to database
    new_ingredient(db, ingredient)
    print(f"{item} item added")

    # Prompts for adding additional ingredients, will continue using recurssion until user enters "n"
    more = input("Add more items (y/n) => ")
    if more.lower() != "n":
        add_ingredients(db, recipe_id)

def edit_recipe(db):
    if has_recipes(db):                     # Checks that there are recipes
        recipe_id = choose_recipe(db)       # Prompts for a choice from numbered list and returns recipe_id
        print_recipe(db, recipe_id)         # Prints the Recipe Info
        input("")                 # Waits for user input to exit the view
    else:
        clear()
        print("There are no existing recipes to edit.")
        sample_data_prompt(db)

def delete_recipe(db):
    if has_recipes(db):                     # Checks that there are recipes
        recipe_id = choose_recipe(db)       # Prompts for a choice from numbered list and returns recipe_id
        print_recipe(db, recipe_id)
        confirm = input("\nAre you sure you want to DELETE? (y/n) => ")
        if confirm.lower() == "y":

            if ingredient_exists(db, recipe_id):            # Checks that there is a recipe with this recipe_id
                del_ingredients(db, recipe_id)              # Deletes chosen ingredients based on choice
            
            if recipe_exists(db, recipe_id):                # Checks that there are ingredients associated to this recipe_id
                del_recipe(db, recipe_id)                   # Deletes chosen recipe based on choice
                print("Recipe has been deleted.")
    else:
        clear()
        print("There are no existing recipes to delete.")
        sample_data_prompt(db)