import os
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 3:
    print("give input file and output folder") #folder not given
    sys.exit()

input_file = sys.argv[1]
output_folder = sys.argv[2] #storing the input and output folders for import and export

if not os.path.exists(output_folder):
    os.makedirs(output_folder) #making output folder incase

tree = ET.parse(input_file)
root = tree.getroot() #parsing xml

things = {}
relationships = []
specializations = [] #hold translation semantic results

for cell in root.iter("mxCell"): #available in the xml element tree library, so go thru every cell

    vertex = cell.get("vertex")
    edge = cell.get("edge")

    if vertex == "1": #finds the entities (rectangles)
        id_value = cell.get("id")
        name_value = cell.get("value")

        if name_value is not None and name_value != "":
            things[id_value] = name_value

    if edge == "1": #find the relations (arrows)
        source = cell.get("source")
        target = cell.get("target")
        label = cell.get("value")
        style = cell.get("style")

        if label is None:
            label = ""

        if style is None:
            style = ""

        if "endArrow=block" in style: #checks if its inheritance
            specializations.append([source, target])
        else:
            relationships.append([source, target, label])

def get_parts(label): #split the labels on arrows
    if "(" in label and ")" in label:
        first = label.split("(")[0]
        second = label.split("(")[1]
        number = second.replace(")", "")
        return first, number
    else:
        return None, None

for thing_id in things: #make java files and write to them

    thing_name = things[thing_id]
    super_class = None

    for spec in specializations: #superclass 
        if spec[0] == thing_id:
            parent_id = spec[1]
            super_class = things.get(parent_id)

    file_path = os.path.join(output_folder, thing_name + ".java")
    file = open(file_path, "w")

    needs_list = False
    field_lines = []

    for rel in relationships: #check the relationship type
        source = rel[0]
        target = rel[1]
        label = rel[2] #spliting up cardinality, owner class, and suppplier class

        if source == thing_id:

            rel_name, card = get_parts(label) #break into cardinality and relation

            if rel_name is not None: #if theres a relation
                target_name = things.get(target)

                variable_name = rel_name + "_" + target_name.lower()

                if card == "1":
                    line = "    private " + target_name + " " + variable_name + ";" #add line that created private instance variable to file
                    field_lines.append(line)
                else:
                    line = "    private java.util.List<" + target_name + "> " + variable_name + ";" #add line that creates private java list to file
                    field_lines.append(line)
                    needs_list = True
