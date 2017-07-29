# Trisha Moyer
# Version 3.5

from tkinter import *
from addRecipe import AddARecipe
from tkinter import messagebox
import datetime
from mealPlan import MakeMealPlan
from PIL import Image, ImageTk
import sqlite3

LARGE_FONT=("Trebuchet MS", 24)
MEDIUM_FONT=("Trebuchet MS", 12)


def set_up_database():
    """Creates the database and tables needed for the project.

    Keyword arguments: None
    :return: Nothing
    """
    database_file = "meal_planner.db"
    now = datetime.datetime.now()
    dt = datetime.date(now.year, now.month, now.day)
    week_number = dt.isocalendar()[1]

    with sqlite3.connect(database_file) as conn:
        # create the tables if they haven't been created yet
        recipe_table_name = "recipes_" + str(week_number)
        conn.execute('''CREATE TABLE IF NOT EXISTS ''' + recipe_table_name + ''' (recipe text, row int, column int)''')
        ingredients_table_name = "ingredients_" + str(week_number)
        conn.execute('''CREATE TABLE IF NOT EXISTS ''' + ingredients_table_name + ''' (ingredients text)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS recipe (name text, time int, servings int, favorite text, ingredients text, directions text)''')

class LandingPage(Frame):
    def __init__(self, parent, controller):
        """Initalizes first page of the app"""
        Frame.__init__(self, parent)
        #set up the database for the app
        set_up_database()
        #create the frames for this page
        view_recipe_frame = Frame(self, bg="#f8f8f8")
        menu_frame = Frame(self, bg="#e7e7e7")
        view_details_frame = Frame(self, bg="#f8f8f8")
        delete_menu_frame = Frame(self, bg="#e7e7e7")
        frame = Frame(self, bg="#f8f8f8")
        frame.pack(expand=True, fill='both')
        Label(frame, text="Trisha's Meal Planner", font=LARGE_FONT, bg="#f8f8f8", fg="#000000").pack(fill='both', pady=20)

        load = Image.open("recipe_card.jpg")
        render = ImageTk.PhotoImage(load)
        img = Label(frame, image = render, bg="#f8f8f8")
        img.image = render
        img.pack(fill='both', pady=40)

        Button(frame, text="Add A Recipe", highlightbackground="#f8f8f8", command=lambda: controller.show_frame(AddARecipe)).pack(fill=Y)
        Button(frame, text="Make a Meal Plan", highlightbackground="#f8f8f8", command=lambda: controller.show_frame(MakeMealPlan)).pack(fill=Y)
        Button(frame, text="View Recipes", highlightbackground="#f8f8f8", command=lambda: view_recipes()).pack(fill=Y)

        def view_recipes():
            """Allows the user to view the recipes in the database.

            Keyword arguments: None
            :return: Nothing
            """
            frame.pack_forget()
            #add the menu
            menu_frame.pack(fill='both')
            load = Image.open("home.jpg")
            render = ImageTk.PhotoImage(load)
            img = Button(menu_frame, image=render, borderwidth=0, highlightthickness=0,
                         highlightbackground="#e7e7e7",
                         command=lambda: [frame.pack(expand=True, fill='both'),
                                          view_details_frame.pack_forget(),
                                          menu_frame.pack_forget(),
                                          view_recipe_frame.pack_forget()])
            img.image = render
            img.pack(side=LEFT)
            label = Label(menu_frame, text="View Recipe", font=LARGE_FONT, bg="#e7e7e7", fg="#272822")
            label.pack(side=LEFT, padx=300)

            #add this view
            view_recipe_frame.pack(expand=True, fill='both')
            database_file = "meal_planner.db"
            recipe_array = []
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                selection = cursor.execute("""SELECT name FROM recipe""")
                for result in [selection]:
                    for row in result.fetchall():
                        name = row[0]
                        recipe_array.append(name)

            for recipe in recipe_array:
                label = Label(view_recipe_frame, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000",
                              text=recipe)
                label.pack()
                label.bind("<Button-1>", lambda event: [view_details(name), view_recipe_frame.pack_forget()])

        def view_details(recipeName):
            """Called when a user clicks on a recipe.
            Gives them the details of the recipe.

            Keyword arguments: recipeName -- recipe name that we want to view.
            :return: Nothing
            """
            #updatae the frame like always
            menu_frame.pack_forget()
            view_recipe_frame.pack_forget()
            database_file = "meal_planner.db"
            delete_menu_frame.pack(fill='both')
            load = Image.open("home.jpg")
            render = ImageTk.PhotoImage(load)
            img = Button(delete_menu_frame, image=render, borderwidth=0, highlightthickness=0,
                         highlightbackground="#e7e7e7",
                         command=lambda: [frame.pack(expand=True, fill='both'),
                                          view_details_frame.pack_forget(),
                                          delete_menu_frame.pack_forget(),
                                          view_recipe_frame.pack_forget()])
            img.image = render
            img.pack(side=LEFT)
            label = Label(delete_menu_frame, text="View Recipe", font=LARGE_FONT, bg="#e7e7e7", fg="#272822")
            label.pack(side=LEFT, padx=300)
            Button(delete_menu_frame, text="Delete", highlightbackground="#e7e7e7",
                   command=lambda: delete_recipe(name)).pack(side=RIGHT)
            view_details_frame.pack(expand=True, fill='both')
            #query the database to get out the recipe
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
                        string = ("Name: {} \n Cook time: {} \n Number of Servings: {} \n Ingredients: {} \n Directions: {}".format(name, time, servings, ingredients, directions))
                        Label(view_details_frame, text=string, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000").pack(side=TOP)
            conn.close()

        def delete_recipe(recipeName):
            """Called when a user clicks on delete a recipe.

            Keyword arguments: recipeName -- recipe name that the user wants to delete.
            :return: Nothing
            """
            
            database_file = "meal_planner.db"
            now = datetime.datetime.now()
            dt = datetime.date(now.year, now.month, now.day)
            week_number = dt.isocalendar()[1]
            tableName = "recipes_" + str(week_number)
            # we want to query the database, and if it's part of this week's menu - don't delete.
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT count(*) FROM """ + tableName + """ WHERE recipe = ?;""", (recipeName, ))
                return_object = cursor.fetchone()[0]
                if return_object == 0:
                    actually_delete(recipeName)
                    print("there is no component named {}".format(recipeName))
                else:
                    print("component {} found".format(recipeName))
                    messagebox.showerror("Cannot Delete",
                                         "Cannot delete recipe when it's used in the current week's menu.")

        def actually_delete(recipeName):
            """Called when the recipe the user wants to delete is not part of the menu.

            Keyword arguments: recipeName -- recipe name that the user wants to delete.
            :return: Nothing
            """
            with sqlite3.connect("meal_planner.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""DELETE FROM recipe WHERE name = ?;""", (recipeName, ))
                if cursor.rowcount == 1:
                    messagebox.showinfo("Success", "Recipe Deleted.")
                    menu_frame.pack_forget()
                    delete_menu_frame.pack_forget()
                    view_details_frame.pack_forget()
                    view_recipe_frame.pack_forget()
                    frame.pack(expand=True, fill='both')
                elif cursor.rowcount == 0:
                    messagebox.showerror("Cannot Delete", "Error.")
            conn.close()
