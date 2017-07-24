from tkinter import *
from addRecipe import addARecipe
from mealPlan import makeMealPlan

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 12)

class firstPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Start Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        createButton = Button(self, text="Add A Recipe", command=lambda: controller.show_frame(addARecipe))
        createButton.grid(row=1, column=0)

        weeklyPlan = Button(self, text="Make a Meal Plan", command=lambda: controller.show_frame(makeMealPlan))
        weeklyPlan.grid(row=1, column=1)