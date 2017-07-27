from tkinter import *
from tkinter import messagebox
import sqlite3

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 12)

class addARecipe(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Add a Recipe Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        name = StringVar()
        time = StringVar()
        servings = StringVar()
        favoriteVar = IntVar()

        Label(self, text="Recipe Name", font=MEDIUM_FONT).grid(row=1, column=0)
        Entry(self, show="", textvariable=name).grid(row=1, column=1)

        Label(self, text="Cook time (in mins)", font=MEDIUM_FONT).grid(row=2, column=0)
        Entry(self, show="", textvariable=time).grid(row=2, column=1)

        Label(self, text="Number of Servings", font=MEDIUM_FONT).grid(row=3, column=0)
        Entry(self, show="", textvariable=servings).grid(row=3, column=1)

        Label(self, text="Add to your favorites?", font=MEDIUM_FONT).grid(row=4, column=0)
        Checkbutton(self, text="Favorite", variable=favoriteVar).grid(row=4, column=1)

        Label(self, text="Ingredients \n (quantity unit ingredient, i.e. 1 cup milk)", font=MEDIUM_FONT).grid(row=5, column=0)

        Label(self, text="Directions", font=MEDIUM_FONT).grid(row=5, column=1)

        ingredients = Text(self, bg='#d3d3d3', width=30, height=20)
        ingredients.grid(row=6, column=0)

        directions = Text(self, bg='#d3d3d3', width=30, height=20)
        directions.grid(row=6, column=1)


        submit_button = Button(self, text="Submit Recipe", command = lambda: [(submit(name.get(), time.get(),
                                                                                          servings.get(), favoriteVar.get(),ingredients.get("1.0", END),
                                                                                          directions.get("1.0", END)), controller.show_frame(firstPage)),
                                                                              messagebox.showinfo("Success", "Successful saved to database.")])
        submit_button.grid(row=7, column=0)

        from firstpage import firstPage
        Button(self, text="Return Home", command=lambda: controller.show_frame(firstPage)).grid(row=8, column=0)

def submit(name, time, servings, favorite, ingredients, directions):
    print("Name: ", name)
    print("Time: ", time)
    print("servings: ", servings)
    print("favorite: ", favorite)
    print("ingredients: ", ingredients)
    print("directions: ", directions)


    database_file = "meal_planner.db"
    try:
        intTime = int(time)
        try:
            intServings = int(servings)
            with sqlite3.connect(database_file) as conn:
                # create the table if it hasn't been created yet
                conn.execute('''CREATE TABLE IF NOT EXISTS recipe
                     (name text, time int, servings int, favorite text, ingredients text, directions text)''')
                conn.execute("""INSERT INTO recipe VALUES (?, ?, ?, ?, ?, ?);""",
                             (name, intTime, intServings, favorite, ingredients, directions))
        except ValueError:
            messagebox.showerror("Incorrect Value", "Servings must be an int")
    except ValueError:
        messagebox.showerror("Incorrect Value", "Time must be an int")


