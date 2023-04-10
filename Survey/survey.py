"""" Survey Applicaiotn for AI (Basic set up) in terminal"""

print(" ~ Sustainability Survey ~ ")
print("Answer the following questions to help SAGE tailor its advice")

# Question 1: Budget
budget = input("What is your budget? (Low, Middle, or High) ")
while budget not in ["Low", "Middle", "High"]:
    budget = input("Invalid input. Please enter either Low, Middle, or High. ")
print(f"Your budget is {budget}.")

# Question 2: Living situation
living_situation = input("Do you rent or own your home? ")
while living_situation not in ["rent", "own"]:
    living_situation = input(
        "Invalid input. Please enter either rent or own. ")
print(f"You {living_situation} your home.")

# Question 3: Location
location = input("Do you live in an urban or rural area? ")
while location not in ["urban", "rural"]:
    location = input("Invalid input. Please enter either urban or rural. ")
print(f"You live in a {location} area.")

# Question 4: Diet
print("What is your diet?")
print("1. Vegan")
print("2. Vegetarian")
print("3. Pescatarian")
print("4. Omnivore")
print("5. N/A")
diet_option = input("Enter your choice (1-5): ")
while diet_option not in ["1", "2", "3", "4", "5"]:
    diet_option = input("Invalid input. Please enter a number from 1-5. ")
diet_options = ["Vegan", "Vegetarian", "Pescatarian", "Omnivore", "N/A"]
diet = diet_options[int(diet_option) - 1]
print(f"Your diet is {diet}.")

# Question 5: Primary Transportation
print("What is your primary mode of transportation?")
print("1. Car")
print("2. Public transportation")
print("3. Bike")
print("4. Walk")
transport_option = input("Enter your choice (1-4): ")
while transport_option not in ["1", "2", "3", "4"]:
    transport_option = input("Invalid input. Please enter a number from 1-4. ")
transport_options = ["Car", "Public transportation", "Bike", "Walk"]
transport = transport_options[int(transport_option) - 1]
print(f"Your primary mode of transportation is {transport}.")

# Question 6: Current practices
print("Do you currently do any of the following?")
print("Check all that apply:")
print("1. Compost")
print("2. Recycle")
print("3. Practice zero waste purchasing")
print("4. Practice zero waste lifestyle")
print("5. Shop local")
print("6. Produce your own food")
current_practices = []
for i in range(1, 7):
    answer = input(f"Enter {i} for yes, or leave blank for no: ")
    if answer == str(i):
        current_practices.append(True)
    else:
        current_practices.append(False)
print("Your current practices are:")
if current_practices[0]:
    print("- Composting")
if current_practices[1]:
    print("- Recycling")
if current_practices[2]:
    print("- Practicing zero waste purchasing")
if current_practices[3]:
    print("- Practicing zero waste lifestyle")
if current_practices[4]:
    print("- Shopping local")
if current_practices[5]:
    print("- Producing your own food")
