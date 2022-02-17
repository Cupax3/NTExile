import sys
import csv
import csvconstants as cc

from enum import IntFlag
class EncodedTable(IntFlag):
	CivilianLowerClass	= 1
	CivilianUpperClass	= 2
	Shop				= 4
	Industrial			= 8
	Factories			= 16
	VehicleService		= 32
	Military			= 64
	Medical				= 128
	Tourist				= 256
	Radiation			= 512
	All					= 1023

from terminal import *
pHeader ("Build step started: generate-weapon-loot")

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
	if (row[cc.COLUMN_LOOT_BOOLEAN] == "1"):
		t = row[cc.COLUMN_LOOT_AMOUNT]
		if (t == ""):
			t = 1
		else:
			t = int(t)
		for x in range(t):
			content.append(row)

pBuild ("Content successfully cached.")
pBuild ("Beginning encoding.")

# 10-bit table encoding
# CivillianLowerClass	0000000001 1
# CivillianUpperClass	0000000010 2
# Shop					0000000100 4
# Industrial			0000001000 8
# Factories				0000010000 16
# VehicleService		0000100000 32
# Military				0001000000 64
# Medical				0010000000 128
# Tourist				0100000000 256
# Radiation				1000000000 512
# All					1111111111 1023

def encodeBitflags(input):
	output = input

	for i in EncodedTable:
		output = output.replace(i.name, str(i.value))

	return output

for row in content:
	row[cc.COLUMN_LOOT_CATEGORY] = encodeBitflags(row[cc.COLUMN_LOOT_CATEGORY])
	if "-" in row[cc.COLUMN_LOOT_CATEGORY]:
		splitRow = row[cc.COLUMN_LOOT_CATEGORY].split("-")
		splitRow.pop(0)
		total = 1023
		for subString in splitRow:
			total - int(subString)
		row[cc.COLUMN_LOOT_CATEGORY] = str(total)
	elif "+" in row[cc.COLUMN_LOOT_CATEGORY]:
		splitRow = row[cc.COLUMN_LOOT_CATEGORY].split("+")
		total = 0
		for subString in splitRow:
			total + int(subString)
		row[cc.COLUMN_LOOT_CATEGORY] = str(total)

lootTables = [None]
EncodedTableHelper = [None]

for i in EncodedTable:
	EncodedTableHelper.append(i)

for i in range(1, 11):
	lootTables.append([None])
	for row in content:
		if int(row[cc.COLUMN_LOOT_CATEGORY]) & EncodedTableHelper[i].value:
			lootTables[i].append(row[cc.COLUMN_CLASS_NAME])

lootTables.pop(0)
EncodedTableHelper.pop(0)

for i in range(10):
	lootTables[i].pop(0)

dividedLootTables = [None]

def chunks(lst, n):
	for i in range(0, len(lst), n):
		yield lst[i:i + n]

for item in lootTables:
	dividedLootTables.append(list(chunks(item, 20)))

dividedLootTables.pop(0)

for i in range(10):
	try:
		file = open("output/loot/" + str(EncodedTableHelper[i].name) + ".txt", "w")
	except IOError:
		exit()

	j = 1;
	for item in dividedLootTables[i]:
		file.write("		" + str(EncodedTableHelper[i].name) + str(j) + "[] = {")
		output = ""
		for itemTwo in item:
			output += "\"" + itemTwo + "\", "
		output = output[:-2]
		file.write(output + "};\n")
		j += 1

	file.write("\n\n")

	file.write("		" + str(EncodedTableHelper[i].name) + "[] = {")
	output = ""
	for k in range(1, j):
		output += "\"" + str(EncodedTableHelper[i].name) + str(k) + "\", "
	output = output[:-2]
	file.write(output + "};\n")

	file.close()
