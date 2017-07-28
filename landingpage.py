from tkinter import *
from addRecipe import AddARecipe
from tkinter import messagebox
import datetime
from mealPlan import MakeMealPlan
from PIL import Image, ImageTk
import sqlite3

LARGE_FONT=("Trebuchet MS", 24)
MEDIUM_FONT=("Trebuchet MS", 12)

recipeNames = []


def set_up_database():
    database_file = "meal_planner.db"
    now = datetime.datetime.now()
    dt = datetime.date(now.year, now.month, now.day)
    weekNumber = dt.isocalendar()[1]

    with sqlite3.connect(database_file) as conn:
        # create the tables if they haven't been created yet
        recipeTableName = "recipes_" + str(weekNumber)
        conn.execute('''CREATE TABLE IF NOT EXISTS ''' + recipeTableName + ''' (recipe text, row int, column int)''')
        ingredientsTableName = "ingredients_" + str(weekNumber)
        conn.execute('''CREATE TABLE IF NOT EXISTS ''' + ingredientsTableName + ''' (ingredients text)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS recipe (name text, time int, servings int, favorite text, ingredients text, directions text)''')

class LandingPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        set_up_database()

        viewRecipeFrame = Frame(self, bg="#f8f8f8")
        menuFrame = Frame(self, bg="#e7e7e7")
        viewDetailsFrame = Frame(self, bg="#f8f8f8")
        deleteMenuFrame = Frame(self, bg="#e7e7e7")

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
            frame.pack_forget()
            #add the menu
            menuFrame.pack(fill='both')
            load = Image.open("home.jpg")
            render = ImageTk.PhotoImage(load)
            img = Button(menuFrame, image=render, borderwidth=0, highlightthickness=0,
                         highlightbackground="#e7e7e7",
                         command=lambda: [frame.pack(expand=True, fill='both'),
                                          viewDetailsFrame.pack_forget(),
                                          menuFrame.pack_forget(),
                                          viewRecipeFrame.pack_forget()])
            img.image = render
            img.pack(side=LEFT)
            label = Label(menuFrame, text="View Recipe", font=LARGE_FONT, bg="#e7e7e7", fg="#272822")
            label.pack(side=LEFT, padx=300)

            #add this view
            viewRecipeFrame.pack(expand=True, fill='both')
            database_file = "meal_planner.db"

            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT count(*) FROM recipe""")
                returnObject = cursor.fetchone()[0]
                recipe_list_length = returnObject

            i = 0
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                selection = cursor.execute("""SELECT name FROM recipe""")
                for result in [selection]:
                    for row in result.fetchall():
                        name = row[0]
                        recipeNames.append(name)
                        i = i +1
                        label = Label(viewRecipeFrame, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000",
                                      text=name)
                        label.pack()
                        label.bind("<Button-1>", lambda event: [callback(name), viewRecipeFrame.pack_forget()])

        def callback(recipeName):
            menuFrame.pack_forget()
            viewRecipeFrame.pack_forget()
            database_file = "meal_planner.db"

            deleteMenuFrame.pack(fill='both')
            load = Image.open("home.jpg")
            render = ImageTk.PhotoImage(load)
            img = Button(deleteMenuFrame, image=render, borderwidth=0, highlightthickness=0,
                         highlightbackground="#e7e7e7",
                         command=lambda: [frame.pack(expand=True, fill='both'),
                                          viewDetailsFrame.pack_forget(),
                                          deleteMenuFrame.pack_forget(),
                                          viewRecipeFrame.pack_forget()])
            img.image = render
            img.pack(side=LEFT)
            label = Label(deleteMenuFrame, text="View Recipe", font=LARGE_FONT, bg="#e7e7e7", fg="#272822")
            label.pack(side=LEFT, padx=300)

            Button(deleteMenuFrame, text="Delete", highlightbackground="#e7e7e7",
                   command=lambda: delete_recipe(name)).pack(side=RIGHT)

            viewDetailsFrame.pack(expand=True, fill='both')
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
                        Label(viewDetailsFrame, text=string, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000").pack(side=TOP)
            conn.close()

        def delete_recipe(recipeName):
            database_file = "meal_planner.db"

            now = datetime.datetime.now()
            dt = datetime.date(now.year, now.month, now.day)
            weekNumber = dt.isocalendar()[1]

            tableName = "recipes_" + str(weekNumber)
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                cursor.execute("""SELECT count(*) FROM """ + tableName + """ WHERE recipe = ?;""", (recipeName, ))
                returnObject = cursor.fetchone()[0]
                if returnObject == 0:
                    actually_delete(recipeName)
                    print("there is no component named {}".format(recipeName))
                else:
                    print("component {} found".format(recipeName))
                    messagebox.showerror("Cannot Delete",
                                         "Cannot delete recipe when it's used in the current week's menu.")

        def actually_delete(recipeName):
            with sqlite3.connect("meal_planner.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""DELETE FROM recipe WHERE name = ?;""", (recipeName, ))
                if cursor.rowcount == 1:
                    messagebox.showinfo("Success", "Recipe Deleted.")
                    menuFrame.pack_forget()
                    deleteMenuFrame.pack_forget()
                    viewDetailsFrame.pack_forget()
                    viewRecipeFrame.pack_forget()
                    frame.pack(expand=True, fill='both')
                elif cursor.rowcount == 0:
                    messagebox.showerror("Cannot Delete", "Error.")
            conn.close()

