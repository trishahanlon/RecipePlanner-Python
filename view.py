import tkinter as tk

LARGE_FONT=("Verdana", 12)

class mealPlanner(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width=1000, height=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for my_frame in (firstPage, secondPage):
            print("whatever")
            frame = my_frame(container, self)
            self.frames[my_frame] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(firstPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class firstPage(tk.Frame):
    print("firstPage")
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        createButton = tk.Button(self, text="Add A Recipe", command=lambda: controller.show_frame(secondPage))
        createButton.pack()

        weeklyPlan = tk.Button(self, text="Make a Meal Plan", command=lambda: controller.show_frame(secondPage))
        weeklyPlan.pack()


class secondPage(tk.Frame):
    print("secondpage")
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Second Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

app = mealPlanner()
app.maxsize(1000,6000)
app.minsize(1000,600)
app.mainloop()