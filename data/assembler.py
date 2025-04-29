import sqlite3
from csv import DictReader


database_url = "./ksp.db"
csv_engines = "./data/csv/Engines.csv"

def clear_quotation_floats(input_string):
    strings = input_string.split(",")
    for i in range(len(strings)):
        strings[i] = strings[i].lstrip()
        if is_floatable(strings[i]) is True:
            strings[i] = strings[i].replace("'", "")
            strings[i] = float(strings[i])
    return strings
    


def is_floatable(input_string):
    input_string.replace(".", "", 1)
    if input_string.isdigit() == True:
        return True
    else:
        return False

with sqlite3.connect(database_url) as conn:
    with open(csv_engines, newline="") as csv_engine:
        reader = DictReader(csv_engine)
        for row in reader:
            print(row)
            collums = tuple(dict(row).keys())
            values = tuple(dict(row).values())
        collums_to_insert =  str(collums).replace("'", "")
        values_to_insert = clear_quotation_floats((str(values).replace('(', "").replace(")", "")))
        print(values_to_insert)
        quit()
        query_composition = f"INSERT INTO Egnines {collums_to_insert}"
        cursor = conn.cursor()
        print(f"INSERT INTO Engines {collums} VALUES{values};")
        cursor.execute(f"INSERT INTO Engines ({collums}) VALUES({values});")
        results = cursor.fetchall()
        print(results)

