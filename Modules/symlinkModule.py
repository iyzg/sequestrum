#!/usr/bin/python
#
# Symlink Module

# Libraries
import os
from shutil import copytree, copyfile

# Functions
def createSymlink(source, destination):
    try:
        os.symlink(source, destination)
    except OSError:
        print("Sequestrum: Symlink failed")
    else:
        print("Sequestrum: Symlink success")

def copyFile(source, destination):
    try: 
        copyfile(source, destination)
    except IOError:
        print("Location must be writable")
    else:
        print("Success copying file")

def copyFolder(source, destination):
    try: 
        copytree(source, destination)
    except IOError: 
        print("Location must be writable")
    else:
        print("Sucess copying folder ")

def symlinkSourceExists(sourcePath):
    return os.path.exists(sourcePath)
