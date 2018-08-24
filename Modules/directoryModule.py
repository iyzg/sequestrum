#!/usr/bin/python
#
# Directory Module

# Libraries
import os
import sys
import shutil

# Create Folder
def createFolder(path):
    """
        Creates a folder
    """
    try:
        os.makedirs(path)
    except OSError:
        print("Sequestrum: Creation of folder failed")
    else:
        print("Sequestrum: Created successfully!")

# Delete Folder
def deleteFolder(path):
    """
        Deletes a folder
    """
    try:
        shutil.rmtree(path)
    except OSError:
        print("Sequestrum: Deletion of folder failed")
    else:
        print("Sequestrum: Deleted successfully!")

# Delete File 
def deleteFile(path):
    """
        Deletes file
    """
    try:
        os.remove(path)
    except OSError:
        print("REmoving of file failed")
    else:
        print("Successfully removed file")

# Check If Folder
def isFolder(path):
    """
        Checks to see if path is a folder
    """
    try:
        if os.path.isdir(path):
            return True
        else:
            return False
    except OSError:
        print("Sequestum: Folder checking failed")

# Check If File
def isFile(path):
    """
        Checks to see if path is a file
    """
    try: 
        if os.path.isfile(path):
            return True
        else:
            return False
    except OSError:
        print("Sequestrum: File check failed")

def setupDirectory(directoryKey, dotfilePath, homePath):
    """
        Setup dotfiles with all directories
    """
    newDirectoryPath = dotfilePath + configDict['options'][directoryKey]['directoryName'] + "/"
    dirMod.createFolder(newDirectoryPath)

    for link in configDict['options'][directoryKey]['links']:
        for key, value in links.items():
            sourceFile = homePath + value
            destFile = newDirectoryPath + key
            if symMod.symlinkSourceExists(sourceFile):
                if dirMod.isFolder(sourceFile):
                    symMod.copyFolder(sourceFile, destFile)
                elif dirMod.isFile(sourceFile):
                    symMod.copyFile(sourceFile, destFile)
                else:
                    return False
            else:
                return False
    return True
   
def installDirectory(directoryKey, dotfilePath, homePath):
    """
        Install all directories from dotfiles
    """
    directoryPath = dotfilePath + configDict['options'][directoryKey]['directoryName'] + "/"
    for link in configDict['options'][directoryKey]['links']:
        for key, value in link.items():
            sourceFile = directoryPath + key
            destFile = homePath + value
 
            if symMod.symlinkSourceExists(sourceFile):
                if dirMod.isFolder(sourceFile):
                    symMod.createSymlink(sourceFile, destFile)
                elif dirMod.isFile(sourceFile):
                    symMod.createSymlink(sourceFile, destFile)
                else:
                    return False
            else:
                return False
    return True

