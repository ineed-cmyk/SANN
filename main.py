import mysql.connector
import csv
import pprint 
pp = pprint.PrettyPrinter(indent=4)


cnx = mysql.connector.connect(
        username = "root",
        password = "root",
        host = "localhost",
        database = "kitcritic"
    )
curs = cnx.cursor()

# Building a dictionary of types
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
                return


# Function to update data (NAZIA)

# This function reads the CSV containing what is in the kit, and builds a dictionary to use in code.
extract = {}
def extractKitUtil(fi):
        with open(fi, "r") as fileObject:
                csvObject = csv.reader(fileObject)
                global extract

                # Note : Returns as nested tuples, hence we extract with [0][0]
                for i in csvObject:
                        icat = getData(i[0], "Category", "utility")
                        iscore = getData(i[0], "SurvivalScore", "utility")
                        ireq =  getData(i[0], "Required", "utility")
                        iweight =  getData(i[0], "WeightGram", "utility")
                        imax =  getData(i[0], "MaxPerPerson", "utility")
                        iquant = i[1]

                        out = {
                                "category" : icat,
                                "SurvivalScore" : iscore,
                                "Required" : ireq,
                                "WeightGram" : iweight,
                                "MaxPerPerson" : imax,
                                "Quantity" : iquant
                        }

                        extract[i[0]] = out

                return extract

# Function to aggregrate the score
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
def sumScore():
        for i in extract:
                iScore = extract[i]["SurvivalScore"]
                cat = extract[i]["category"]
                categoryScores[cat] += iScore

# This function gives the overall weighted score for each category

def weightScore():
        finalScore = 0
        for i in categoryScores:
                # Percentage = x / total * 100
                unWeight = categoryScores[i] / categoryTotals[i] * 100
                # WeightedPercent = Percentage * (Weightage/100)
                weighted = unWeight * (weightage[i]/100)
                # Round down to 2 decimals
                weightedRound = round(weighted,2)
                
                # Add it to final score
                finalScore += weightedRound
        print(f"Your final score is {finalScore}%")
                


extractKitUtil("./sampleInput.csv")
sumScore()
weightScore()