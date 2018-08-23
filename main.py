#! /usr/bin/python
#
# Sequestrum - Dotfile Manager

# Libraries
import sys
import yaml
from pathlib import Path

sys.path.insert(0, '/home/plasma/Sequestrum/Modules')

# Modules
import directoryModule as dirMod
import symlinkModule as symMod
import argumentsModule as argMod

# Variables
homePath = str(Path.home()) + "/"
arguments = argMod.getArguments()

# Main Program
configFile = open("config.yaml", "r")
configDict = yaml.load(configFile)
directoryList = []

for key,value in configDict['options'].items():
    if key.endswith("Directory"):
        directoryList.append(key[:-9])

dotfilePath = homePath + configDict['options']['base']['dotfileDirectory'] + "/"

if arguments[0] in {"-i", "--install"}:
    if arguments[1] == "all":
        for key, value in configDict['options'].items():
            if key.endswith("Directory"):
                newDirectoryPath = dotfilePath + configDict['options'][key]['directoryName'] + "/"
                dirMod.createFolder(newDirectoryPath)

                for link in configDict['options'][key]['links']:
                    for key, value in link.items():
                        sourceFile = homePath + key
                        destFile = newDirectoryPath + value
                        if symMod.symlinkSourceExists(sourceFile):
                            symMod.createSymlink(sourceFile, destFile)

    elif arguments[1] in directoryList:
        for key,value in configDict['options'].items():
            if key == arguments[1] + "Directory":
                newDirectoryPath = dotfilePath + configDict['options'][key]['directoryName'] + "/"
                dirMod.createFolder(newDirectoryPath)

                for link in configDict['options'][key]['links']:
                    for key, value in link.items():
                        sourceFile = homePath + key
                        destFile = newDirectoryPath + value
                        if symMod.symlinkSourceExists(sourceFile):
                            symMod.createSymlink(sourceFile, destFile)
    else:
        print("Invalid Directory")
