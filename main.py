import sqlite3
from ui import clear, sample_data_prompt, heading, options, view_recipe, add_recipe, edit_recipe, delete_recipe
from db import create_db

db = sqlite3.connect("recipe.db")   # Opens database connection
create_db()                         # Creates database if it doesn't exist
cursor = db.cursor()

sample_data_prompt(db)

def menu ():
    while True:
        heading(db)                 # Program heading with list of existing recipes
        choice = options()          # Provides menu options and returns choice
        
        # Run functions based on choice
        if choice == "1": view_recipe(db)
        elif choice == "2": add_recipe(db)
        elif choice == "3": edit_recipe(db)
        elif choice == "4": delete_recipe(db)
        elif choice == "5":
            db.close()
            clear()
            break
        else: clear()
menu()