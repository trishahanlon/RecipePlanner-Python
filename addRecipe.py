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
        menu_frame = Frame(self, bg="#e7e7e7")
        menu_frame.pack(fill='both')
        from landingpage import LandingPage
        load = Image.open("home.jpg")
        render = ImageTk.PhotoImage(load)
        img = Button(menu_frame, image = render, borderwidth=0, highlightthickness=0, highlightbackground="#e7e7e7",
                     command=lambda: controller.show_frame(LandingPage))
        img.image = render
        img.pack(side=LEFT)
        label = Label(menu_frame, text="Add a Recipe", font=LARGE_FONT, bg="#e7e7e7", fg="#272822")
        label.pack(side=LEFT, padx=300)

        #
        # Middle
        #
        name = StringVar()
        time = StringVar()
        servings = StringVar()
        favoriteVar = IntVar()

        middle_frame = Frame(self, bg="#f8f8f8")
        middle_frame.pack(expand=True, fill='both', padx=300)

        label_frame = Frame(middle_frame, bg="#f8f8f8")
        label_frame.pack(side=LEFT)

        entry_frame = Frame(middle_frame, bg="#f8f8f8")
        entry_frame.pack(side=LEFT)

        Label(label_frame, text="Recipe Name: ", font=MEDIUM_FONT, bg="#f8f8f8").pack(pady=4,expand=NO)
        name_entry = Entry(entry_frame, show="", textvariable=name, bg="#ffffff", fg="#000000")
        name_entry.pack(pady=1, expand=YES)

        Label(label_frame, text="Cook time (in mins): ", font=MEDIUM_FONT, bg="#f8f8f8").pack(pady=4, expand=NO)
        time_entry = Entry(entry_frame, show="", textvariable=time, bg="#ffffff", fg="#000000")
        time_entry.pack(pady=1, expand=YES)

        Label(label_frame, text="Number of Servings: ", font=MEDIUM_FONT, bg="#f8f8f8").pack(pady=5, expand=NO)
        servings_entry = Entry(entry_frame, show="", textvariable=servings, bg="#ffffff", fg="#000000")
        servings_entry.pack(pady=1, expand=YES)

        #
        # Bottom
        #
        bottomFrame = Frame(self, bg="#f8f8f8")
        bottomFrame.pack(fill='both')

        Label(bottomFrame, text="Add to your favorites?", font=MEDIUM_FONT, bg="#f8f8f8",).pack(side=TOP)
        Checkbutton(bottomFrame, text="Favorite", font=MEDIUM_FONT, variable=favoriteVar, bg="#f8f8f8").pack(side=TOP)

        left_frame = Frame(bottomFrame, bg="#f8f8f8")
        left_frame.pack(side=LEFT, padx=50)
        Label(left_frame, text="Ingredients \n (quantity unit ingredient, i.e. 1 cup milk)", font=MEDIUM_FONT, bg="#f8f8f8").pack(side=TOP, expand=YES)
        ingredients_text = Text(left_frame, bg='#d3d3d3', width=50, height=20)
        ingredients_text.pack(fill=Y, side=LEFT)

        right_frame = Frame(bottomFrame, bg="#f8f8f8")
        right_frame.pack(side=RIGHT, padx=50)
        Label(right_frame, text="Directions \n", font=MEDIUM_FONT, bg="#f8f8f8").pack(side=TOP, expand=YES)
        directions_text = Text(right_frame, bg='#d3d3d3', width=50, height=20)
        directions_text.pack(fill=Y, side=RIGHT)


        submit_button = Button(self, text="Submit Recipe", highlightbackground="#f8f8f8", command = lambda: [(submit(name.get(), time.get(),
                                                                                          servings.get(), favoriteVar.get(),ingredients_text.get("1.0", END),
                                                                                          directions_text.get("1.0", END)))])
        submit_button.pack()

        def submit(name, time, servings, favorite, ingredients, directions):

            database_file = "meal_planner.db"
            if len(name) == 0 or len(time) == 0 or len(servings) == 0 or len(ingredients) == 0 or len(directions) == 0:
                messagebox.showerror("Missing Value", "All fields must be completed.")
            else:
                try:
                    int_time = int(time)
                    try:
                        int_servings = int(servings)
                        with sqlite3.connect(database_file) as conn:
                            # create the table if it hasn't been created yet
                            conn.execute('''CREATE TABLE IF NOT EXISTS recipe
                                 (name text, time int, servings int, favorite text, ingredients text, directions text)''')
                            conn.execute("""INSERT INTO recipe VALUES (?, ?, ?, ?, ?, ?);""",
                                         (name, int_time, int_servings, favorite, ingredients, directions))
                            name_entry.delete(0, END)
                            servings_entry.delete(0, END)
                            time_entry.delete(0,END)
                            ingredients_text.delete(1.0, END)
                            directions_text.delete(1.0, END)
                        messagebox.showinfo("Success", "Recipe Added.")
                        controller.show_frame(LandingPage)
                    except ValueError:
                        messagebox.showerror("Incorrect Value", "Servings must be an int")
                except ValueError:
                    messagebox.showerror("Incorrect Value", "Time must be an int")


