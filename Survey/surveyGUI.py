"""Survey Code that has a GUI"""

import tkinter as tk
import json


class SurveyApp:
    def __init__(self, root):

        self.root = root
        root.title("Sustainability Survey")
        root.configure(bg='#96c896')

        # Question 1: Budget
        budget_label = tk.Label(
            root, text="What is your current budget?", bg='#96c896')
        budget_label.pack()
        budget_options = ["Low", "Middle", "High"]
        self.budget_var = tk.StringVar(root)
        self.budget_var.set(budget_options[0])
        budget_menu = tk.OptionMenu(root, self.budget_var, *budget_options)
        budget_menu.config(bg='#96c896')
        budget_menu.pack()

        # Question 2: Living situation
        living_label = tk.Label(
            root, text="Do you rent or own your home?", bg='#96c896')
        living_label.pack()
        living_options = ["rent", "own"]
        self.living_var = tk.StringVar(root)
        self.living_var.set(living_options[0])
        living_menu = tk.OptionMenu(root, self.living_var, *living_options)
        living_menu.config(bg='#96c896')
        living_menu.pack()

        # Question 3: Location
        location_label = tk.Label(
            root, text="Do you live in an urban or rural area?", bg='#96c896')
        location_label.pack()
        location_options = ["urban", "rural"]
        self.location_var = tk.StringVar(root)
        self.location_var.set(location_options[0])
        location_menu = tk.OptionMenu(
            root, self.location_var, *location_options)
        location_menu.config(bg='#96c896')
        location_menu.pack()

        # Question 4: Diet
        diet_label = tk.Label(root, text="What is your diet?", bg='#96c896')
        diet_label.pack()
        diet_options = ["Vegan", "Vegetarian",
                        "Pescatarian", "Omnivore", "N/A"]
        self.diet_var = tk.StringVar(root)
        self.diet_var.set(diet_options[0])
        diet_menu = tk.OptionMenu(root, self.diet_var, *diet_options)
        diet_menu.config(bg='#96c896')
        diet_menu.pack()

        # Question 5: Primary Transportation
        transport_label = tk.Label(
            root, text="What is your primary mode of transportation?", bg='#96c896')
        transport_label.pack()
        transport_options = ["Car", "Public transportation", "Bike", "Walk"]
        self.transport_var = tk.StringVar(root)
        self.transport_var.set(transport_options[0])
        transport_menu = tk.OptionMenu(
            root, self.transport_var, *transport_options)
        transport_menu.config(bg='#96c896')
        transport_menu.pack()

      # Question 6: Current practices
        current_label = tk.Label(
            root, text="Do you currently do any of the following?", bg='#96c896')
        current_label.pack()
        self.compost_var = tk.BooleanVar(root)
        self.recycle_var = tk.BooleanVar(root)
        self.zerowaste_purchasing_var = tk.BooleanVar(root)
        self.zerowaste_lifestyle_var = tk.BooleanVar(root)
        self.shoplocal_var = tk.BooleanVar(root)
        self.producefood_var = tk.BooleanVar(root)
        compost_checkbox = tk.Checkbutton(
            root, text="Compost", bg='#96c896', variable=self.compost_var)
        compost_checkbox.pack()
        recycle_checkbox = tk.Checkbutton(
            root, text="Recycle",  bg='#96c896', variable=self.recycle_var)
        recycle_checkbox.pack()
        zerowaste_purchasing_checkbox = tk.Checkbutton(
            root, text="Practice zero waste purchasing", bg='#96c896', variable=self.zerowaste_purchasing_var)
        zerowaste_purchasing_checkbox.pack()
        zerowaste_lifestyle_checkbox = tk.Checkbutton(
            root, text="Practice zero waste lifestyle", bg='#96c896', variable=self.zerowaste_lifestyle_var)
        zerowaste_lifestyle_checkbox.pack()
        shoplocal_checkbox = tk.Checkbutton(
            root, text="Shop local", bg='#96c896', variable=self.shoplocal_var)
        shoplocal_checkbox.pack()
        producefood_checkbox = tk.Checkbutton(
            root, text="Produce your own food", bg='#96c896', variable=self.producefood_var)
        producefood_checkbox.pack()

        # Submit button
        submit_button = tk.Button(
            root, text="Submit", bg='#96c896', width=10, command=self.submit)
        submit_button.pack()

        # Chat Display box (used by AI in future?)
        self.textbox = tk.Text(root, height=2, wrap="word", bg="white",
                               padx=5, pady=5, borderwidth=2, relief="groove")
        self.textbox.pack(side=tk.BOTTOM, fill=tk.X)
        self.textbox.insert(tk.END, "Welcome to the Sustainability Survey!")
        self.textbox.tag_configure("center", justify="center")
        self.textbox.tag_add("center", "1.0", "end")

    def submit(self):

        # Get user responses
        budget = self.budget_var.get()
        living_situation = self.living_var.get()
        location = self.location_var.get()
        diet = self.diet_var.get()
        transportation = self.transport_var.get()
        compost = self.compost_var.get()
        recycle = self.recycle_var.get()
        zerowaste_purchasing = self.zerowaste_purchasing_var.get()
        zerowaste_lifestyle = self.zerowaste_lifestyle_var.get()
        shoplocal = self.shoplocal_var.get()
        producefood = self.producefood_var.get()

        # Create dictionary of user responses
        user_responses = {
            "budget": budget,
            "living_situation": living_situation,
            "location": location,
            "diet": diet,
            "transportation": transportation,
            "compost": compost,
            "recycle": recycle,
            "zerowaste_purchasing": zerowaste_purchasing,
            "zerowaste_lifestyle": zerowaste_lifestyle,
            "shoplocal": shoplocal,
            "producefood": producefood
        }

        # Save user responses to JSON file
        with open('survey_responses.json', 'w') as f:
            json.dump(user_responses, f)

        # Show confirmation message to user
        # Clear the text box
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert(
            tk.END, "You have successfully submitted, thank you.")

        # Reset all the selected values to their defaults
        self.budget_var.set("Select one")
        self.living_var.set("Select one")
        self.location_var.set("Select one")
        self.diet_var.set("Select one")
        self.transport_var.set("Select one")
        self.compost_var.set(False)
        self.recycle_var.set(False)
        self.zerowaste_purchasing_var.set(False)
        self.zerowaste_lifestyle_var.set(False)
        self.shoplocal_var.set(False)
        self.producefood_var.set(False)

    def run(self):
        # start the GUI event loop
        self.root.mainloop()
