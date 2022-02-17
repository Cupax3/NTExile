import sys
import csv
import csvconstants as cc

from terminal import *
pHeader ("Build step started: generate-trader-includes")

if (len(sys.argv) < 2):
	pError ("Not enough arguments.")
	exit()

pBuild ("Beginning parsing of trader includes from ", f"{bcolors.OKBLUE}", str(sys.argv[1]))

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

pBuild ("Preparing arsenal output file.")

try:
	file = open("output/traders/CfgExileArsenal.txt", "w")
	pBuild ("Arsenal output file successfully opened.")
except IOError:
	pError ("Cannot open arsenal output file.")
	exit()

for category in categories:
	file.write("	#include \"ntcustom\\" + category.lower() + ".hpp\"\n")

file.close()

pBuild ("Arsenal output file successfuly built.")
pBuild ("Preparing trader category output file.")

try:
	file = open("output/traders/CfgTraderCategories.txt", "w")
	pBuild ("Trade category output file successfully opened.")
except IOError:
	pError ("Cannot open trader category output file.")
	exit()

for category in categories:
	file.write("	#include \"ntcustom\\" + category.lower() + "_category.hpp\"\n")

file.close()

pBuild ("Trader category output file successfully built.")
#pBuild ("Preparing trader type output.")
#
#try:
#	file = open("output/traders/CfgTraders.txt", "w")
#	pBuild ("Trader type output file successfully opened.")
#except IOError:
#	pError ("Cannot open trader type output file.")
#	exit()

traderTypes = [None]

pBuild ("Building trader type list.")

for row in content:
	if not row[cc.COLUMN_TRADER_TYPE] in traderTypes:
		traderTypes.append(row[cc.COLUMN_TRADER_TYPE])

traderTypes.pop(0)

pBuild ("Trader types found: ", traderTypes)

for trype in traderTypes:
	pBuild ("Trying to write trader " + trype + ".")

	typeCategories = [None]

	for row in content:
		if (row[cc.COLUMN_TRADER_TYPE] == trype):
			if not row[cc.COLUMN_TRADER_CATEGORY] in typeCategories:
				typeCategories.append(row[cc.COLUMN_TRADER_CATEGORY])

	typeCategories.pop(0)

	pInfo (typeCategories)

	try:
		file = open("output/traders/Cfg" + trype + ".txt", "w")
		pBuild (trype + " file successfully opened.")
	except IOError:
		pError ("Cannot open " + trype + " output file.")
		exit()

	for category in typeCategories:
		file.write("			\"NTCustom" + category + "\",\n")
	file.close()

pFooter ("Trader types sucessfully done.")
