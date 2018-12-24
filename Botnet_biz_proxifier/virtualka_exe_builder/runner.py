# -*- coding: utf-8 -*-

#@Botnet.biz Virtualbox packaging installer script runner
#@author Tomas Keske <admin@botnet.biz>
#@since 24.12.2018

from subprocess import check_output

def extractValue(data):

	for line in data.split('\n'):
		if ("Value") in line:
			arr = line.split(": ")
			return arr[1]

def changeTheSource(file, eVal):

	changedSource = []
	file = open("../proxifier_server.py", "r")

	for index,line in enumerate(file.split('\n')):
		if ("affid") in line:
			changedSource[index] = "affid = "+eVal
		else:
			changedSource[index] = line

	file.close()

	oFileName = "proxifier_server"+eVal+".py"

	output = open(oFileName)

	for line in changedSource:
		output.write(line)

	output.close()

	return oFileName

def runPyInstaller(fileName):
	p = subprocess.Popen(["pyinstaller", fileName], stdout=sys.stdout)
    p.communicate()

def runMsiInstaller():
	pass


if __name__ == '__main__':
	data = check_output("vboxcontrol guestproperty get user_id", shell=True).decode()
	eVal = extractValue(data)
	fileNameChanged = changeTheSource(eVal)
	runPyInstaller(fileNameChanged)
	