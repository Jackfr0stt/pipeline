# Python code to properly setup JSON info
def model_JSON(file):
    jsonFile = open(file, 'r')
    Lines = jsonFile.readlines()

    count = 0
    for line in Lines:
        count += 1

        # Fixes strings where where full names are present
        if (line.count("#") > 0):
            http = line.rsplit("http")[0]
            afterCardinal = line.rsplit("#")[1]
            line=http+afterCardinal

        line = line.replace("@", "")

        # Turns words separated by _ to camelCase

        # Prints lines to file
        print(line, end = '')

# Usage
model_JSON('APIbuster.json')
# model_JSON('peopleOntology.json')