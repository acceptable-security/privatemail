import os
def scanfolder():
	lineCount = 0
	for path, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
		for f in files:
			if f.endswith('.py') or f.endswith('.html') or f.endswith('.js'):
				lines = len(open(os.path.join(path, f)).read().split('\n'))
				print "[" + os.path.join(path, f) + "] -  LINECOUNT: " + str(lines)
				lineCount += lines

	return lineCount

if __name__ == "__main__":
	lc = scanfolder()
	print "TOTAL LINECOUNT: " + str(lc)
	input('Press ENTER to exit..')
