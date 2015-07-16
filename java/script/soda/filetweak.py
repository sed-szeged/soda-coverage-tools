from .feedback import *
import os
import re

print(info(as_proper("File tweaking")+" features loaded."))

def insert(what, into, where):
	with open(into, 'r') as f:
		contents = f.readlines()
	index = None
	line = None
	for i in range(len(contents)):
		if re.search(where, contents[i]):
			line = contents[i]
			index = i
			break
	else:
		raise Exception("Pattern not found in '%s' file" % as_proper(into))
	contents.insert(index, what)
	print(info("Insert into '%s' file before: '%s'" % (into, line.strip())))
	with open(into+".tmp", 'w') as f:
		f.write("".join(contents))
	os.rename(into, into+".original")
	os.rename(into+".tmp", into)
