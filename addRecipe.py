from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

LARGE_FONT=("Trebuchet MS", 24)
MEDIUM_FONT=("Trebuchet MS", 12)

class addARecipe(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#f8f8f8")
        menuFrame = Frame(self, bg="#e7e7e7")
        menuFrame.grid( row=0, column=0)
        menuFrame.grid_columnconfigure(0, weight=0)
        menuFrame.grid_columnconfigure(1, weight=1)

        label = Label(menuFrame, text="Add a Recipe Page", font=LARGE_FONT, bg="#e7e7e7", fg="#272822")
        label.grid(row=0, column=1, columnspan=3, sticky="nsew")

        name = StringVar()
        time = StringVar()
        servings = StringVar()
        favoriteVar = IntVar()

        Label(self, text="Recipe Name", font=MEDIUM_FONT, bg="#f8f8f8",).grid(row=1, column=0)
        Entry(self, show="", textvariable=name, fg="#f8f8f8",).grid(row=1, column=1)

        Label(self, text="Cook time (in mins)", font=MEDIUM_FONT, bg="#f8f8f8",).grid(row=2, column=0)
        Entry(self, show="", textvariable=time, fg="#f8f8f8",).grid(row=2, column=1)

        Label(self, text="Number of Servings", font=MEDIUM_FONT, bg="#f8f8f8",).grid(row=3, column=0)
        Entry(self, show="", textvariable=servings, fg="#f8f8f8",).grid(row=3, column=1)

        Label(self, text="Add to your favorites?", font=MEDIUM_FONT, bg="#f8f8f8",).grid(row=4, column=0)
        Checkbutton(self, text="Favorite", variable=favoriteVar, bg="#f8f8f8",).grid(row=4, column=1)

        Label(self, text="Ingredients \n (quantity unit ingredient, i.e. 1 cup milk)", font=MEDIUM_FONT, bg="#f8f8f8",).grid(row=5, column=0)

        Label(self, text="Directions", font=MEDIUM_FONT, bg="#f8f8f8",).grid(row=5, column=1)

        ingredients = Text(self, bg='#d3d3d3', width=30, height=20)
        ingredients.grid(row=6, column=0)

        directions = Text(self, bg='#d3d3d3', width=30, height=20)
        directions.grid(row=6, column=1)


        submit_button = Button(self, text="Submit Recipe",highlightbackground="#f8f8f8", command = lambda: [(submit(name.get(), time.get(),
                                                                                          servings.get(), favoriteVar.get(),ingredients.get("1.0", END),
                                                                                          directions.get("1.0", END)), controller.show_frame(firstPage)),
                                                                              messagebox.showinfo("Success", "Successful saved to database.")])
        submit_button.grid(row=7, column=0)

        from firstpage import firstPage
        load = Image.open("home.jpg")
        render = ImageTk.PhotoImage(load)

        img = Button(menuFrame, image = render, borderwidth=0, highlightthickness=0, highlightbackground="#e7e7e7",
                     command=lambda: controller.show_frame(firstPage))
        img.image = render
        img.grid(row=0, column=0)

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


