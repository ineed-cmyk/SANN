import mysql.connector

cnx = mysql.connector.connect(
        username = "root",
        password = "root",
        host = "localhost",
        database = "kitcritic"
    )
curs = cnx.cursor()

# Buidling a dictionary of types
categories = {
        "Lighting and Illumination" = 13,
        "Power and Batteries" = 15,
        "Tools and Equipment" = 61,
        "Fire and Warmth" = 14,
        "Navigation and Signaling" = 18,
        "Medical Supplies" = 36,
        "Hygiene and Sanitation" = 31,
        "Food and Water" = 14,
        "Documentation and Emergency Funds" = 9,
        "Shelter and Clothing" = 9
}

weightage = {
        # Utility items make up 50% of the score
        "Lighting and Illumination" = 5,
        "Power and Batteries" = 5,
        "Tools and Equipment" = 7,
        "Fire and Warmth" = 6,
        "Navigation and Signaling" = 5,
        "Medical Supplies" = 8,
        "Hygiene and Sanitation" = 7,
        "Documentation and Emergency Funds" = 3,
        "Shelter and Clothing" = 4,
        
        # Food and water make up the other 50
        "Food" = 20,
        "Water" = 30
}



# Function to find the total score as per catagory

# Function to retrieve data (NAZIA)

# Function to update data (NAZIA)

# Function to give overall score to kit

