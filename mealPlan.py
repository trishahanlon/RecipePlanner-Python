from tkinter import *
from calendary import Calendary
import calendar
import datetime
from isoweek import Week

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 12)

NOW = datetime.datetime.now()

class makeMealPlan(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Make Meal Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

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

        breakfast = Label(self, text="Breakfast", font = MEDIUM_FONT, fg='#d3d3d3')
        breakfast.grid(row=1, column=2,  sticky="s")

        lunch = Label(self, text="Lunch", font = MEDIUM_FONT, fg='#d3d3d3')
        lunch.grid(row = 1, column=3, sticky="s")

        dinner = Label(self, text="Dinner", font = MEDIUM_FONT, fg='#d3d3d3')
        dinner.grid(row = 1, column=4, sticky="s")

        mondayText = "Monday " + str(w.monday())
        tuesdayText = "Tuesday " + str(w.tuesday())
        wednesdayText = "Wednesday " + str(w.wednesday())
        thursdayText = "Thursday " + str(w.thursday())
        fridayText = "Friday " + str(w.friday())
        saturdayText = "Saturday " + str(w.saturday())
        sundayText = "Sunday " + str(w.sunday())

        monday = Label(self, text=mondayText, font=MEDIUM_FONT)
        monday.grid(row=2, column=0)

        tuesday = Label(self, text=tuesdayText, font=MEDIUM_FONT)
        tuesday.grid(row=3, column=0)

        wednesday = Label(self, text=wednesdayText, font=MEDIUM_FONT)
        wednesday.grid(row=4, column=0)

        thursday = Label(self, text=thursdayText, font=MEDIUM_FONT)
        thursday.grid(row=5, column=0)

        friday = Label(self, text=fridayText, font=MEDIUM_FONT)
        friday.grid(row=6, column=0)

        saturday = Label(self, text=saturdayText, font=MEDIUM_FONT)
        saturday.grid(row=7, column=0)

        sunday = Label(self, text=sundayText, font=MEDIUM_FONT)
        sunday.grid(row=8, column=0)


        from firstpage import firstPage
        createButton = Button(self, text="Return Home", command=lambda: controller.show_frame(firstPage))
        createButton.grid(row=9, column=0)