from tkinter import *
from calendary import Calendary
import calendar
import datetime
from isoweek import Week
from tkinter import ttk

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 14)

NOW = datetime.datetime.now()

class makeMealPlan(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Make Meal Page", font=LARGE_FONT).grid(row=0, column=0)

        dt = datetime.date(NOW.year, NOW.month, NOW.day)
        weekNumber = dt.isocalendar()[1]
        w = Week(NOW.year, weekNumber)
        print ("Week %s starts on %s and ends on %s" % (w, w.monday(), w.sunday()))

        cal_x = calendar.month(NOW.year, NOW.month, w=2, l=1)
        cal_out = Label(
            self,
            bg='#d3d3d3',
            font=('courier', 12),
            justify=LEFT,
            text=cal_x
        )
        cal_out.grid(row=1, column=0, columnspan=2)


        menu = Frame(self)
        menu.rowconfigure(0, weight=1)
        menu.columnconfigure(0, weight=1)
        menu.rowconfigure(1, weight=3)
        menu.columnconfigure(1, weight=3)

        columnLabels = ["Breakfast", "Lunch", "Dinner"]
        for i in range(len(columnLabels)):
            Label(menu, text = columnLabels[i], font = ("Verdana", 16), fg= "#d3d3d3").grid(row=1, column=i+2, pady= 10,
                                                                                        padx=85, sticky="nsew")

        mondayText = "Monday " + str(w.monday())
        tuesdayText = "Tuesday " + str(w.tuesday())
        wednesdayText = "Wednesday " + str(w.wednesday())
        thursdayText = "Thursday " + str(w.thursday())
        fridayText = "Friday " + str(w.friday())
        saturdayText = "Saturday " + str(w.saturday())
        sundayText = "Sunday " + str(w.sunday())

        labels = [mondayText, tuesdayText, wednesdayText, thursdayText, fridayText, saturdayText, sundayText]
        for i in range(len(labels)):
            Label(menu, text = labels[i]).grid(row=i+2, column=0, padx = 5, pady=15, sticky="w")
            sep = ttk.Separator(menu, orient="vertical")
            sep.grid(row=i+2, column=1, padx=5, sticky="nsew")

        menu.grid(row=2, column=0)

        from firstpage import firstPage
        createButton = Button(self, text="Return Home", command=lambda: controller.show_frame(firstPage))
        createButton.grid(row=9, column=0)