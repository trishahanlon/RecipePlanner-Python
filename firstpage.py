from tkinter import *
from addRecipe import addARecipe
from mealPlan import makeMealPlan
from PIL import Image, ImageTk

LARGE_FONT=("Trebuchet MS", 24)
MEDIUM_FONT=("Trebuchet MS", 12)

class firstPage(Frame):
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

        Button(frame, text="Add A Recipe", highlightbackground="#f8f8f8", command=lambda: controller.show_frame(addARecipe)).pack(fill=Y)
        Button(frame, text="Make a Meal Plan", highlightbackground="#f8f8f8", command=lambda: controller.show_frame(makeMealPlan)).pack(fill=Y)