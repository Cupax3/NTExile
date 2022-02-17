import sys
import csv
import csvconstants as cc

from terminal import *
pHeader ("Build step started: generate-zombie-loot")

if (len(sys.argv) < 2):
	pError ("Not enough arguments.")
	exit()

pBuild ("Beginning parsing of class file from ", f"{bcolors.OKBLUE}", str(sys.argv[1]))

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
	if (row[cc.COLUMN_ZOMBIE_BOOLEAN] == "1"):
		content.append(row)

pBuild ("Content successfully cached.")

categories = [None]

pBuild ("Building category list.")

for row in content:
	if not row[cc.COLUMN_ZOMBIE_LOOT_CATEGORY] in categories:
		categories.append(row[cc.COLUMN_ZOMBIE_LOOT_CATEGORY])

pBuild ("Categories found: ", categories)

categories.pop(0)

pBuild ("Preparing zombie loot output files.")

for category in categories:
	try:
		file = open("output/zombieloot/" + category.lower() + ".txt", "w")
		pBuild ("Output file successfully opened.")
	except IOError:
		pError ("Cannot open output file.")
		exit()

	pBuild("Prepending output file information.")

	for item in content:
		if (item[cc.COLUMN_ZOMBIE_LOOT_CATEGORY] == category):
			t = item[cc.COLUMN_ZOMBIE_LOOT_AMOUNT]
			if (t == ""):
				t = 1
			else:
				t = int(t)
			for x in range(t):
				line = "		\"" + item[cc.COLUMN_CLASS_NAME] + "\",\n"
				file.write(line)

	pBuild ("Output content written.")
	file.close()
	pBuild ("Output file successfully released.")
pFooter ("Generating of zombie loot finished.")
