import sys
import csv
import csvconstants as cc

from terminal import *
from copy import copy

pHeader ("Build step started: import-formatted-csv")

if (len(sys.argv) < 3):
	pError ("Not enough arguments.")
	exit()

pBuild ("Beginning parsing of class names from ", f"{bcolors.OKBLUE}", str(sys.argv[1]), f"{bcolors.OKCYAN}", " to ", f"{bcolors.OKBLUE}", str(sys.argv[2]))

new = None
file = None

try:
	new = open(sys.argv[1])
	pBuild ("Import file successfully opened.")
	file = open(sys.argv[2])
	pBuild ("Class file successfully opened.")
except IOError:
	pError ("Cannot open files.")
	exit()

newReader = csv.reader(new)
fileReader = csv.reader(file)

pBuild ("CSV reader successfully initiated.")

newContent = []
fileContent = []

for row in newReader:
	newContent.append(row)
newContent.pop(0)

fileContent.append(fileReader.__next__())

def mergeRows(a, b):
	a.insert(cc.COLUMN_CAPACITY, b[cc.IMPORT_CAPACITY])
	a.insert(cc.COLUMN_MAGS_ARMOR, b[cc.IMPORT_MAGS_ARMOR])
	a.insert(cc.COLUMN_MASS, b[cc.IMPORT_MASS])
	a.insert(cc.COLUMN_PASSTHROUGH, b[cc.IMPORT_PASSTHROUGH])
	a.insert(cc.COLUMN_READABLE_NAME, b[cc.IMPORT_READABLE_NAME])
	a.insert(cc.COLUMN_TYPE, b[cc.IMPORT_TYPE])

	return a

def toSize(x, y):
	for i in range(y):
		if (len(x) < i + 1):
			x.insert(i, "")
		if (x[i] == None):
			x[i] == ""

	return x

def formatToClass(x):
	x = toSize(x, cc.MAX_SIZE)
	temp = copy(x)

	pInfo(len(x))
	exit()

	x[cc.COLUMN_CLASS_NAME] = temp[cc.IMPORT_CLASS_NAME]
	x[cc.COLUMN_MAGS_ARMOR] = temp[cc.IMPORT_MAGS_ARMOR]
	x[cc.COLUMN_MASS] = temp[cc.IMPORT_MASS]
	x[cc.COLUMN_PASSTHROUGH] = temp[cc.IMPORT_PASSTHROUGH]
	x[cc.COLUMN_READABLE_NAME] = temp[cc.IMPORT_READABLE_NAME]
	x[cc.COLUMN_TYPE] = temp[cc.IMPORT_TYPE]
	x[cc.COLUMN_LOOT_BOOLEAN] = "0"
	x[cc.COLUMN_TRADER_BOOLEAN] = "0"
	x[cc.COLUMN_ZOMBIE_BOOLEAN] = "0"
	x[cc.COLUMN_BLACK_MARKET_BOOLEAN] = "0"

	return x

for row in fileReader:
	for x in newContent:
		if (row[cc.COLUMN_CLASS_NAME] == x[cc.IMPORT_CLASS_NAME]):
			row = mergeRows(row, x)
			fileContent.append(row)
			newContent.remove(x)

for x in newContent:
	fileContent.append(formatToClass(x))

file.close()

try:
	file = open(sys.argv[2], "r+", newline="")
	pBuild ("Class file successfully reopened.")
except IOError:
	pError ("Cannot write to file.")
	exit()

fileWriter = csv.writer(file)
fileWriter.writerows(fileContent)

new.close()
file.close()
