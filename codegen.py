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