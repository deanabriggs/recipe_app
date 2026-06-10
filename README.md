# Recipe App — Python + SQLite

A command-line recipe manager that demonstrates full CRUD (Create, Read, Update, Delete) operations against a relational SQLite database. Store your favorite recipes and retrieve them whenever you need them.

## Overview

This is a self-contained recipe program that lets a user store and retrieve their favorite recipes. On startup, the database is created automatically if it doesn't already exist. If there are no recipes yet, the user is offered a set of sample recipes to get started. From there, a menu lets the user view, add, edit, or delete recipes, with each option guiding the user through a series of prompts that read from and write to the database.

Because it's fully self-contained, the app runs on a single device with no network connection required.

## Getting Started

Make sure Python is installed on your system, then run:

```bash
python main.py
```

Some environments use `py main.py` instead.

## Database Design

The database has two tables connected by a foreign key. A LEFT JOIN from `recipes` to `recipe_ingredients` retrieves data from both tables in a single query.

**recipes**
- `recipe_id` (primary key)
- `title`
- `desc`
- `servings`
- `minutes`
- `directions`

**recipe_ingredients**
- `item_id` (primary key)
- `item`
- `specs`
- `quantity`
- `measure_type`
- `recipe_id` (foreign key → recipes)

## Development Environment

- Visual Studio Code (v1.95.3)
- Python 3.13.0
- SQLite3 (built-in Python library)

## Demo

<!-- TODO: add Software Demo Video link -->

## Future Work

- Error handling for unexpected values
- Add options for canceling actions
- Sort recipes in alphabetical order
- Add update commands for ingredients, not just the recipe table
- Add a feature to print to PDF
- Add a feature to double or halve recipes
- Print recipes using a JOIN
