import sys
import csv
import csvconstants as cc

from terminal import *
pHeader ("Build step started: generate-trader-prices")

if (len(sys.argv) < 2):
	pError ("Not enough arguments.")
	exit()

pBuild ("Beginning parsing of trader prices from ", f"{bcolors.OKBLUE}", str(sys.argv[1]))

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

content = []

for row in csvContent:
	if (row[cc.COLUMN_TRADER_BOOLEAN] == "1"):
		content.append(row)

pBuild ("Tradeable goods successfully loaded.")

categories = []

pBuild ("Building category list.")

for row in content:
	if not row[cc.COLUMN_TRADER_CATEGORY] in categories:
		categories.append(row[cc.COLUMN_TRADER_CATEGORY])

pBuild ("Categories found: ", categories)
pBuild ("Preparing output file.")

for category in categories:
	try:
		file = open("output/traderstuff/" + category.lower() + ".hpp", "w")
		pBuild ("Output file successfully opened.")
	except IOError:
		pError ("Cannot open output file.")
		exit()

	pBuild ("Prepending output file information.")

	file.write("	///////////////////////////////////////////////////////////////////////////////" + '\n')
	file.write("	// NTC " + category + '\n')
	file.write("	///////////////////////////////////////////////////////////////////////////////" + '\n')

	for item in content:
		if (item[cc.COLUMN_TRADER_CATEGORY] == category):
			line = "	class " + item[cc.COLUMN_CLASS_NAME] + ' { quality = ' + item[cc.COLUMN_QUALITY] + '; price = ' + item[cc.COLUMN_BUY_PRICE] + '; sellPrice = ' + item[cc.COLUMN_SELL_PRICE] + '; };\n'
			file.write(line)
			#pInfo (line)

	pBuild ("Output content written.")
	file.close()
	pBuild ("Output file successfully released.")
pFooter ("Generating of trader prices finished.")
