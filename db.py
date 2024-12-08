import sqlite3

# Used in: main.py
def create_db():
    db = sqlite3.connect("recipe.db") # Opens database connection
    cursor = db.cursor()

    # Create the 'recipes' table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes
                    (RECIPE_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
                    TITLE      TEXT    NOT NULL,
                    DESC       TEXT    NOT NULL,
                    SERVINGS   INT     NOT NULL,
                    MINUTES    INT     NOT NULL,
                    DIRECTIONS TEXT    NOT NULL
                    );''')
    print("Recipes table created successfully")

    # Create the 'recipe_ingredients' table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS recipe_ingredients
                    (ITEM_ID  INTEGER PRIMARY KEY AUTOINCREMENT,
                    ITEM           TEXT    NOT NULL,
                    SPECS          TEXT,
                    QUANTITY       REAL     NOT NULL,
                    MEASURE_TYPE   TEXT    NOT NULL,
                    RECIPE_ID      INT     NOT NULL,
                    FOREIGN KEY(RECIPE_ID) REFERENCES recipes(RECIPE_ID) ON DELETE CASCADE
                    );''')
    
    cursor.execute("PRAGMA foreign_keys = ON;")
    print("Recipe_ingredients table created successfully")
    
    # Commit and Close
    db.commit()
    db.close()

# Used in: main.py
def sample_data(db):
    cursor = db.cursor()
    cursor.execute('''INSERT INTO recipes (TITLE, DESC, SERVINGS, MINUTES, DIRECTIONS) 
        VALUES 
        ("French Apple Pie", "Granny Smith Apple Pie with Crumb Topping", 12, 90, 
            "Preheat oven to 425 degrees. Peal and slice apples. Mix apples with sugar, cinnamon, and corn starch in a large bowl. 
              Pour into pie crust. Cook for 40 minutes. Mix flour, brown sugar, and butter in a separate bowl. Remove pie from oven. 
              Reduce oven to 400 degrees. Add crumb topping to pie. Return to oven and bake for an additional 15 minutes.")''')
    db.commit()

    recipe_id = cursor.lastrowid
    ingredients = [
        ("Apples", "Granny Smith, pealed and sliced", 8, "items", recipe_id ),
        ("Sugar", "white", 1, "cup", recipe_id ),
        ("Cinnamon", "ground", 1, "tsp", recipe_id),
        ("Corn Starch", "", 2, "TBSP", recipe_id),      
        ("Flour", "", 1, "cup", recipe_id),
        ("Brown Sugar", "packed", .5, "cup", recipe_id),
        ("Butter", "salted", .5, "cup", recipe_id)]
    cursor.executemany('''INSERT INTO recipe_ingredients (ITEM, SPECS, QUANTITY, MEASURE_TYPE, RECIPE_ID)
        VALUES (?,?,?,?,?)''', ingredients)
    db.commit()

    cursor.execute('''INSERT INTO recipes (TITLE, DESC, SERVINGS, MINUTES, DIRECTIONS) 
        VALUES 
        ("Grandmas Rolls", "Sweet Dinner Rolls", 24, 180,
              "In a small bowl, combine water, yeast, and a little sugar, then set aside. In a large bowl, microwave butter and milk for one minute. 
              Then combine eggs, sugar, and salt to butter and milk. Add yeast and walk mixture and stir thoroughly. Slowly add in flour. Cover and let raise for an hour. 
              Divide dough into three sections and roll out separately. Cut each section in roll into cressant. Set on baking sheet then cover let raise for an hour. 
              Preheat oven to 350 degrees, then bake for 14 minutes.")
        ''')
    db.commit()

    recipe_id = cursor.lastrowid
    ingredients = [
        ("Water", "warm", .25, "cups", recipe_id ),
        ("Yeast", "Dry", 1, "TBLS", recipe_id ),
        ("Sugar", "white", 1, "tsp", recipe_id),
        ("Sugar", "white", .5, "cup", recipe_id),
        ("Butter", "salted", .5, "cup", recipe_id),
        ("Eggs", "large", 3, "item", recipe_id),
        ("Salt", "iodized", 1, "tsp", recipe_id),
        ("Flour", "bread", 5.5, "cups", recipe_id)]
    cursor.executemany('''INSERT INTO recipe_ingredients (ITEM, SPECS, QUANTITY, MEASURE_TYPE, RECIPE_ID)
        VALUES (?,?,?,?,?)''', ingredients)
    db.commit()

    cursor.close()

# Used by: veiw_recipe, edit_recipe, delete_recipe
def has_recipes(db):
    cursor = db.execute("SELECT COUNT(*) FROM recipes")
    count = cursor.fetchone()[0]
    return count > 0 # return True if there are records

# Used by: edit_recipe
def has_ingedients(db, recipe_id):
    cursor = db.execute("SELECT COUNT(*) FROM recipes WHERE RECIPE_ID = ?", (recipe_id,))
    count = cursor.fetchone()[0]
    return count > 0 # return True if there are records

# Used by: edit_recipe
def edit_recipe_db(db, field, recipe_id, value):
    query = f"UPDATE recipes SET {field} = ? WHERE RECIPE_ID = ?"
    db.execute(query,(value, recipe_id))

# Used by: heading
def get_titles(db):
    cursor = db.execute("SELECT TITLE FROM recipes")
    return cursor.fetchall()

# Used by: choose_recipe
def get_titles_id(db):
    cursor = db.execute("SELECT RECIPE_ID, TITLE FROM recipes")
    return cursor.fetchall()

# Used by: view_recipe
def get_recipe (db, recipe_id):
    cursor = db.execute('''SELECT * FROM recipes WHERE RECIPE_ID = ?''', (recipe_id,))
    return cursor.fetchone()

# Used by: print_recipe, choose_ingredient
def get_ingredients(db, recipe_id):
    cursor = db.execute('''SELECT * FROM recipe_ingredients WHERE RECIPE_ID = ?''', (recipe_id,))
    return cursor.fetchall()

# Used by: print_recipe (revised method using JOIN)
def get_recipe_with_ingredients(db, recipe_id):
    query = '''
        SELECT 
            r.*,
            ri.ITEM,
            ri.SPECS,
            ri.QUANTITY,
            ri.MEASURE_TYPE
        FROM recipes AS r
        LEFT JOIN recipe_ingredients AS ri
            ON r.RECIPE_ID = ri.RECIPE_ID
        WHERE r.RECIPE_ID = ?
        '''
    cursor = db.execute(query, (recipe_id,))
    return cursor.fetchall()

# Used by: add_recipe
def new_recipe(db, recipe):
    cursor = db.cursor()
    cursor.execute("INSERT INTO recipes (TITLE, DESC, SERVINGS, MINUTES, DIRECTIONS) VALUES (?,?,?,?,?)", recipe)
    db.commit()
    return cursor.lastrowid

# Used by: add_ingredients
def new_ingredient(db, ingredient):
    db.execute("INSERT INTO recipe_ingredients (ITEM, SPECS, QUANTITY, MEASURE_TYPE, RECIPE_ID) VALUES (?,?,?,?,?)", ingredient)
    db.commit()

# Used by: delete_recipe
def ingredient_exists(db, recipe_id):
    cursor = db.execute("SELECT 1 FROM recipe_ingredients WHERE RECIPE_ID = ?", (recipe_id,))
    result = cursor.fetchone()
    return result is not None  # returns True if there is at least 1

# Used by: delete_recipe
def recipe_exists(db, recipe_id):
    cursor = db.execute("SELECT 1 FROM recipes WHERE RECIPE_ID = ?", (recipe_id,))
    result = cursor.fetchone()
    return result is not None  # returns True if there is at least 1

# Used by: delete_recipe
def del_recipe (db, recipe_id):
    db.execute('''DELETE FROM recipes WHERE RECIPE_ID = ?''', (recipe_id,))
    db.commit()

# Used by: change_ingredient
def del_ingredients(db, recipe_id):
    db.execute('''DELETE FROM recipe_ingredients WHERE RECIPE_ID = ?''', (recipe_id,))
    db.commit()

# Used by: change_ingredient
def del_ingredient(db, item_id):
    db.execute('''DELETE FROM recipe_ingredients WHERE ITEM_ID = ?''', (item_id,))
    db.commit()