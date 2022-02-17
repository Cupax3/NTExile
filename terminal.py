class bcolors:
	INFO = '\033[90m'
	RED = '\033[91m'
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def pHeader(*args):
	args = (f"{bcolors.HEADER}", "[START] ") + args + (f"{bcolors.ENDC}",)
	print (*args, sep='')

def pBuild(*args):
	args = (f"{bcolors.OKCYAN}", "[BUILD] ") + args + (f"{bcolors.ENDC}",)
	print (*args, sep='')

def pError(*args):
	args = (f"{bcolors.FAIL}", "[ERROR] ") + args + (f"{bcolors.ENDC}",)
	print (*args, sep='')

def pWarning(*args):
	args = (f"{bcolors.WARNING}", "[WARNING] ") + args + (f"{bcolors.ENDC}",)
	print (*args, sep='')

def pInfo(*args):
	args = (f"{bcolors.INFO}", "[INFO] ") + args + (f"{bcolors.ENDC}",)
	print (*args, sep='')

def pFooter(*args):
	args = (f"{bcolors.OKGREEN}", "[FINISH] ") + args + (f"{bcolors.ENDC}",)
	print (*args, sep='')
