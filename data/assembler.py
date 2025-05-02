#Importing sqlite3 for database addition, csv to read sample data,
# and json to write the csv data to a human redable format.
import sqlite3
from csv import DictReader
import json

#Form csv and database paths for links.
database_url = "./ksp.db"
csv_engines = "./data/csv/Engines.csv"
csv_images = "./data/csv/Images.csv"
csv_missions = "./data/csv/Missions.csv"
csv_stages = "./data/csv/Stages.csv"


#A Function to wipe the database as the script relies on an empty database.
def clear_db(database):
    """Clears the database of all data."""
    #Connect to the database and collect table names
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Delete all data from each table
    for table_name in tables:
        table = table_name[0]
        cursor.execute(f"DELETE FROM {table}")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
    conn.commit()
    conn.close()


# A Function to convert the quotations around floats and integers in
# the csv's into floats or integers.
def convert_numerics_to_int_float(input_list):
    """Checks if elements in a list are integers or floats contained 
    in a string and converts them into an integer or float.
    """
    for i in range(len(input_list)):  
        if input_list[i].isdigit() is True:
            input_list[i] = int(input_list[i])
        # Checks if a string is all numbers with a single . removed.
        # This checks if the string is a float.
        elif (input_list[i].replace(".","",1).isdigit()) is True:
            input_list[i] = float(input_list[i])
    input_list = tuple(input_list)
    return input_list
    

def engine_table_composer(database_url, csv_engines):
    """A function to insert data on various engines into
    the engine table of database.
    """
    with sqlite3.connect(database_url) as conn:
        with open(csv_engines, newline="") as csv_engine:
            reader = DictReader(csv_engine)
            # Read a row of data from the csv.
            for row in reader:
                # Convert the columns into a tuple for query injection 
                # and values into a list for data sanitisation.
                columns = tuple(dict(row).keys())
                values = list(dict(row).values())
                columns_to_insert =  str(columns).replace("'", "")
                values_to_insert = convert_numerics_to_int_float(values)
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO Engine {columns_to_insert}VALUES (?,?,?,?,?,?,?,?,?,?,?);", values_to_insert)

def image_table_composer():
    """A function to insert data on various images into
    the image table of database.
    """
    with sqlite3.connect(database_url) as conn:
        with open(csv_images, newline="") as csv_image:
            reader = DictReader(csv_image)
            for row in reader:
                columns = list(dict(row).keys())
                values = list(dict(row).values())
                values = values[0:(len(values)-1)]
                columns.remove(columns[-1])
                columns = tuple(columns)
                columns_to_insert =  str(columns).replace("'", "")
                values_to_insert = convert_numerics_to_int_float(values)
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO Image {columns_to_insert} VALUES (?,?,?);", values_to_insert)

#clear_db(database_url)
#image_table_composer()
#engine_table_composer()
