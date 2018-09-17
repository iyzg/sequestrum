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
    except OSError as e:
        print(str(e))
    else:
        print("Sequestrum: Created successfully!")

# Delete Folder


def deleteFolder(path):
    """
        Deletes a folder
    """
    try:
        shutil.rmtree(path)
    except OSError as e:
        print(str(e))
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

# Grab all package names
def grabPackageNames(path):
    packageList = []
    for name in os.listdir(path):
        if os.path.isdir(path):
            packageList.append(name)

    return packageList
