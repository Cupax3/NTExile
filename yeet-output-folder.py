import os,shutil

from terminal import *
pHeader ("Build step started: yeet-output-folder")

if (os.path.exists("output")):
	pBuild("Yeeting output folder.")
	shutil.rmtree("output")

pBuild ("Yeeted. Making folder.")

os.mkdir("output")
os.mkdir("output/traders")
os.mkdir("output/loot")
os.mkdir("output/zombieloot")
os.mkdir("output/traderstuff")

pFooter ("Yeet complete.")
