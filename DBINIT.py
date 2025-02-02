import mysql.connector

inpPass = input("Please Enter MYSQL password : ")

try :
    print("Connecting to SQL...")
    cnx = mysql.connector.connect(
        username = "root",
        password = inpPass,
        host = "localhost",
    )
    curs = cnx.cursor()
   

    print("Creating database...")
    curs.execute("CREATE DATABASE kitcritic")
    cnx.database = "kitcritic"
    curs = cnx.cursor()

    print("Creating utility table")
    curs.execute("""CREATE TABLE utility (
	ID INT,
	Item VARCHAR(50),
	Category VARCHAR(50),
	SurvivalScore INT,
	Required VARCHAR(5),
	WeightGram INT,
	MaxPerPerson INT);""")

    print("Populating utility table")
    curs.execute("""INSERT INTO utility VALUES
	('1', 'Flashlights', 'Lighting and Illumination', '9', 'True', '200', '1'),
	('2', 'Batteries(Single AA)', 'Power and Batteries', '7', 'False', '30', '2'),
	('3', 'Radio', 'Tools and Equipment', '8', 'False', '500', '1'),
	('4', 'Knives', 'Tools and Equipment', '7', 'True', '350', '1'),
	('5', 'Waterproof Matches', 'Fire and Warmth', '6', 'False', '30', '2'),
	('6', 'Map', 'Navigation and Signaling', '5', 'False', '100', '1'),
	('7', 'Lanterns', 'Lighting and Illumination', '4', 'False', '800', '2'),
	('8', 'First Aid Kit', 'Medical Supplies', '10', 'True', '1000', '1'),
	('9', 'Bandages(Roll)', 'Medical Supplies', '8', 'True', '75', '3'),
	('10', 'Thermometer', 'Medical Supplies', '2', 'False', '100', '1'),
	('11', 'Tourniquet', 'Medical Supplies', '6', 'False', '150', '1'),
	('12', 'Medicine', 'Medical Supplies', '10', 'True', '35', '3'),
	('13', 'Compass', 'Navigation and Signaling', '3', 'False', '100', '1'),
	('14', 'Whistle', 'Navigation and Signaling', '4', 'False', '30', '1'),
	('15', 'Tissue Paper', 'Hygiene and Sanitation', '4', 'False', '100', '3'),
	('16', 'Toilet Paper', 'Hygiene and Sanitation', '5', 'True', '250', '3'),
	('17', 'Sleeping Bag', 'Fire and Warmth', '8', 'True', '2000', '1'),
	('18', 'Portable Stove', 'Food and Water', '5', 'False', '2000', '1'),
	('19', 'Rope(10m)', 'Tools and Equipment', '6', 'False', '2000', '2'),
	('20', 'Shovel', 'Tools and Equipment', '5', 'False', '1500', '1'),
	('21', 'Duct Tape', 'Tools and Equipment', '3', 'False', '400', '1'),
	('22', 'Pail for Toilet', 'Hygiene and Sanitation', '8', 'True', '1000', '1'),
	('23', 'Axe', 'Tools and Equipment', '7', 'False', '2000', '1'),
	('24', 'Garbage Bag', 'Hygiene and Sanitation', '4', 'False', '75', '3'),
	('25', 'Flare Gun', 'Navigation and Signaling', '6', 'False', '600', '1'),
	('26', 'Copy of Important Records', 'Documentation and Emergency Funds', '9', 'True', '100', '1'),
	('27', 'Purification Tablet', 'Food and Water', '9', 'False', '35', '2'),
	('28', 'Manual Can Opener', 'Tools and Equipment', '7', 'False', '200', '1'),
	('29', 'Set of Clothes', 'Shelter and Clothing', '9', 'True', '1000', '4'),
	('30', 'Soap', 'Hygiene and Sanitation', '10', 'True', '150', '2'),
	('31', 'Power Bank', 'Power and Batteries', '8', 'False', '350', '2'),
	('32', 'Portable Water Purifier', 'Tools and Equipment', '9', 'False', '50', '1'),
	('33', 'Water Purification Tablet', 'Tools and Equipment', '9', 'False', '10', '1');
                 """)
    cnx.commit()

    print("Creating food database")
    curs.execute("""CREATE TABLE food (
	ID INT,
	Item VARCHAR(50),
	WeightGram INT,
	Perishable VARCHAR(5),
	NutritionScore INT,
	Calorie INT);
    """)
    print("Populating food table")
    curs.execute("""INSERT INTO food VALUES
	('1', 'Gohan Pack', '160', 'True', '9', '230'),
	('2', 'Instant Noodles', '75', 'False', '8', '400'),
	('3', 'Onigiri', '110', 'True', '5', '220'),
	('4', 'Canned Fish', '150', 'False', '6', '120'),
	('5', 'Canned Meat', '200', 'False', '8', '200'),
	('6', 'Canned Vegetables', '400', 'False', '3', '45'),
	('7', 'Crackers/Biscuits', '150', 'False', '7', '180'),
	('8', 'Nuts and Seeds', '100', 'False', '7', '180'),
	('9', 'Dried Fruits', '150', 'False', '7', '130'),
	('10', 'Seaweed', '50', 'False', '4', '20'),
	('11', 'Freeze-Dried Meal', '100', 'False', '7', '500'),
	('12', 'Calorie Bar', '50', 'False', '9', '230'),
	('13', 'Energy Gel', '30', 'False', '5', '100'),
	('14', 'Chocolate Bar', '100', 'False', '8', '230'),
	('15', 'Miso Powder', '50', 'False', '4', '40');
    """)
    cnx.commit()

    print("Creating water table")
    curs.execute("""CREATE TABLE water (
	ID INT,
	Item VARCHAR(50),
	WeightGram INT,
	HydrationScore INT);""")
    print("Populating water table")
    curs.execute("""INSERT INTO water VALUES
	('1', 'Water Bottle (500ml)', '500', '10'),
	('2', 'Sports Drink (500ml)', '500', '9'),
	('3', 'Water Bottle (1000ml)', '1000', '10');""")
    cnx.commit()

    print("SUCCESS! Database imported")



except Exception as e:
    print("FAIL!")
    print("The following error was encountered : \n")
    print(e)