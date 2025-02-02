import csv
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
import mysql.connector
import math
import io
import plotly.graph_objects as go
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
import kaleido
# Functionality to pretty print dictionaries
import pprint
from colorama import Fore, init
from kivy import Config
import os

debugMode = True
writeFile = "./sampleInput.csv"
if debugMode :
    inputFile = "./premadeInput.csv"
else:
    inputFile = "./sampleInput.csv"


Config.set("graphics", "multisamples", "0")
os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


# Coloured text and pretty print for debug
init(convert=True, autoreset=True)
pp = pprint.PrettyPrinter(indent=4)

cnx = mysql.connector.connect(
    username="root", password="root", host="localhost", database="kitcritic"
)
curs = cnx.cursor()

###// HARD CODED REFERENCE VALUES ###

# Max weight in grams (13 kg as per data online)
# We need to fix this to consider large party sizes, maybe more bags?
maxWeight = 13000

# Required amount of calories per day
"""
In implementing the revised MOU (March 1997), WFP and UNHCR will follow the WHO
Guidelines and use 2,100 kilocalories as the initial reference value for calculating energy
requirements and designing food aid rations for the affected populations in emergency
situations.

- WHO
"""
dailyCal = 2100
# Required amount of water per day
"""
Store at least 1 gallon of water per person, per day for 3 days (Approx 3700 ml). 
You can use this water during an emergency for drinking, cooking, brushing teeth, and other uses. 
Try to store a 2-week supply if possible.

- CDC
"""
dailyWater = 3700

# Bictionary of categories and their totals
categoryTotals = {
    "Lighting and Illumination": 13,
    "Power and Batteries": 15,
    "Tools and Equipment": 61,
    "Fire and Warmth": 14,
    "Navigation and Signaling": 18,
    "Medical Supplies": 36,
    "Hygiene and Sanitation": 31,
    "Documentation and Emergency Funds": 9,
    "Shelter and Clothing": 9,
    "Water": 100,
    "Food": 100,
}


# This function find the amount needed for the family size and days
def modifyDaily(fi):
    global dailyWater, dailyCal
    # print(f"OG REQ AMOUNT : water {dailyWater}, calories {dailyCal}")
    with open(fi, "r") as fileObject:
        csvObject = csv.reader(fileObject)
        next(csvObject, None)  # skip the headers
        for i in csvObject:
            familyMembers = i[0]
            days = i[1]

        totalReq = float(familyMembers) * float(days)

        dailyWater *= totalReq
        dailyCal *= totalReq

        return f"There are {familyMembers} people in your party, and you will be surving {days} days"


# To calculate the weighted average
weightage = {
    # Utility items make up 50% of the score
    "Lighting and Illumination": 5,
    "Power and Batteries": 5,
    "Tools and Equipment": 7,
    "Fire and Warmth": 6,
    "Navigation and Signaling": 5,
    "Medical Supplies": 8,
    "Hygiene and Sanitation": 7,
    "Documentation and Emergency Funds": 3,
    "Shelter and Clothing": 4,
    # Food and water make up the other 50
    "Food": 20,
    "Water": 30,
}

### HARD CODED REFERENCE VALUES //###

# Dictionary to hold how much the user earnt
categoryScores = {
    "Lighting and Illumination": 0,
    "Power and Batteries": 0,
    "Tools and Equipment": 0,
    "Fire and Warmth": 0,
    "Navigation and Signaling": 0,
    "Medical Supplies": 0,
    "Hygiene and Sanitation": 0,
    "Documentation and Emergency Funds": 0,
    "Shelter and Clothing": 0,
}

# Dictionary of the percentage the user earnt per category
categoryPercentage = {
    "Lighting and Illumination": 0,
    "Power and Batteries": 0,
    "Tools and Equipment": 0,
    "Fire and Warmth": 0,
    "Navigation and Signaling": 0,
    "Medical Supplies": 0,
    "Hygiene and Sanitation": 0,
    "Food": 0,
    "Water": 0,
    "Documentation and Emergency Funds": 0,
    "Shelter and Clothing": 0,
}


# Function to retrieve data (NAZIA)
def getData(condition, request, table):
    # c = input("Enter the item you want to fetch data for: ")
    # v = input("Enter the data you want to retrieve from the item: ")
    curs.execute(f'SELECT {request} FROM {table} WHERE Item = "{condition}"')
    fetched = curs.fetchall()
    # If no empty value
    if fetched:
        return fetched[0][0]
    else:
        pass


# Function to get required (NAZIA)

# This function reads the CSV containing what Utilities are in the kit, and builds a dictionary to use in code.
extract = {}


def extractKitUtil(fi):
    with open(fi, "r") as fileObject:
        csvObject = csv.reader(fileObject)
        next(csvObject, None)  # skip the headers

        global extract

        # Note : Returns as nested tuples, hence we extract with [0][0]
        for i in csvObject:
            # if none is returned, ignore
            if not getData(i[0], "Category", "utility"):
                continue
            icat = getData(i[0], "Category", "utility")
            iscore = getData(i[0], "SurvivalScore", "utility")
            ireq = getData(i[0], "Required", "utility")
            iweight = getData(i[0], "WeightGram", "utility")
            imax = getData(i[0], "MaxPerPerson", "utility")
            iquant = i[1]

            out = {
                "Category": icat,
                "SurvivalScore": iscore,
                "Required": ireq,
                "WeightGram": iweight,
                "MaxPerPerson": imax,
                "Quantity": iquant,
            }

            extract[i[0]] = out

        return extract


# Function to aggregrate the score
def sumScore():
    for i in extract:
        iScore = extract[i]["SurvivalScore"]
        cat = extract[i]["Category"]
        categoryScores[cat] += iScore


# This function gives percentage for each category
def percentagePerCategory():
    global categoryPercentage
    for i in categoryPercentage:
        # Percentage = x / total * 100, rounded to 2 decimal places
        unWeight = round(categoryScores[i] / categoryTotals[i] * 100, 2)

        # If percentage is over 100, then just set it to 100. Same with negative scores
        if unWeight > 100:
            unWeight = 100
        elif unWeight <= 0:
            unWeight = 0

        categoryPercentage[i] = str(unWeight) + "%"


# This function gives the overall weighted score
def weightScore():
    finalScore = 0
    for i in categoryScores:
        # WeightedPercent = Percentage * (Weightage/100)
        # [-1] to not consider the percentage symbol
        weighted = float(categoryPercentage[i][:-1]) * (weightage[i] / 100)
        # Round down to 2 decimals
        weightedRound = round(weighted, 2)
        # Add it to final score
        finalScore += weightedRound

    return f"Your final score is {finalScore}%"


# This function normalizes for the quantity ie. Checks for too many items
def weightMaxCheck():
    # pp.pprint(extract)
    for i in extract:
        amountInKit = int(extract[i]["Quantity"])
        maxAmount = int(extract[i]["MaxPerPerson"])
        itemCat = extract[i]["Category"]

        # If there is exact amount or none at all, score stays the same
        if amountInKit == 1 or amountInKit == 0:
            pass
        # If the amount is less than the max, and they did not put in only 1, we will reward them
        elif amountInKit <= maxAmount:
            # We account for any extra
            reward = amountInKit - 1
            categoryScores[itemCat] += reward
        # IF they go over limit, we must punish them >:)
        elif amountInKit > maxAmount:
            # Lower score for however much excess they put in
            punish = amountInKit - maxAmount
            categoryScores[itemCat] -= punish


# This function calculates the calories
def getTotCal(fi):
    with open(fi, "r") as fileObject:
        csvObject = csv.reader(fileObject)
        totCal = 0
        # Note : Returns as nested tuples, hence we extract with [0][0]
        for i in csvObject:
            ical = getData(i[0], "Calorie", "food")
            if ical is not None:
                # Multiply by quantitiy
                ical *= int(i[1])
                totCal += ical
        return totCal


# This function calculate the amount of water in ml
def getTotWater(fi):
    with open(fi, "r") as fileObject:
        csvObject = csv.reader(fileObject)
        totWater = 0
        # Note : Returns as nested tuples, hence we extract with [0][0]
        for i in csvObject:
            iWeight = getData(i[0], "WeightGram", "water")
            if iWeight is not None:
                # Multiply by quantitiy
                iWeight *= int(i[1])
                totWater += iWeight
        return totWater


# Function to determine the weight
def getTotWeight(fi):
    with open(fi, "r") as fileObject:
        csvObject = csv.reader(fileObject)
        totWeight = 0
        # Note : Returns as nested tuples, hence we extract with [0][0]
        for i in csvObject:
            # Check each table if the item is in there or not, then collect the weight
            iWeight = getData(i[0], "WeightGram", "water")
            if iWeight is None:
                iWeight = getData(i[0], "WeightGram", "food")
            if iWeight is None:
                iWeight = getData(i[0], "WeightGram", "utility")

            if iWeight is not None:
                # Multiply by quantitiy
                iWeight *= int(i[1])
                totWeight += iWeight
        return totWeight


# Function to check over weight
# Returns a tuple, first value is weight percentage, second value is overweight boolean, third value is how much more
# ie . (Weight Percent, Overweight (T/F), Excess amount)
def checkWeight(curWeight):
    overWeight = False
    excess = 0
    weightPercent = int(round(curWeight / maxWeight * 100, 0))

    if weightPercent > 100:
        overWeight = True
        excess = math.fabs(curWeight - maxWeight)
    return (weightPercent, overWeight, excess)


# Function to check if enough calories and water are present, very similar to pervious function
# Returns a nested tuple
# First tuple is about calories -> Calorie Percent, Under prepared (T/F), lacking amount
# Secpmd tuple is about water -> Water Percent, Under prepared (T/F), lacking amount
# We do NOT punish the user for over preparing in this regard
def checkConsumeables(curCal, curWater):
    underCal = False
    underWater = False

    lackingCal = 0
    lackingWater = 0

    calPercent = int(round(curCal / dailyCal * 100, 0))
    waterPercent = int(round(curWater / dailyWater * 100, 0))

    if calPercent > 100:
        calPercent = 100

    if waterPercent > 100:
        waterPercent = 100

    if calPercent < 100:
        underCal = True
        lackingCal = dailyCal - curCal

    if waterPercent < 100:
        underWater = True
        lackingWater = dailyWater - curWater

    output = (
        (calPercent, underCal, lackingCal),
        (waterPercent, underWater, lackingWater),
    )

    return output


# Function to add water and calories into score system
def calWaterAdd(calPercent, waterPercent):
    global categoryPercentage, categoryScores

    categoryScores["Water"] = waterPercent
    categoryScores["Food"] = calPercent

    categoryPercentage["Water"] = str(waterPercent) + "%"
    categoryPercentage["Food"] = str(calPercent) + "%"

    # # If percentage is over 100, then just set it to 100. Same with negative scores
    # if unWeight > 100:
    #     unWeight = 100
    # elif unWeight <= 0:
    #     unWeight = 0

    # categoryPercentage[i] = str(unWeight) + "%"


# Function to get required items
def require(kit):
    kitList = list(kit)  # True Copy
    curs.execute("SELECT item FROM utility WHERE required = 'True'")
    f2 = curs.fetchall()
    req_it = []  # List of required stuffs
    for i in f2:
        req_it.append(i[0])

    # Subtraction
    for j in req_it:
        if j in kitList:
            req_it.remove(j)
        else:
            continue
    return req_it


# Running the help statement automatically
def help():
    print(Fore.GREEN + "Following are all the functions in the code")
    print()

    print(Fore.BLUE + "modifyDaily()")
    print(
        "This function is run at the beginning. It checks family size and days to go, and modifies food and water accordingly"
    )
    debugText = modifyDaily("./sampleFamilyConfig.csv")
    print(Fore.GREEN + debugText)
    print(
        Fore.GREEN + "Evaluated amount for party and days -> Water : ",
        Fore.GREEN + str(dailyWater),
        Fore.GREEN + "Calories : ",
        Fore.GREEN + str(dailyCal),
    )
    print()

    print(Fore.BLUE + "getTotWater()")
    print("This function gets the total amount of water in the kit")
    totalWater = getTotWater(inputFile)
    print(Fore.GREEN + "You have this many ml of water :", Fore.GREEN + str(totalWater))
    print()

    print(Fore.BLUE + "getTotCal()")
    print("This function gets the total amount of calories in the kit")
    totalFood = getTotCal(inputFile)
    print(Fore.GREEN + "Total calories in kit :", Fore.GREEN + str(totalFood))
    print()

    print(Fore.BLUE + "extractKitUtil()")
    print("This function extracts the given kit from CSV to a python dictionary")
    extractKitUtil(inputFile)
    print()

    print(Fore.BLUE + "checkConsumeables()")
    print(
        "This function returns information on food and water, such as percentages, True and False satisfactory, and required amount to add. Check code"
    )
    consumInfo = checkConsumeables(totalFood, totalWater)
    print(Fore.GREEN + str(consumInfo))
    print()

    print(Fore.BLUE + "sumScore()")
    print("This function adds up the total scores for each utility category")
    sumScore()
    print()

    print(Fore.BLUE + "calWaterAdd()")
    print(
        "This function adds the water and calorie scores to the overall score dictionary"
    )
    calWaterAdd(consumInfo[0][0], consumInfo[1][0])
    print()

    print(Fore.BLUE + "percentagePerCategory()")
    print(
        "This function takes the scores per category and makes them into a percentage. This is our reference values"
    )
    percentagePerCategory()
    print()

    print(Fore.GREEN + "Here is the scores per category : ")
    pp.pprint(categoryPercentage)
    print()

    print()

    print(Fore.BLUE + "weightScore()")
    print(
        "This function takes percentages and multiplies them by the weightage values. Should be run after getting water and calories"
    )
    debugText = weightScore()
    print(Fore.GREEN + debugText)
    print()

    print(Fore.BLUE + "weightMaxCheck()")
    print(
        "This function punishes or rewards the user based on if they have too few or too many items"
    )
    weightMaxCheck()
    print()

    print(Fore.BLUE + "getTotWeight()")
    print("This function gets the total weight of the kit")
    totalWeight = getTotWeight(inputFile)
    print()

    print(Fore.GREEN + "The total weight of your kit is:", totalWeight, "grams")
    print()

    print(Fore.BLUE + "checkWeight()")
    print("This function checks the total weight and lets user know of overweightage")
    print(Fore.GREEN + str(checkWeight(totalWeight)))
    print()

    print(Fore.BLUE + "getTotWater(fi)")
    print(
        "This function returns required utility items that need to be added to the kit"
    )
    print(
        Fore.GREEN
        + "Following are required items you should add : \n"
        + str(require(extract))
    )
    print()


def outputPrint():
    output = []

    modifyDaily("./sampleFamilyConfig.csv")

    output.append(
        [
        "Water Required : ",
        str(dailyWater),
        "ml",
        "Calories Required : ",
        str(dailyCal),
        "cal"]
    )


    totalWater = getTotWater(inputFile)
    output.append(["Water in the kit :",str(totalWater)])

    totalFood = getTotCal(inputFile)
    output.append(["Calories in the kit :", str(totalFood)])

    extractKitUtil(inputFile)

    consumInfo = checkConsumeables(totalFood, totalWater)
    output.append([consumInfo])

    calWaterAdd(consumInfo[0][0], consumInfo[1][0])

    sumScore()

    percentagePerCategory()

    debugText = weightScore()
    output.append(debugText)
    print()

    weightMaxCheck()

    totalWeight = getTotWeight(inputFile)

    output.append(["The total weight of your kit is:", totalWeight, "grams"])

    output.append([checkWeight(totalWeight)])

    output.append(
        ["Following are required items you should add :", str(require(extract))]
    )
    # Join all the parts into a single formatted string

    # sample = ""

    # for i in output:
    #     sample += str(i)
    #     sample += "\n"

    # return str(sample)
    return output


KV = """


<SwipeToDeleteItem>:
    size_hint_y: None
    height: content.height

    MDCardSwipeLayerBox:
        padding: "8dp"

        MDIconButton:
            icon: "trash-can"
            pos_hint: {"center_y": .5}
            on_release: app.delete_item(root)

    MDCardSwipeFrontBox:

        MDListItem:
            id: content
            _no_ripple_effect: True
            MDListItemHeadlineText:
                text:root.text



MDScreenManager:


    MDScreen:
        name: "front_page"
        md_bg_color: self.theme_cls.backgroundColor
        MDIcon:
            icon: "exit-run"
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
            theme_text_color: "Secondary"

        #Text
        MDLabel:
            text: "CritKit"
            halign: "center"
            pos_hint: {"center_y": 0.6}
            theme_text_color: "Secondary"
        #Tagline
        MDLabel:
            text: "Assesses how prepared your kit is for any disaster!"
            halign: "center"
            pos_hint: {"center_y": 0.53}
            theme_text_color: "Primary"
        #Start button
        MDButton:
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            size_hint: (0.5, 0.08)
            md_bg_color: 1, 0.5, 0, 1 
            on_release:
                app.root.transition.direction = "left"
                app.root.current = "first_input_page"
            MDButtonText:
                text: "Get Started" 


    MDScreen:
        name: "first_input_page"
        md_bg_color: self.theme_cls.backgroundColor
        MDLabel:
            text: "Enter Duration(Days)"
            pos_hint: {"center_x": .75, "center_y": .69}
        MDLabel:
            text: "Enter Max People"
            pos_hint: {"center_x": .75, "center_y": .47}

        MDBoxLayout:
            orientation: "vertical"
            spacing: "80dp"
            adaptive_height: True
            size_hint_x: .5
            pos_hint: {"center_x": .5, "center_y": .6}

            MDSlider:
                id: duration_slider

                step: 1
                max: 30
                min:
                value: 1

                MDSliderHandle:

                MDSliderValueLabel:
        MDBoxLayout:
            orientation: "vertical"
            spacing: "80dp"
            adaptive_height: True
            size_hint_x: .5
            pos_hint: {"center_x": .5, "center_y": .4}

            MDSlider:
                id: people_slider

                step: 1
                max: 15
                min:1
                value: 1

                MDSliderHandle:

                MDSliderValueLabel:

        MDButton:
            style: "outlined"
            pos_hint: {"center_x": .3, "center_y": .26}
            on_release:
                root.current = "front_page"
            MDButtonText:
                text: "Back"

        MDButton:
            style: "filled"
            pos_hint: {"center_x": .42, "center_y": .26}
            on_press: 
                app.save_values()
                root.current = "second_input_page"
            MDButtonText:
                text: "Enter"

    MDScreen:
        name: "second_input_page"
        md_bg_color: self.theme_cls.backgroundColor

        MDScrollView:
            do_scroll_x: False

            MDBoxLayout:
                id: main_scroll
                orientation: "vertical"
                adaptive_height: True
                padding: dp(16)  
                spacing: dp(12)  

                MDBoxLayout:
                    orientation: "horizontal"
                    adaptive_height: True
                    spacing: dp(20)  # Adjust spacing between the text field and button

                    MDTextField:
                        id: inputfield
                        mode: "outlined"
                        size_hint_x: None  # Ensure width is used
                        width: dp(300)
                    MDTextField:
                        id: secondinputfield
                        mode: "outlined"
                        size_hint_x: None  # Ensure width is used
                        width: dp(100)

                    MDButton:
                        size_hint_x: None
                        width: dp(200)
                        on_release: app.add_item_widget()
                        MDButtonText:
                            text: "Enter"
        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: dp(16)
            spacing: dp(20)
            pos_hint: {"center_x": 0.5, "y": 0}

            MDButton:            
                size_hint_x: None
                on_release:
                    root.current = "first_input_page"
                width: dp(150)
                MDButtonText:
                    text: "Go Back"
            MDButton:
                size_hint_x: None
                width: dp(150)
                on_release:
                    root.current = "output_page"
                    app.save_to_csv()
                    app.create_radar_graph()
                MDButtonText:
                    text: "Go to next page"
    MDScreen:
        name: "output_page"
        md_bg_color: self.theme_cls.backgroundColor

        MDBoxLayout:
            orientation: "horizontal"
            spacing: "10dp"
            padding: "10dp"
        
        # Plotly Graph Section
        Image:
            id: radar_image
            size_hint: 0.5, 1

        # Text Section
        MDBoxLayout:
            orientation: "vertical"
            size_hint: 0.5, 1

            MDLabel:
                text: "Radar Graph Example"
                theme_text_color: "Secondary"
                halign: "center"

            MDLabel:
                text: "This radar graph shows an example of data visualization side by side with text using Plotly and KivyMD."
                theme_text_color: "Secondary"
                halign: "center"
                padding: "10dp"                      
"""


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()


class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_input_list2 = []

    def build(self):
        self.theme_cls.primary_palette = "Antiquewhite"
        return Builder.load_string(KV)

    def save_values(self, filename="sampleFamilyConfig.csv"):
        duration = self.root.ids.duration_slider.value
        max_people = self.root.ids.people_slider.value

        print(f"Duration: {duration} days")
        print(f"Max People: {max_people}")

        self.duration = duration
        self.max_people = max_people
        try:
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                # Add a header row
                writer.writerow(["Family Size", "Days to Survive"])
                # Write each item and quantity to the file
                writer.writerow([f"{self.max_people}", f"{self.duration}"])
            print(f"Data saved successfully to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def add_item_widget(self):
        user_input = self.root.ids.inputfield.text.strip()
        user_input_No = self.root.ids.secondinputfield.text.strip()
        if user_input and user_input_No:
            self.user_input_list2.append([user_input, user_input_No])
            self.root.ids.main_scroll.add_widget(
                SwipeToDeleteItem(text=f"{user_input} X {user_input_No}")
            )

            self.root.ids.inputfield.text = ""
            self.root.ids.secondinputfield.text = ""

    def delete_item(self, list_item):
        """Remove the specified list item."""
        item_name = list_item.text.split(" X ")[0]
        for x in self.user_input_list2:
            if item_name in x[0]:
                self.user_input_list2.remove(x)
        self.root.ids.main_scroll.remove_widget(list_item)

        print(self.user_input_list2)

    def save_to_csv(self, filename= writeFile):
        """
        Save the user_input_list2 (containing user input and numbers) to a CSV file.
        :param filename: Name of the file to save data (default: 'user_input.csv').
        """
        try:
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                # Add a header row
                writer.writerow(["Item Name", "Quantity"])
                # Write each item and quantity to the file
                print(self.user_input_list2)
                for x in self.user_input_list2:
                    writer.writerow([x[0], x[1]])
            print(f"Data saved successfully to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
        help()

    def create_radar_graph(self):
        # Define the radar graph data
        categories = ["Lighting and Illumination", "Power and Batteries", "Tools and Equipment", "Fire and Warmth", "Navigation and Signaling", "Medical Supplies", "Hygiene and Sanitation","Food","Water","Documentation and Emergency Funds","Shelter and Clothing"]
        print(len(categories))
        values = [float(value.strip('%')) for value in categoryPercentage.values()]
        print(len(values))
        # Create radar graph with Plotly
        fig = go.Figure(data=go.Scatterpolar(
            r=values + [values[0]],  # Close the loop
            theta=categories + [categories[0]],
            fill='toself',
            name='KritikitGraph'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True)
            ),
            showlegend=False
        )

        # Convert the figure to an image
        image_bytes = io.BytesIO(fig.to_image(format="png", engine="kaleido"))
        image_bytes.seek(0)

        # Load image into Kivy
        core_image = CoreImage(image_bytes, ext="png")
        self.root.ids.radar_image.texture = core_image.texture
Example().run()



extra = '''

        MDScrollView:

            MDBoxLayout:
                id: main_scroll2
                orientation: "vertical"
                adaptive_height: True
                padding: dp(16)  
                spacing: dp(12)  

        MDBoxLayout:
            orientation: "vertical"
            size_hint: (1, 1)
            padding: "10dp"
        ScrollView:
            MDBoxLayout:
                id: output_container
                orientation: "vertical"
                adaptive_height: True
                padding: "10dp"

                MDLabel:
                    id: output_label  # Reference this label for dynamic updates
                    text: "Your output will be displayed here."
                    halign: "center"
                    font_size: "16sp"
                    text_size: self.width, None  # Ensures text wraps to the width of the screen
                    size_hint_y: None
                    height: self.texture_size[1]  # Dynamically adjust height to fit the text
                    theme_text_color: "Primary"



'''