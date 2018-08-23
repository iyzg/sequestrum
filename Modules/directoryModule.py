#!/usr/bin/python
#
# Directory Module

# Libraries
import os 

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
        os.rmdir(path)
    except OSError:
        print("Sequestrum: Deletion of folder failed")
    else:
        print("Sequestrum: Deleted successfully!")

# Check If Folder
def isFolder(path):
    try:
        if os.path.isdir(path):
            return True
        else:
            return False
    except OSError:
        print("Sequestum: Folder checking failed")

