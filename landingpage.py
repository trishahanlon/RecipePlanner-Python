from tkinter import *
from addRecipe import AddARecipe
from mealPlan import MakeMealPlan
from PIL import Image, ImageTk
import sqlite3

LARGE_FONT=("Trebuchet MS", 24)
MEDIUM_FONT=("Trebuchet MS", 12)


class LandingPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
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

            viewRecipeFrame = Frame(self, bg="#f8f8f8")
            viewRecipeFrame.pack(expand=True, fill='both')

            recipeNames = []
            database_file = "meal_planner.db"
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                selection = cursor.execute("""SELECT * FROM recipe""")
                for result in [selection]:
                    for row in result.fetchall():
                        name = row[0]
                        recipeNames.append(name)
            for i in range(len(recipeNames)):
                label = Label(viewRecipeFrame, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000", text=recipeNames[i])
                label.pack()
                label.bind("<Button-1>", lambda  event, x=recipeNames[i]: callback(x))

            def callback(recipeName):
                    viewRecipeFrame.pack_forget()

                    viewDetailsFrame = Frame(self, bg="#f8f8f8")
                    viewDetailsFrame.pack(expand=True, fill='both')
                    with sqlite3.connect(database_file) as conn:
                        cursor = conn.cursor()
                        selection = cursor.execute("""SELECT * FROM recipe WHERE name = """ + "\"" + recipeName + "\"" )
                        for result in [selection]:
                            for row in result.fetchall():
                                name = row[0]
                                time = row[1]
                                servings = row[2]
                                favorite = row[3]
                                ingredients = row[4]
                                directions = row[5]
                        string = ("Name: {} \n Cook time: {} \n Number of Servings: {} \n Ingredients: {} \n Directions: {}".format(name, time, servings, ingredients, directions))
                        Label(viewDetailsFrame, text=string, font=MEDIUM_FONT, bg="#f8f8f8", fg="#000000").pack(side=LEFT)

                    conn.close()

                    ##need to figure out the positioning of this button.
                    Button(viewDetailsFrame, text="Home", highlightbackground="#f8f8f8",
                           command=lambda: [viewDetailsFrame.pack_forget(), frame.pack(expand=True, fill='both')]).pack(side=TOP)



