import mysql.connector
import csv

# Functionality to pretty print dictionaries
import pprint 
pp = pprint.PrettyPrinter(indent=4)


cnx = mysql.connector.connect(
        username = "root",
        password = "root",
        host = "localhost",
        database = "kitcritic"
    )
curs = cnx.cursor()

###// HARD CODED REFERENCE DICTIONARIES ###

# Max weight in grams (13 kg as per data online)
maxWeight = 13000;

# Bictionary of categories and their totals
categoryTotals = {
        "Lighting and Illumination" : 13,
        "Power and Batteries" : 15,
        "Tools and Equipment" : 61,
        "Fire and Warmth" : 14,
        "Navigation and Signaling" : 18,
        "Medical Supplies" : 36,
        "Hygiene and Sanitation" : 31,
        #"Food and Water" : 14,
        "Documentation and Emergency Funds" : 9,
        "Shelter and Clothing" : 9
}

# To calculate the weighted average
weightage = {
        # Utility items make up 50% of the score
        "Lighting and Illumination" : 5,
        "Power and Batteries" : 5,
        "Tools and Equipment" : 7,
        "Fire and Warmth" : 6,
        "Navigation and Signaling" : 5,
        "Medical Supplies" : 8,
        "Hygiene and Sanitation" : 7,
        "Documentation and Emergency Funds" : 3,
        "Shelter and Clothing" : 4,
        
        # Food and water make up the other 50
        "Food" : 20,
        "Water" : 30
}

### HARD CODED REFERENCE DICTIONARIES //###

# Dictionary to hold how much the user earnt
categoryScores = {
        "Lighting and Illumination" : 0,
        "Power and Batteries" : 0,
        "Tools and Equipment" : 0,
        "Fire and Warmth" : 0,
        "Navigation and Signaling" : 0,
        "Medical Supplies" : 0,
        "Hygiene and Sanitation" : 0,
        #"Food and Water" : 0,
        "Documentation and Emergency Funds" : 0,
        "Shelter and Clothing" : 0
}

# Dictionary of the percentage the user earnt per category
categoryPercentage={
        "Lighting and Illumination" : 0,
        "Power and Batteries" : 0,
        "Tools and Equipment" : 0,
        "Fire and Warmth" : 0,
        "Navigation and Signaling" : 0,
        "Medical Supplies" : 0,
        "Hygiene and Sanitation" : 0,
        #"Food and Water" : 0,
        "Documentation and Emergency Funds" : 0,
        "Shelter and Clothing" : 0
}

# Function to retrieve data (NAZIA)
def getData(condition,request, table):
        # c = input("Enter the item you want to fetch data for: ")
        # v = input("Enter the data you want to retrieve from the item: ")
        curs.execute(f"SELECT {request} FROM {table} WHERE Item = \"{condition}\"")
        fetched = curs.fetchall()
        #If no empty value
        if fetched :
                return fetched[0][0]
        else:
                pass

# Function to update data (NAZIA)

# This function reads the CSV containing what Utilities are in the kit, and builds a dictionary to use in code.
extract = {}
def extractKitUtil(fi):
        with open(fi, "r") as fileObject:
                csvObject = csv.reader(fileObject)
                global extract

                # Note : Returns as nested tuples, hence we extract with [0][0]
                for i in csvObject:
                        #if none is returned, ignore
                        if not getData(i[0], "Category", "utility") :
                                continue
                        icat = getData(i[0], "Category", "utility")
                        iscore = getData(i[0], "SurvivalScore", "utility")
                        ireq =  getData(i[0], "Required", "utility")
                        iweight =  getData(i[0], "WeightGram", "utility")
                        imax =  getData(i[0], "MaxPerPerson", "utility")
                        iquant = i[1]

                        out = {
                                "Category" : icat,
                                "SurvivalScore" : iscore,
                                "Required" : ireq,
                                "WeightGram" : iweight,
                                "MaxPerPerson" : imax,
                                "Quantity" : iquant
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
        for i in categoryPercentage:
                # Percentage = x / total * 100, rounded to 2 decimal places
                unWeight = round(categoryScores[i] / categoryTotals[i] * 100,2)

                # If percentage is over 100, then just set it to 100. Same with negative scores
                if unWeight > 100 :
                        unWeight = 100
                elif unWeight <= 0:
                        unWeight = 0

                categoryPercentage[i] = str(unWeight)+"%"


# This function gives the overall weighted score
def weightScore():
        finalScore = 0
        for i in categoryScores:
                # WeightedPercent = Percentage * (Weightage/100)
                # [-1] to not consider the percentage symbol
                weighted = float(categoryPercentage[i][:-1]) * (weightage[i]/100)
                # Round down to 2 decimals
                weightedRound = round(weighted,2)
                # Add it to final score
                finalScore += weightedRound

        print(f"Your final score is {finalScore}%")

# This function normalizes for the quantity ie. Checks for too many items
def normalWeight():
        pp.pprint(extract)
        for i in extract :
                amountInKit = int(extract[i]['Quantity'])
                maxAmount = int(extract[i]['MaxPerPerson'])
                itemCat = extract[i]['Category']
                
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
                        if ical != None :
                                #Multiply by quantitiy
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
                        if iWeight != None :
                                #Multiply by quantitiy
                                iWeight *= int(i[1])
                                totWater += iWeight
                return totWater

# This function find the amount needed for the family size and days
        # Daily water and calorie based

# Function to determine the weight
extractKitUtil("./sampleInput.csv")
sumScore()
percentagePerCategory()
print("Here is the scores per category : ")
pp.pprint(categoryPercentage)
print()
weightScore()
print()
normalWeight()
print("Total calories in kit :" ,getTotCal("./sampleInput.csv"))
print("You have this many ml of water :",getTotWater("./sampleInput.csv"))