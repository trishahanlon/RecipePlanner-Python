from tkinter import *

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 12)

class addARecipe(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Add a Recipe Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        name = StringVar()
        time = IntVar()
        servings = IntVar()
        favoriteVar = IntVar()

        recipeNameLabel = Label(self, text="Recipe Name", font=MEDIUM_FONT)
        recipeNameLabel.grid(row=1, column=0)
        recipeName = Entry(self, show="", textvariable=name)
        recipeName.grid(row=1, column=1)

        timeLabel = Label(self, text="Cook time (in mins)", font=MEDIUM_FONT)
        timeLabel.grid(row=2, column=0)
        time = Entry(self, show="", textvariable=time)
        time.grid(row=2, column=1)

        numberOfServingsLabel = Label(self, text="Number of Servings", font=MEDIUM_FONT)
        numberOfServingsLabel.grid(row=3, column=0)
        numberOfServings = Entry(self, show="", textvariable=servings)
        numberOfServings.grid(row=3, column=1)

        favoriteLabel = Label(self, text="Add to your favorites?", font=MEDIUM_FONT)
        favoriteLabel.grid(row=4, column=0)
        favoriteValue = Checkbutton(self, text="Favorite", variable=favoriteVar)
        favoriteValue.grid(row=4, column=1)

        ingredientsLabel = Label(self, text="Ingredients \n (quantity unit ingredient, i.e. 1 cup milk)", font=MEDIUM_FONT)
        ingredientsLabel.grid(row=5, column=0)

        directionsLabel = Label(self, text="Directions", font=MEDIUM_FONT)
        directionsLabel.grid(row=5, column=1)

        ingredients = Text(self, bg='#d3d3d3', width=30, height=20)
        ingredients.grid(row=6, column=0)

        directions = Text(self, bg='#d3d3d3', width=30, height=20)
        directions.grid(row=6, column=1)

        submitButton = Button(self, text="Submit Recipe", command = lambda: submit(name.get(), time.get(), servings.get(), favoriteVar.get(),
                                                                                      ingredients.get("1.0", END), directions.get("1.0", END)))
        submitButton.grid(row=7, column=0)

        from firstpage import firstPage
        createButton = Button(self, text="Return Home", command=lambda: controller.show_frame(firstPage))
        createButton.grid(row=8, column=0)

def submit(name, time, servings, favorite, ingredients, directions):
    print("Name: ", name)
    print("Time: ", time)
    print("servings: ", servings)
    print("favorite: ", favorite)
    print("ingredients: ", ingredients)
    print("directions: ", directions)