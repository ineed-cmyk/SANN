import mysql.connector
import csv

cnx = mysql.connector.connect(
        username = "root",
        password = "root",
        host = "localhost",
        database = "kitcritic"
    )
curs = cnx.cursor()

# Building a dictionary of types
categorieTotals = {
        "Lighting and Illumination" : 13,
        "Power and Batteries" : 15,
        "Tools and Equipment" : 61,
        "Fire and Warmth" : 14,
        "Navigation and Signaling" : 18,
        "Medical Supplies" : 36,
        "Hygiene and Sanitation" : 31,
        "Food and Water" : 14,
        "Documentation and Emergency Funds" : 9,
        "Shelter and Clothing" : 9
}

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
    fetched = cur.fetchall()
    return fetched


# Function to update data (NAZIA)

# Function to give overall score to kit
def rateAKitUtil(fi):
        with open(fi, "r") as fileObject:
                csvObject = csv.reader(fileObject)
                extract = {} 
                for i in csvObject:
                        icat = getData(i[0], "Category", "utility")
                        iscore = getData(i[0], "SurvivalScore", "utility")
                        ireq =  getData(i[0], "Required", "utility")
                        iweight =  getData(i[0], "WeightGram", "utility")
                        imax =  getData(i[0], "MaxPerPerson", "utility")
                        iquant = i[2]

                        out = {
                                "category" : icat,
                                "SurvivalScore" : iscore,
                                "Required" : ireq,
                                "WeightGram" : iweight,
                                "MaxPerPerson" : imax,
                                "Quantity" : iquant
                        }

                        extract[i] = out

                        return extract

rateAKitUtil("./sampleInput.csv")