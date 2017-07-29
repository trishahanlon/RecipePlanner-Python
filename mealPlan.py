# Trisha Moyer
# Version 3.5

from tkinter import *
import datetime
from isoweek import Week
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk

LARGE_FONT=("Trebuchet MS", 24)
MEDIUM_FONT=("Trebuchet MS", 14)

class MakeMealPlan(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#f8f8f8")
        menu_frame = Frame(self, bg="#e7e7e7")
        menu_frame.pack(fill='both')

        load = Image.open("home.jpg")
        render = ImageTk.PhotoImage(load)
        from landingpage import LandingPage
        img = Button(menu_frame, image=render, borderwidth=0, highlightthickness=0, highlightbackground="#e7e7e7",
                     command=lambda: controller.show_frame(LandingPage))
        img.image = render
        img.grid(row=0, column=0, sticky="nsew")

        label = Label(menu_frame, text="Meal Planner", font=LARGE_FONT, bg="#e7e7e7", fg="#272822")
        label.grid(row=0, column=1, sticky="nsew")

        grocery_button = Button(menu_frame, text="Grocery List", highlightbackground="#e7e7e7", command=lambda: view_grocery_list())
        grocery_button.grid(row=0, column=2, sticky="nsew")

        view_recipe_frame = Frame(self, bg="#f8f8f8")

        now = datetime.datetime.now()
        dt = datetime.date(now.year, now.month, now.day)
        week_number = dt.isocalendar()[1]
        w = Week(now.year, week_number)

        menu = Frame(self, bg="#f8f8f8")
        menu.pack()

        column_labels = ["Breakfast", "Lunch", "Dinner"]
        for i in range(len(column_labels)):
            Label(menu, text=column_labels[i], font=("Trebuchet MS", 16), bg="#f8f8f8").grid(row=0, column=i+2, pady= 10,
                                                                                        padx=85, sticky="nsew")
        monday_text = "Monday " + str(w.monday())
        tuesday_text = "Tuesday " + str(w.tuesday())
        wednesday_text = "Wednesday " + str(w.wednesday())
        thursday_text = "Thursday " + str(w.thursday())
        friday_text = "Friday " + str(w.friday())
        saturday_text = "Saturday " + str(w.saturday())
        sunday_text = "Sunday " + str(w.sunday())

        labels = [monday_text, tuesday_text, wednesday_text, thursday_text, friday_text, saturday_text, sunday_text]
        for i in range(len(labels)):
            Label(menu, font=("Trebuchet MS", 12), bg="#f8f8f8", text=labels[i]).grid(row=i+1, column=0, padx = 5, pady=15, sticky="w")
            sep = ttk.Separator(menu, orient="vertical")
            sep.grid(row=i+1, column=1, padx=5, sticky="nsew")

        database_file = "meal_planner.db"
        tableName = "recipes_" + str(week_number)
        menuDict = {}
        with sqlite3.connect(database_file) as conn:
            cursor = conn.cursor()
            selection = cursor.execute("""SELECT * FROM """ + tableName)
            for result in [selection]:
                for row in result.fetchall():
                    name = row[0]
                    row_db = row[1]
                    column_db = row[2]
                    menuDict[name] = (row_db, column_db)
        valueArray = []
        keyArray = []
        for (key, value) in menuDict.items():
            print(key, value)
            keyArray.append(key)
            valueArray.append(value)

        button_dict = {}
        list_of_buttons = []
        for rows in range(len(labels)):
            for columns in range(len(column_labels)):
                buttons = Button(menu, text="Add meal", highlightbackground="#f8f8f8",
                                 command=lambda x=rows + 1, y=columns + 2: add_meal(x, y))
                buttons.grid(row=rows + 1, column=columns + 2)
                locationTuple = (rows+1, columns+2)
                for key, value in menuDict.items():
                    if locationTuple == value:
                        #dont add a button
                        recipeLabel = Label(menu, text=key, bg="#f8f8f8", padx=1, pady=1)
                        recipeLabel.grid(row=value[0], column=value[1])
                        recipeLabel.bind("<Button-1>", lambda event, x=key: print_recipe(x))
                    else:
                        buttons.grid(row=rows + 1, column=columns + 2)
                        buttons.position = (rows + 1, columns + 2)
                        button_dict[buttons] = buttons.position
                        list_of_buttons.append(buttons)

        def add_meal(rowLocation, columnLocation):
            """Grabs meals from the database to be displayed.

            Keyword arguments:  rowLocation - Row on the grid
                                columnLocation - Column on the grid
            :return: Nothing
            """
            menu.pack_forget()
            view_recipe_frame.forget()
            add_meal_frame = Frame(self, bg="#f8f8f8")
            add_meal_frame.pack()

            recipe_names = []
            ingredient_list = []
            database_file = "meal_planner.db"
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                selection = cursor.execute("""SELECT * FROM recipe""")
                for result in [selection]:
                    for row in result.fetchall():
                        name = row[0]
                        ingredients = row[4]
                        recipe_names.append(name)
                        ingredient_list.append(ingredients)
            for i in range(len(recipe_names)):
                Button(add_meal_frame, text=recipe_names[i], highlightbackground="#f8f8f8", command=lambda x=recipe_names[i], y=ingredient_list[i]:add_recipe(x, y, add_meal_frame,
                                                                                     rowLocation, columnLocation)).grid(row=i, column=0)

        def add_recipe(recipe, ingredients, view, row, column):
            """Adds recipe name to the grid for the meal plan.

            Keyword arguments:  recipe - recipe name
            ingredients - ingredients for that recipe
            view - the add meal frame
            rowLocation - Row on the grid
            columnLocation - Column on the grid

            :return: Nothing
            """
            view.pack_forget()
            view_recipe_frame.forget()
            searchIndex = (row, column)
            for key, value in button_dict.items():
                if value == searchIndex:
                    key.destroy()
            save_weeks_recipes(recipe, row, column)
            save_ingredients(ingredients)
            recipe_label = Label(menu, text=recipe, bg="#f8f8f8")
            recipe_label.grid(row = row, column = column)
            recipe_label.bind("<Button-1>", lambda event: print_recipe(recipe))
            menu.pack()

        def print_recipe(recipeName):
            """Prints the recipe info on a new screen.

            Keyword arguments:  recipe - recipe name

            :return: Nothing
            """
            menu.pack_forget()
            view_recipe_frame.pack(expand=True, fill='both')
            grocery_button.grid_forget()
            database_file = "meal_planner.db"
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                selection = cursor.execute("""SELECT * FROM recipe WHERE name = ?;""", (recipeName, ))
                for result in [selection]:
                    for row in result.fetchall():
                        name = row[0]
                        time = row[1]
                        servings = row[2]
                        ingredients = row[4]
                        directions = row[5]
                        string = ("Name: {} \n Cook time: {} \n Number of Servings: {} \n ".format(name, time, servings))
                        second_string = ("Ingredients: {}".format(ingredients))
                        third_string = ("Directions: {}".format(directions))
            Label(view_recipe_frame, text=string, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000").grid(row=1, column=0, sticky="nsew", padx=400)
            Label(view_recipe_frame, text=second_string, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000").grid(row=2, column=0, sticky="nsew")
            Label(view_recipe_frame, text=third_string, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000").grid(row=3, column=0, sticky="nsew")

            return_button = Button(menu_frame, text = "Return to Menu", highlightbackground="#e7e7e7", command=lambda: [view_recipe_frame.pack_forget(),
                                                                                                                        return_button.grid_forget(),
                                                                                     menu.pack(), label.configure(text="Meal Planer"), grocery_button.grid(row=0, column=2, sticky="nsew")])
            # returnButton.pack(side=RIGHT)
            return_button.grid(row=0, column=4, sticky="nsew")

        def view_grocery_list():
            """Prints the grocery list for the week.

            Keyword arguments:  None

            :return: Nothing
            """

            grocery_list_frame = Frame(self,  bg="#f8f8f8")
            grocery_list_frame.pack()

            menu.pack_forget()
            grocery_button.grid_forget()
            label.configure(text="Grocery List")

            i = 0
            database_file = "meal_planner.db"
            item_array = []
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                tableName = "ingredients_" + str(week_number)
                selection = cursor.execute("""SELECT * FROM """ + tableName)
                for result in [selection]:
                    for row in result.fetchall():
                        print(row)
                        for ingredient in row:
                            print(ingredient)
                            item_array.append(str(ingredient).split())
                        i = i +1
                        Label(grocery_list_frame, text=ingredient, bg="#f8f8f8", font=MEDIUM_FONT, justify=LEFT).grid(row=i, column=0, sticky="w")
            return_button = Button(menu_frame, text = "Return to Menu", highlightbackground="#e7e7e7", command=lambda: [grocery_list_frame.pack_forget(),
                                                                                                                        return_button.grid_forget(),
                                                                                     menu.pack(), label.configure(text="Meal Planer"), grocery_button.grid(row=0, column=2, sticky="nsew")])
            # returnButton.pack(side=RIGHT)
            return_button.grid(row=0, column=4, sticky="nsew")

        def save_ingredients(ingredients):
            """Save the ingredients to the database so we can get them later for the grocery list.

            Keyword arguments:  ingredients - ingredients to be saved to db

            :return: Nothing
            """
            database_file = "meal_planner.db"
            with sqlite3.connect(database_file) as conn:
                # create the table if it hasn't been created yet
                tableName = "ingredients_" + str(week_number)
                conn.execute('''CREATE TABLE IF NOT EXISTS ''' + tableName + ''' (ingredients text)''')
                conn.execute("""INSERT INTO """ + tableName + """ VALUES (?);""", (ingredients,))
            
        def save_weeks_recipes(recipeName, row, column):
            """Save the week's recipe so we can keep them between app sessions.

            Keyword arguments:  recipeName - the name of the recipe
            row - the row the recipe belongs to in the menu grid
            column - the column the recipe belongs to in the menu grid

            :return: Nothing
            """
            print("save weeks")
            database_file = "meal_planner.db"
            with sqlite3.connect(database_file) as conn:
                # create the table if it hasn't been created yet
                tableName = "recipes_" + str(week_number)
                conn.execute('''CREATE TABLE IF NOT EXISTS ''' + tableName + ''' (recipe text, row int, column int)''')
                conn.execute("""INSERT INTO """ + tableName + """ VALUES (?, ?, ?);""", (recipeName, row, column))
            