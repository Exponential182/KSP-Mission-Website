from csv import DictReader
import json

with open('csv testing/output.txt', 'w+') as output:
    with open('csv testing/Celeste Speedrun Tracker - Sheet9.csv',newline="") as csvfile:
        reader = DictReader(csvfile)
        print(type(reader))
        for row in reader:
            print(row)
            ree = str(row)
            print(ree)
            output.write(json.dumps(row, sort_keys=True, indent=4))
            output.write("\n")