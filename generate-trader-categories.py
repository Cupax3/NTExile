import sys
import csv
import csvconstants as cc

from terminal import *
pHeader ("Build step started: generate-trader-categories")

if (len(sys.argv) < 2):
	pError ("Not enough arguments.")
	exit()

pBuild ("Beginning parsing of trader categories from ", f"{bcolors.OKBLUE}", str(sys.argv[1]))

file = None

try:
	file = open(sys.argv[1], "r+", newline='')
	pBuild ("Class file found.")
except IOError:
	pError ("Class file does not exist.")
	exit()

csvReader = csv.reader(file)
pBuild ("Class file read successfully.")

csvContent = [None]

for row in csvReader:
	csvContent.append(row)
csvContent.pop(0)
csvContent.pop(0) # Pop twice to remove descriptor line

file.close()

pBuild ("Class file cached successfully.")

content = [None]

for row in csvContent:
	if (row[cc.COLUMN_TRADER_BOOLEAN] == "1"):
		content.append(row)

content.pop(0)

pBuild ("Tradeable goods successfully loaded.")

categories = [None]

pBuild ("Building category list.")

for row in content:
	if not row[cc.COLUMN_TRADER_CATEGORY] in categories:
		categories.append(row[cc.COLUMN_TRADER_CATEGORY])

pBuild ("Categories found: ", categories)

categories.pop(0)

pBuild ("Preparing output file.")

for category in categories:
	try:
		file = open("output/traderstuff/" + category.lower() + "_category.hpp", "w")
		pBuild ("Output file successfully opened.")
	except IOError:
		pError ("Cannot open output file.")
		exit()

	pBuild ("Prepending output file information.")

	file.write("	class NTCustom" + category + "\n")
	file.write("	{" + '\n')
	file.write("		name = \"NTC " + category + "\";\n")
	file.write("		icon = \"a3\\ui_f\\data\\gui\\Rsc\\RscDisplayArsenal\\itemacc_ca.paa\";\n")
	file.write("		items[] =\n")
	file.write("		{\n")

	for i, item in enumerate(content, 0):
		if (item[cc.COLUMN_TRADER_CATEGORY] == category):
			if (i < len(content)-1):
				line = "			\"" + item[cc.COLUMN_CLASS_NAME] + "\",\n"
			else:
				line = "			\"" + item[cc.COLUMN_CLASS_NAME] + "\"\n"
			file.write(line)
			#pInfo (line)

	file.write("		};\n")
	file.write("	};")

	pBuild ("Output content written.")
	file.close()
	pBuild ("Output file successfully released.")
pFooter ("Generating of trader categories finished.")
