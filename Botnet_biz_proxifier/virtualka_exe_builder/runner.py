# -*- coding: utf-8 -*-

#@Botnet.biz Virtualbox packaging installer script runner
#@author Tomas Keske <admin@botnet.biz>
#@since 24.12.2018

import os
import sys
import ctypes
import subprocess
from subprocess import check_output
from shutil import copyfile

def extractValue(data):

	for line in data.split('\n'):
		if ("Value") in line:
			arr = line.split(": ")
			return arr[1]

def changeTheSource(eVal):

	changedSource = []


	with open("../proxifier_server.py", "r") as file:

		line = file.readlines()

		for x in line:
			if ("affid =") in x:
				changedSource.append("\taffid = '"+eVal+"'")
				changedSource.append("\n")
			elif ("&affid=") in x:
				changedSource.append(x.strip())
			else:
				changedSource.append(x)


	file.close()

	oFileName = "proxifier_server"+eVal+".py"

	output = open(os.path.join(os.getcwd()+"\\..\\", oFileName), "w")

	for line in changedSource:
		output.write(line)

	output.close()

	return oFileName

def runPyInstaller(fileName):

	p = subprocess.Popen(["pyinstaller", "--onefile", os.path.join(os.getcwd()+"\\..\\", fileName)], stdout=sys.stdout)
	p.wait()

def runMsiInstaller(cwd, eVal):
	os.chdir(os.path.join(cwd+"\\..\\", "installer"))
	p = subprocess.Popen(["python", "msiinstaller.py",  "installer-"+eVal+".json"], stdout=sys.stdout)
	p.wait()

def changeInstallerConfig(eVal):
	os.chdir(os.path.join(cwd+"\\..\\", "installer"))

	print(os.getcwd())
	installer = open("installer.json", "r")

	string = installer.read()
	installer.close()
	modified = string.replace("BotInstaller", "BotInstaller_"+eVal)
	instEval = open("installer-"+eVal+".json", "w")
	instEval.write(modified)
	instEval.close()


	return "BotInstaller_"+eVal+"-1.0.0-64.msi"

def copyInstallerToSharedFolder(installerName):
	path = os.path.join(cwd+"\\..\\", "installer")
	os.chdir(path)
	copyfile(path+"\\"+installerName, r"\\VBOXSVR\\downloads\\"+installerName)

def cleanUp():
	os.chdir(os.getcwd()+"..\\installer");
	#TODO


if __name__ == '__main__':
	data = check_output("vboxcontrol guestproperty get user_id", shell=True).decode()
	eVal = extractValue(data).strip()
	fileNameChanged = changeTheSource(eVal)
	fileNameChanged = fileNameChanged.strip()
	cwd = os.getcwd()
	runPyInstaller(fileNameChanged)
	copyfile(cwd+"\\dist\\proxifier_server"+eVal+".exe", cwd+"\\..\\installer\\main\\"+"proxifier_server"+eVal+".exe")
	installerName = changeInstallerConfig(eVal)
	runMsiInstaller(cwd, eVal)
	copyInstallerToSharedFolder(installerName)
	os.system('shutdown -s')