import json
from random import randint

# --------------- INITIALIZATION ----------------
DELETE = True

# Open the JSON file
with open('APIbusterModelled2.json', 'r') as f:
# with open('peopleOntologyModelled2.json', 'r') as f:
    data = json.load(f)

CLASSES_ARRAY = []
CLASS_PROPERTIES = []
OBJECT_PROPERTIES = []

DROP_ARRAY = []
CREATE_ARRAY = []
ALTER_ARRAY = []
# --------------- INITIALIZATION ----------------


# --------------- SUPPLEMENTARY FUNCS ---------------
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]
# --------------- SUPPLEMENTARY FUNCS ---------------


# --------------- FUNCTIONS ---------------
def update_classes():
    for obj in data:
        # Check if the object has a "type" field set to "Class" and updates CLASSES_ARRAY
        if "type" in obj and obj["type"][0] == "Class":
                new_class = obj
                # Updates the array filled with all Classes of the ontology
                CLASSES_ARRAY.append(new_class)

    order_classes(CLASSES_ARRAY)

def update_data_properties():
    for obj in data:
        # Check if the object has a "type" field set to "DatatypeProperty" and updates CLASSES_PROPERTIES
        if "type" in obj and obj["type"][0] == "DatatypeProperty":
                new_property = obj
                # Updates the array filled with all Data Properties of the ontology
                CLASS_PROPERTIES.append(new_property)

    # update_data_properties(CLASS_PROPERTIES)

def update_object_properties():
    for obj in data:
        # Check if the object has a "type" field set to "ObjectProperty" and updates OBJECT_PROPERTIES
        if "type" in obj and obj["type"][0] == "ObjectProperty":
                new_property = obj
                # Updates the array filled with all Object Properties of the ontology
                OBJECT_PROPERTIES.append(new_property)

def order_classes(array):
    for obj in array:
        if "subClassOf" in obj:
            # Get the value of the "subClassOf" field
            subclass_id = obj["subClassOf"][0]["id"]

            # Search for an object with an "id" field that matches the value of "subClassOf"
            find_class = [class_obj for class_obj in array if class_obj['id'] == subclass_id]
            
            # Restructure array
            aux_obj = obj
            if find_class == []:
                # Search for index
                index = array.index(aux_obj)
                # Delete existing obj
                array.pop(index)
                # Insert in proper index
                array.insert(0, aux_obj)
            elif not find_class == []:
                # Search for parent index
                parent_index = array.index(find_class[0])
                # Search for index
                index = array.index(obj)
                # Delete existing obj
                array.pop(index)
                # Insert in proper index
                parent_index = parent_index + 1
                array.insert(parent_index, aux_obj)
        # if "equivalentClass" in obj:
        #     print(obj)


def check_restrictions():
    RESTRICT = []
    for obj in data:
        if "type" in obj and obj["type"][0] == "Restriction":
            # Search for an object with an "id" field that matches the value of "subClassOf"
            find_applied_class = []
            for new_obj in CLASSES_ARRAY:
                if "subClassOf" in new_obj:
                    # print(f"OBJECT: \n{new_obj}\n")
                    # name = subClass["id"]
                    # name = new_obj["subClassOf"][0]["id"]
                    # print(f"subClass name: {name}")
                    for subClass in new_obj["subClassOf"]:
                        # print(f"SUBCLASS: \n{subClass}\n")
                        if subClass["id"] == obj["id"]:
                        # if new_obj["subClassOf"][0]["id"] == obj["id"]:
                            find_applied_class.append(new_obj)

                        # elif len(new_obj["subClassOf"]) > 1:
                        #     max_count = len(new_obj["subClassOf"])
                        #     for count in range(1, max_count):
                        #         if new_obj["subClassOf"][count]["id"] == obj["id"]:
                        #             find_applied_class = new_obj

                        if not find_applied_class == []:
                            # objName = obj["id"]
                            # print(f"subclassName: {name} ---- VS ---- objName: {objName}")
                            # print(f"Match: {find_applied_class}")
                            if "someValuesFrom" in obj:
                                someValues = obj["someValuesFrom"]
                                # print(f"RESTRICTION_VALUES: {someValues}")
                                # print(f"class where applied: {find_applied_class}")
                                domain = find_applied_class[0]["id"]
                                # print(f"DOMAIN: {domain}")
                                # print(f"RANGE: {someValues}")
                                restriction = {
                                    "domain": find_applied_class[0]["id"],
                                    # "range": obj["someValuesFrom"][0]["id"]
                                    "range": obj["someValuesFrom"]
                                }
                                # print(f"FINAL_RESTRICTION_VALUE: {restriction}\n")
                                # Check if restriction already exists
                                if not restriction in RESTRICT:
                                    RESTRICT.append(restriction)
            
    return RESTRICT

def print_ddl():
    # Print file
    for entry in DROP_ARRAY:
        print(entry, end='')
    for entry in CREATE_ARRAY:
        print(entry, end='')
    for entry in ALTER_ARRAY:
        print(entry, end='')

def check_for_Discriminator(table):
    # Check in Create array if table with name "table" has Discriminator property
    for obj in CREATE_ARRAY:
        if f"TABLE {table}" in obj and "Discriminator" in obj:
            return True
        elif f"TABLE {table}" in obj and not "Discriminator" in obj:
            return False
           
def create_ddl():
    FK_AUX = []
    RESTRICT_ARRAY = check_restrictions()
    for obj in CLASSES_ARRAY:
        table = obj["id"]

        # Updates DROP array to build DDL file
        DROP_ARRAY.append(f"DROP TABLE IF EXISTS {table} CASCADE;\n")

        AUX = []
        # Updates CREATE array to build DDL file  
        for rest in RESTRICT_ARRAY:    
            # Creates FK properties
            if rest["domain"] == table:
                prop_name = rest["domain"] + "ID"
                prop_type = "int4"
                AUX.append(f", {prop_name} {prop_type} NOT NULL")
                fk = {
                    "name": prop_name,
                    "table": rest["range"][0]["id"],
                    "reference": table
                }
                FK_AUX.append(fk)

        # Checks properties for a class
        for prop in CLASS_PROPERTIES:
            if prop["domain"][0]["id"] == table:
                prop_name = prop["id"]

                # Property type translations
                prop_type = ""
                if prop["range"][0]["id"] == "string":
                    prop_type = "varchar(255)"
                elif prop["range"][0]["id"] == "integer":
                    prop_type = "int4"
                elif prop["range"][0]["id"] == "dateTime":
                    prop_type = "varchar(255)"
                elif prop["range"][0]["id"] == "boolean":
                    prop_type = "boolean"

                AUX.append(f", {prop_name} {prop_type}")
        
        # Check if class has properties
        if not AUX == []:
            properties = ""
            for obj in AUX:
                properties = properties + obj

            CREATE_ARRAY.append(f"CREATE TABLE {table} (ID SERIAL NOT NULL{properties}, PRIMARY KEY (ID));\n")

        # If class has no properties, delete class from DROP array and had discriminator to parent class
        elif AUX == []:
            for obj2 in CLASSES_ARRAY:
                # Checks for parent class in CREATE array and adds Discriminator property to query
                if "subClassOf" in obj:
                    for subClass in obj["subClassOf"]:
                        if subClass["id"] == obj2["id"]:
                            for create in CREATE_ARRAY:
                                obj2ID = obj2["id"]
                                if f"TABLE {obj2ID}" in create:
                                    exists = check_for_Discriminator(obj2["id"])
                                    if exists == False:
                                        new_create = create.replace(", PRIMARY KEY (ID));", ", Discriminator varchar(255), PRIMARY KEY (ID));")
                                        index = CREATE_ARRAY.index(create)
                                        CREATE_ARRAY[index] = new_create

                        # Deletes class from DROP array
                        if DELETE == True:
                            for drop in DROP_ARRAY:
                                if obj["id"] in drop:
                                    index = DROP_ARRAY.index(drop)
                                    DROP_ARRAY.pop(index)

    # print(f"RESTRICTIONS: {FK_AUX}")
    # print(len(FK_AUX))
    for obj in CLASSES_ARRAY:
        table = obj["id"]

        # Updates ALTER array to build DDL file
        num = random_with_N_digits(5)
        TABLE = table.upper()
        for fk in FK_AUX:
            if fk["table"] == table:
                fk_name = fk["name"]
                ref = fk["reference"]
                ALTER_ARRAY.append(f"ALTER TABLE {table} ADD CONSTRAINT FK{TABLE}{num} FOREIGN KEY ({fk_name}) REFERENCES {ref} (ID) ON DELETE CASCADE;\n")

    print_ddl()
# --------------- FUNCTIONS ---------------


# --------------- MAIN ---------------
update_classes()
update_data_properties()
update_object_properties()

create_ddl()
# --------------- MAIN ---------------


