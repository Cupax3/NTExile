import sys
import csv

from terminal import *

pHeader ("Build step started: parse-class-names")

if (len(sys.argv) < 3):
	pError ("Not enough arguments.")
	exit()

if (not sys.argv[1].endswith('.txt')):
	pError ("Wrong filetype. You missclicked, huh?")
	exit()

pBuild ("Beginning parsing of class names from ", f"{bcolors.OKBLUE}", str(sys.argv[1]), f"{bcolors.OKCYAN}", " to ", f"{bcolors.OKBLUE}", str(sys.argv[2]))

file = None

try:
	file = open(sys.argv[1])
	pBuild ("Source file found.")
except IOError:
	pError ("Source file does not exist.")
	exit()

content = file.read()
pBuild ("Source file read successfully.")
file.close()

content = content.replace('[', '')
content = content.replace(']', '')
content = content.replace('"', '')
content = content.split(',')
pBuild ("Source file parsed successfully.")

try:
	file = open(sys.argv[2], "r+", newline='')
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

pBuild ("Class file cached successfully.")

queue = [None]

for item in content:
	found = False
	for row in csvContent:
		if (row[0].replace('\'', '') == item):
			found = True
	if (not found):
		queue.append(item.split())
		pInfo("New: ", item)

queue.pop(0)

pBuild ("Queue successfully assembled.")

csvWriter = csv.writer(file)
csvWriter.writerows(queue)

pBuild ("Queue successfully written.")

file.close()

pBuild ("Class file successfully released.")
pFooter ("Parsing of class names complete.")
