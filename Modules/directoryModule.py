#!/usr/bin/python
#
# Directory Module

# Libraries
import os
import sys
import shutil

# Create Folder
def createFolder(path):
    try:
        os.makedirs(path)
    except OSError:
        print("Sequestrum: Creation of folder failed")
    else:
        print("Sequestrum: Created successfully!")

# Delete Folder
def deleteFolder(path):
    try:
        shutil.rmtree(path)
    except OSError:
        print("Sequestrum: Deletion of folder failed")
    else:
        print("Sequestrum: Deleted successfully!")

# Delete File 
def deleteFile(path):
    try:
        os.remove(path)
    except OSError:
        print("REmoving of file failed")
    else:
        print("Successfully removed file")

# Check If Folder
def isFolder(path):
    try:
        if os.path.isdir(path):
            return True
        else:
            return False
    except OSError:
        print("Sequestum: Folder checking failed")

# Check If File
def isFile(path):
    try: 
        if os.path.isfile(path):
            return True
        else:
            return False
    except OSError:
        print("Sequestrum: File check failed")
