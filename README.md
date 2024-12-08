# Overview

This software was designed to show how Python can be used to Create, Read, Update, and Delete information in a relational database (SQLite). It can create the database and auto-populate data.

This is a recipe program designed for a user to store their favorite recipes and retrieve them when desired. When a user starts the program, the database is created if it doesn't arleady exist. If there aren't any existing recipes in the database, the user is asked if they want to use sample recipes. After they respond, existing recipes will be listed and menu options to view, add, edit, delete, or exit the program are provided. Each menu option will take the user through a series of prompts that interact with the database.

This software is self-contained allowing for it to be used on a signle device without a network connection.

{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}

[Software Demo Video](https://youtu.be/UWvvncjU9e8)

# Relational Database

This relational database has two tables: recipes and recipe_ingredients. Both tables have an auto-incrementing primary key. The recipe_ingredients table has a foreign key that connects it to the recipes table. A left join from the recipes table to the recipe_ingredients table allows for data to be retrieved from both tables in a single call to the database. The fields for each table are outlined below:

### recipes

- recipe_id (KEY)
- title
- desc
- servings
- minutes
- directions

### recipe_ingredients

- item_id (KEY)
- item
- specs
- quantity
- measure_type
- recipe_id (FOREIGN KEY to recipes)

# Development Environment

- Visual Studio Code (v1.95.3)
- Python 3.13.0
- SQLite3 (built-in library in Python)

# Useful Websites

- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [DB-API 2.0 ingerface for SQLite databases](https://docs.python.org/3.8/library/sqlite3.html)
- [SQL Tutorial](https://www.w3schools.com/sql/)
- [Tutorialspoint](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)

# Future Work

Fixes and Improvements

- Error handling for unexpected values
- Add options for canceling actions
- Sorting recipes in Alpha order
- Add "update" commands for ingredients, not just recipe table
- Add feature to print to a PDF
- Add feature to double or half recipes
- Print recipes using JOIN
