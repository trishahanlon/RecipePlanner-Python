# Huge shoutout to youtube user: sentdex at https://www.youtube.com/watch?v=jBUpjijYtCk which
# helped me figure out how to do multiple pages with tkinter

import tkinter as tk

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 12)

class mealPlanner(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width=1000, height=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for my_frame in (firstPage, addARecipe, makeMealPlan):
            frame = my_frame(container, self)
            self.frames[my_frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(firstPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class firstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        createButton = tk.Button(self, text="Add A Recipe", command=lambda: controller.show_frame(addARecipe))
        createButton.grid(row=1, column=0)

        weeklyPlan = tk.Button(self, text="Make a Meal Plan", command=lambda: controller.show_frame(makeMealPlan))
        weeklyPlan.grid(row=1, column=1)

def submit(name, time, servings, favorite, ingredients, directions):
    print("Name: ", name)
    print("Time: ", time)
    print("servings: ", servings)
    print("favorite: ", favorite)
    print("ingredients: ", ingredients)
    print("directions: ", directions)

class addARecipe(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Add a Recipe Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        name = tk.StringVar()
        time = tk.IntVar()
        servings = tk.IntVar()
        favoriteVar = tk.IntVar()

        recipeNameLabel = tk.Label(self, text="Recipe Name", font=MEDIUM_FONT)
        recipeNameLabel.grid(row=1, column=0)
        recipeName = tk.Entry(self, show="", textvariable=name)
        recipeName.grid(row=1, column=1)

        timeLabel = tk.Label(self, text="Cook time (in mins)", font=MEDIUM_FONT)
        timeLabel.grid(row=2, column=0)
        time = tk.Entry(self, show="", textvariable=time)
        time.grid(row=2, column=1)

        numberOfServingsLabel = tk.Label(self, text="Number of Servings", font=MEDIUM_FONT)
        numberOfServingsLabel.grid(row=3, column=0)
        numberOfServings = tk.Entry(self, show="", textvariable=servings)
        numberOfServings.grid(row=3, column=1)

        favoriteLabel = tk.Label(self, text="Add to your favorites?", font=MEDIUM_FONT)
        favoriteLabel.grid(row=4, column=0)
        favoriteValue = tk.Checkbutton(self, text="Favorite", variable=favoriteVar)
        favoriteValue.grid(row=4, column=1)

        ingredientsLabel = tk.Label(self, text="Ingredients \n (quantity unit ingredient, i.e. 1 cup milk)", font=MEDIUM_FONT)
        ingredientsLabel.grid(row=5, column=0)

        directionsLabel = tk.Label(self, text="Directions", font=MEDIUM_FONT)
        directionsLabel.grid(row=5, column=1)

        ingredients = tk.Text(self, bg='#d3d3d3', width=30, height=20)
        ingredients.grid(row=6, column=0)

        directions = tk.Text(self, bg='#d3d3d3', width=30, height=20)
        directions.grid(row=6, column=1)

        submitButton = tk.Button(self, text="Submit Recipe", command = lambda: submit(name.get(), time.get(), servings.get(), favoriteVar.get(),
                                                                                      ingredients.get("1.0", tk.END), directions.get("1.0", tk.END)))
        submitButton.grid(row=7, column=0)


        createButton = tk.Button(self, text="Return Home", command=lambda: controller.show_frame(firstPage))
        createButton.grid(row=8, column=0)


class makeMealPlan(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Make Meal Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        createButton = tk.Button(self, text="Return Home", command=lambda: controller.show_frame(firstPage))
        createButton.grid(row=1, column=0)


app = mealPlanner()
app.maxsize(1000,6000)
app.minsize(1000,600)
app.mainloop()