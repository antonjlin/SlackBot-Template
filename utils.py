from datetime import datetime
from termcolor import cprint, colored
import colorama
import sys
colorama.init()

def log(text,color=None,prefix=None,timestamp=True,overWrite=False):
	if overWrite:
		sys.stdout.write("\x1b[1A") # Cursor up one line
		sys.stdout.write("\x1b[2K") # ERASE
	if prefix != None:
		task = "[" + str(prefix) + "] "
	else:
		task = ""
	if timestamp:
		timestamp = "[" + str(datetime.now().strftime("%H:%M:%S.%f")[:-4]) + "] "
	else:
		timestamp = ""
	total = "{}{}{}".format(task,timestamp,text)
	if color !=None:
		toPrint = colored(total, color)
	else:
		toPrint = total
	sys.stdout.write(toPrint + '\n')
	sys.stdout.flush()

javascript:(function(){document.findelementbyname("button").click()})()