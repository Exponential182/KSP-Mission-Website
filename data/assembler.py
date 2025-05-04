# Importing sqlite3 for database addition, csv to read sample data,
# and json to write the csv data to a human redable format.
import sqlite3
from csv import DictReader
import json

# Form csv and database paths for links.
database_url = "./ksp.db"
engines_url = "./data/csv/Engines.csv"
images_url = "./data/csv/Images.csv"
missions_url = "./data/csv/Missions.csv"
stages_url = "./data/csv/Stages.csv"
engines_json = "./data/json/Engines.json"
images_json = "./data/json/Images.json"
missions_json = "./data/json/Missions.json"
stages_json = "./data/json/Stages.json"


# A Function to wipe the database as the script relies on an empty database.
def clear_db(database_link):
    """Clears the database of all data."""
    # Connect to the database and collect table names
    conn = sqlite3.connect(database_link)
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
    

def engine_table_composer(database_link, csv_link):
    """A function to insert data on various engines into
    the engine table of database.
    """
    with sqlite3.connect(database_link) as conn:
        with open(csv_link, newline="", mode="r", encoding='utf-8-sig') as csv_engine:
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


def image_table_composer(database_link, csv_link):
    """A function to insert data on various images into
    the image table of database.
    """
    with sqlite3.connect(database_link) as conn:
        with open(csv_link, newline="", mode="r", encoding='utf-8-sig') as csv_image:
            reader = DictReader(csv_image)
            for row in reader:
                # Gather and Prepare the column info.
                columns = list(dict(row).keys())
                columns.remove(columns[-1])
                columns = tuple(columns)
                columns_to_insert = str(columns).replace("'", "")

                # Prepare the values and linking ids.
                values = list(dict(row).values())
                linking_info = values[-1]
                values.remove(values[-1])
                values_to_insert = convert_numerics_to_int_float(values)
                linking_info = linking_info.replace("[","").replace("]","")
                linking_ids = list(map(int, linking_info.split(",")))

                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO Image {columns_to_insert} VALUES (?,?,?);", values_to_insert)
                for i in linking_ids:
                    cursor.execute(f'INSERT INTO MissionImage (mission_id, image_id) VALUES(?,?)', (i, values[0]))


def stage_table_composer(database_link, csv_link):
    """A Function to add the stage into into the stage table as well as adding
    the coresponding engine ids to the linking table.
    """
    with sqlite3.connect(database_link) as conn:
        with open(csv_link, newline="", mode="r", encoding='utf-8-sig') as csv_stage:
            reader = DictReader(csv_stage)
            cursor = conn.cursor()
            for row in reader:
                # Prepare the columns
                columns = list(dict(row).keys())
                columns.remove(columns[-1])
                columns_to_insert = str(tuple(columns)).replace("'", "")
                
                # Prepare the values and linking ids.
                values = list(dict(row).values())
                linking_info = values[-1]
                values.remove(values[-1])
                values_to_insert = convert_numerics_to_int_float(values)
                linking_info = linking_info.replace("[","").replace("]","")
                linking_ids = list(map(int, linking_info.split(",")))

                cursor.execute(f"INSERT INTO Stage {columns_to_insert} VALUES (?,?,?,?,?,?,?,?,?)", values_to_insert)
                for i in linking_ids:
                    cursor.execute(f"INSERT INTO StageEngine (stage_id, engine_id) VALUES(?,?)", (values[0], i))


def mission_table_composer(database_link, csv_link):
    """A Function to add the mission into into the mission table as well as 
    adding the coresponding stage ids to the linking table.
    """
    with sqlite3.connect(database_link) as conn:
        with open(csv_link, newline="", encoding='utf-8-sig', mode="r") as csv_mission:
            reader = DictReader(csv_mission)
            cursor = conn.cursor()
            for row in reader:
                # Prepare the columns
                columns = list(dict(row).keys())
                columns.remove(columns[-1])
                columns_to_insert = str(tuple(columns)).replace("'", "")
                
                #Prepare the values and linking ids.
                values = list(dict(row).values())
                linking_info = values[-1]
                values.remove(values[-1])
                values_to_insert = convert_numerics_to_int_float(values)
                linking_info = linking_info.replace("[","").replace("]","")
                linking_ids = list(map(int, linking_info.split(",")))

                cursor.execute(f"INSERT INTO Mission {columns_to_insert} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", values_to_insert)
                for i in linking_ids:
                    cursor.execute(f"INSERT INTO MissionStage (mission_id, stage_id) VALUES(?,?)", (values[0], i))


def json_dumper(csv_file, json_file):
    # Read the csv file and convert it to a list of dictionaries.
    with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as csv_reader:
        reader = DictReader(csv_reader)
        data = list(reader)
    
    # Write the data to json
    with open(json_file, encoding="utf-8-sig", mode="w") as json_file:
        json.dump(data, json_file, indent=4)


# Establishes the database in such a way that the linking tables can be 
# composed without referecing empty keys
clear_db(database_url)
engine_table_composer(database_url, engines_url)
stage_table_composer(database_url, stages_url)
mission_table_composer(database_url, missions_url)
image_table_composer(database_url, images_url)

# Parse the data in JSON files to make the changes more readable in Git.
json_dumper(engines_url, engines_json)
json_dumper(images_url, images_json)
json_dumper(stages_url, stages_json)
json_dumper(missions_url, missions_json)