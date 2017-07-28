# Huge shoutout to youtube user: sentdex at https://www.youtube.com/watch?v=jBUpjijYtCk which
# helped me figure out how to do multiple pages with tkinter

from tkinter import *
from addRecipe import AddARecipe
from mealPlan import MakeMealPlan
from landingpage import LandingPage

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 12)


class main(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(fill="both", expand=TRUE)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}
        for my_frame in (LandingPage, AddARecipe, MakeMealPlan):
            frame = my_frame(container, self)
            self.frames[my_frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LandingPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

app = main()
app.maxsize(900,600)
app.minsize(900,600)
app.mainloop()