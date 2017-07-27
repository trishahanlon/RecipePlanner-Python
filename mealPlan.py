from tkinter import *
import calendar
import datetime
from isoweek import Week
from tkinter import ttk
import sqlite3

LARGE_FONT=("Verdana", 24)
MEDIUM_FONT=("Verdana", 14)

NOW = datetime.datetime.now()

class makeMealPlan(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label(self, text="Make Meal Page", font=LARGE_FONT).grid(row=0, column=0)

        dt = datetime.date(NOW.year, NOW.month, NOW.day)
        weekNumber = dt.isocalendar()[1]
        w = Week(NOW.year, weekNumber)

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
        menu.grid(row=2, column=0)

        columnLabels = ["Breakfast", "Lunch", "Dinner"]
        for i in range(len(columnLabels)):
            Label(menu, text = columnLabels[i], font = ("Verdana", 16), fg= "#d3d3d3").grid(row=0, column=i+2, pady= 10,
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
            Label(menu, text = labels[i]).grid(row=i+1, column=0, padx = 5, pady=15, sticky="w")
            sep = ttk.Separator(menu, orient="vertical")
            sep.grid(row=i+1, column=1, padx=5, sticky="nsew")

        buttonDict = {}
        listOfButtons = []
        for rows in range(len(labels)):
            for columns in range(len(columnLabels)):
                # buttons = Button(menu, text="Add meal to day", command=lambda x=rows+1, y=columns+2: addMeal(x, y))
                buttons = Button(menu, text="Add meal to day", command=lambda x=rows + 1, y=columns + 2: addMeal(x, y))
                buttons.grid(row=rows+1, column=columns+2)
                buttons.position = (rows+1, columns+2)
                buttonDict[buttons] = buttons.position
                listOfButtons.append(buttons)

        def addMeal(rowLocation, columnLocation):
            menu.grid_forget()
            addMealFrame = Frame(self)
            addMealFrame.rowconfigure(0, weight=1)
            addMealFrame.columnconfigure(0, weight=1)
            addMealFrame.rowconfigure(1, weight=3)
            addMealFrame.columnconfigure(1, weight=3)
            addMealFrame.grid(row=2, column=0)

            recipeNames = []

            database_file = "meal_planner.db"
            with sqlite3.connect(database_file) as conn:
                cursor = conn.cursor()
                selection = cursor.execute("""SELECT * FROM recipe""")
                for result in [selection]:
                    for row in result.fetchall():
                        name = row[0]
                        time = row[1]
                        servings = row[2]
                        favorite = row[3]
                        ingredients = row[4]
                        directions = row[5]
                        print (name, time, servings, favorite, ingredients, directions)
                        recipeNames.append(name)

            for i in range(len(recipeNames)):
                Button(addMealFrame, text=recipeNames[i], command=lambda x = recipeNames[i]:newFunction(x, addMealFrame,
                                                                                     rowLocation, columnLocation)).grid(row=i, column=0)

        def newFunction(recipe, view, row, column):
            print(recipe)
            view.grid_forget()
            searchIndex = (row, column)
            for key, value in buttonDict.items():
                if value == searchIndex:
                    key.destroy()
            recipeLabel = Label(menu, text=recipe)
            recipeLabel.grid(row = row, column = column)
            menu.grid()

        from firstpage import firstPage
        Button(self, text="Return Home", command=lambda: controller.show_frame(firstPage)).grid(row=9, column=0)