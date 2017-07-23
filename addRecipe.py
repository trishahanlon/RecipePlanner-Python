import tkinter as tk
import view

def addEntry():
    entry_frame = tk.Frame(view.main)
    entry_frame.pack(fill=tk.X)

    label = tk.Label(entry_frame, font=("Helvetica", 24), text = "Trisha's Meal Planner")
    label.grid(row=0, column=0)