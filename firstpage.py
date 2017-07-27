from tkinter import *
from addRecipe import addARecipe
from mealPlan import makeMealPlan
from PIL import Image, ImageTk

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 12)


class firstPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # root = self
        label = Label(self, text="Trisha's Meal Planner", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky = "nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        load = Image.open("recipe_card.jpg")
        render = ImageTk.PhotoImage(load)

        img = Label(self, image = render)
        img.image = render
        img.grid(row=1, column=0)

        Button(self, text="Add A Recipe", command=lambda: controller.show_frame(addARecipe)).grid(row=2, column=0, sticky = "nsew")
        Button(self, text="Make a Meal Plan", command=lambda: controller.show_frame(makeMealPlan)).grid(row=2, column=1, sticky = "nsew")