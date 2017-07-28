from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

LARGE_FONT=("Trebuchet MS", 24)
MEDIUM_FONT=("Trebuchet MS", 12)


class AddARecipe(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="#f8f8f8")
        #
        # Menu
        #
        menuFrame = Frame(self, bg="#e7e7e7")
        menuFrame.pack(fill='both')
        from landingpage import LandingPage
        load = Image.open("home.jpg")
        render = ImageTk.PhotoImage(load)
        img = Button(menuFrame, image = render, borderwidth=0, highlightthickness=0, highlightbackground="#e7e7e7",
                     command=lambda: controller.show_frame(LandingPage))
        img.image = render
        img.pack(side=LEFT)
        label = Label(menuFrame, text="Add a Recipe", font=LARGE_FONT, bg="#e7e7e7", fg="#272822")
        label.pack(side=LEFT, padx=300)

        #
        # Middle
        #
        name = StringVar()
        time = StringVar()
        servings = StringVar()
        favoriteVar = IntVar()

        middleFrame = Frame(self, bg="#f8f8f8")
        middleFrame.pack(expand=True, fill='both', padx=300)

        labelFrame = Frame(middleFrame, bg="#f8f8f8")
        labelFrame.pack(side=LEFT)

        entryFrame = Frame(middleFrame, bg="#f8f8f8")
        entryFrame.pack(side=LEFT)

        Label(labelFrame, text="Recipe Name: ", font=MEDIUM_FONT, bg="#f8f8f8").pack(pady=4,expand=NO)
        Entry(entryFrame, show="", textvariable=name, bg="#ffffff", fg="#000000").pack(pady=1, expand=YES)

        Label(labelFrame, text="Cook time (in mins): ", font=MEDIUM_FONT, bg="#f8f8f8").pack(pady=4, expand=NO)
        Entry(entryFrame, show="", textvariable=time, bg="#ffffff", fg="#000000").pack(pady=1, expand=YES)

        Label(labelFrame, text="Number of Servings: ", font=MEDIUM_FONT, bg="#f8f8f8").pack(pady=5, expand=NO)
        Entry(entryFrame, show="", textvariable=servings, bg="#ffffff", fg="#000000").pack(pady=1, expand=YES)

        #
        # Bottom
        #
        bottomFrame = Frame(self, bg="#f8f8f8")
        bottomFrame.pack(fill='both')

        Label(bottomFrame, text="Add to your favorites?", font=MEDIUM_FONT, bg="#f8f8f8",).pack(side=TOP)
        Checkbutton(bottomFrame, text="Favorite", font=MEDIUM_FONT, variable=favoriteVar, bg="#f8f8f8").pack(side=TOP)

        leftFrame = Frame(bottomFrame, bg="#f8f8f8")
        leftFrame.pack(side=LEFT, padx=50)
        Label(leftFrame, text="Ingredients \n (quantity unit ingredient, i.e. 1 cup milk)", font=MEDIUM_FONT, bg="#f8f8f8").pack(side=TOP, expand=YES)
        ingredients = Text(leftFrame, bg='#d3d3d3', width=50, height=20)
        ingredients.pack(fill=Y, side=LEFT)

        rightFrame = Frame(bottomFrame, bg="#f8f8f8")
        rightFrame.pack(side=RIGHT, padx=50)
        Label(rightFrame, text="Directions \n", font=MEDIUM_FONT, bg="#f8f8f8").pack(side=TOP, expand=YES)
        directions = Text(rightFrame, bg='#d3d3d3', width=50, height=20)
        directions.pack(fill=Y, side=RIGHT)


        submit_button = Button(self, text="Submit Recipe", highlightbackground="#f8f8f8", command = lambda: [(submit(name.get(), time.get(),
                                                                                          servings.get(), favoriteVar.get(),ingredients.get("1.0", END),
                                                                                          directions.get("1.0", END)))])
        submit_button.pack()



        def submit(name, time, servings, favorite, ingredients, directions):
            print("Name: ", len(name))
            print("Time: ", len(time))
            print("servings: ", len(servings))
            print("favorite: ", favorite)
            print("ingredients: ", len(ingredients))
            print("directions: ", len(directions))

            database_file = "meal_planner.db"
            if len(name) == 0 or len(time) == 0 or len(servings) == 0 or len(ingredients) == 0 or len(directions) == 0:
                messagebox.showerror("Missing Value", "All fields must be completed.")
            else:
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

                        messagebox.showinfo("Success", "Recipe Added.")
                        controller.show_frame(LandingPage)
                    except ValueError:
                        messagebox.showerror("Incorrect Value", "Servings must be an int")
                except ValueError:
                    messagebox.showerror("Incorrect Value", "Time must be an int")


