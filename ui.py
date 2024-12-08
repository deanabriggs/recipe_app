import os
from db import *

# Clears the terminal view (Windows OS)
def clear():
    os.system("cls") # clears the terminal

# Used in main.py, view_recipe, edit_recipe, delete_recipe
def sample_data_prompt(db):
    if not has_recipes(db):
        choice = input("\nWould you like to import sample recipes? (y/n) => ")
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

# Displays numbered list of ingredients, prompts for choice, returns item_id
def choose_ingredient(db, recipe_id):
    print("Choose a ingredient:")

    # Provides recipes in a numbered list
    ingredients = get_ingredients(db, recipe_id)  
    for i, ingredient in enumerate(ingredients, start=1):
        print(f" {i}. {ingredient[1]}")

    choice = int(input("\nEnter number => "))      # saves choice to a variable
    ingredient_id = ingredients[choice-1][0]       # identifies item_id in the table
    return ingredient_id                           # returns item_id

# Displays recipe details with related ingredients
def print_recipe(db, recipe_id):
    clear() # Clear the Terminal
    
    #recipe = get_recipe(db, recipe_id) 
    
    # Update method of pulling recipe data
    recipe_data = get_recipe_with_ingredients(db, recipe_id)
    recipe = recipe_data[0] # uses the first tuple of the data to extract recipe info

    # Prints Recipe Info
    print(f'{recipe[1].upper()} RECIPE\n')
    print(f"Description:  {recipe[2]}")
    print(f"Servings:     {recipe[3]}")
    print(f"Prep Time:    {recipe[4]} minutes")
    print(f"Directions:   {recipe[5]}")
    
    # Retrieve Ingredients
    #ingredients = get_ingredients(db, recipe_id) 
    
    # Update method of pulling related ingredients
    ingredients = [row[6:] for row in recipe_data if row[6]] # narrows data to ingredient values that are not null

    # Print Ingredients
    print("Ingredients:")
    if not ingredients:
        print("              No ingredients provided")
    else:
        for item in ingredients:
            #print(f"        {item[3]:>3} {item[4]:<6} {item[1]} {item[2]}")
            
            # revised for new method of pulling data
            print(f"        {item[2]:>3} {item[3]:<6} {item[0]} {item[1]}")

# Prompts to add a new recipe with ingredients then adds to database
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

# Supports add_recipe & edit_recipe
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
        field = change_recipe_prompt() # Returns a number for recipe choice index, 0 if ingredient, or null to cancel action
        if field:                           # Checks for valid option or if action was canceled
            if field == "INGREDIENTS":
                change_ingredient(db, recipe_id)
            else:
                value = input("Enter new value => ")
                if field in ("SERVINGS", "MINUTES"):
                    value = int(value)
                edit_recipe_db(db, field, recipe_id, value)
        else:
            print("Nothing was updated")
    else:
        clear()
        print("There are no existing recipes to edit.")
        sample_data_prompt(db)

# Prompts for change choice, Returns a number for recipe choice index, 0 if ingredient, or null to cancel action
def change_recipe_prompt():
    choice = input('''
What would you like to change? 
    1. Title
    2. Description
    3. Servings
    4. Prep Time
    5. Directions
    6. Ingredients
    7. Cancel
Choose a number => ''')
    if choice == "1":
        return "TITLE"
    elif choice == "2":
        return "DESC"
    elif choice == "3":
        return "SERVINGS"
    elif choice == "4":
        return "MINUTES"
    elif choice == "5":
        return "DIRECTIONS"
    elif choice == "6":
        return "INGREDIENTS"
    else:
        return

def change_ingredient(db, recipe_id):
    if has_ingedients(db, recipe_id):   # if there are existing ingredients, give options to add, edit, or delete
        edit_type = input('''Choose an option:
  1. Add more ingredients
  2. Remove an ingredient         
  3. Edit an ingredient
Enter number => ''')
        if edit_type == "1":
            add_ingredients(db, recipe_id)
        elif edit_type == "2":
            ingredient_id = choose_ingredient(db, recipe_id)
            del_ingredient(db, ingredient_id)
        elif edit_type == "3":
            ingredient_id = choose_ingredient(db, recipe_id)
            del_ingredient(db, ingredient_id)
            add_ingredients(db, recipe_id)
        else:
            return
    else: 
        add_ingredients(db, recipe_id)  # if there are no ingredients, prompt to add

# Prompts for which recipe to delete, asks for confirmation, deletes recipe and ingredients from database
def delete_recipe(db):
    if has_recipes(db):                     # Checks that there are recipes
        recipe_id = choose_recipe(db)       # Prompts for a choice from numbered list and returns recipe_id
        print_recipe(db, recipe_id)
        confirm = input("\nAre you sure you want to DELETE? (y/n) => ")
        if confirm.lower() == "y":
            
            if recipe_exists(db, recipe_id):                # Checks that there is a recipe with this recipe_id
                del_recipe(db, recipe_id)                   # Deletes chosen recipe based on choice (associate ingredients will be deleted automatically because Cascade Delete is on)
                print("Recipe has been deleted.")
    else:
        clear()
        print("There are no existing recipes to delete.")
        sample_data_prompt(db)