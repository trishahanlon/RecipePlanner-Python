from tkinter import *

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 12)

class makeMealPlan(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Make Meal Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        from firstpage import firstPage
        createButton = Button(self, text="Return Home", command=lambda: controller.show_frame(firstPage))
        createButton.grid(row=1, column=0)