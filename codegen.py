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
