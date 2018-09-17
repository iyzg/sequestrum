# Directory Module

# Libraries
import os
import sys
import shutil
import pathlib

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

# Create Base Folder


def createBaseFolder(path):
    """
        Create Base directory if needed
    """
    basePath = pathlib.Path(path).parent

    # Check if the base folder is a file
    if basePath.exists() and basePath.is_file():
        print("Sequestrum: Base directory is a file: {}".format(basePath))
        return False

    # Create path and parents (or ignore if folder already exists)
    basePath.mkdir(parents=True, exist_ok=True)
    return True

# Delete Folder


def deleteFolder(path):
    """
        Deletes a folder
    """

    basePath = pathlib.Path(path)
    
    if not basePath.exists():
        print("Sequestrum: Folder already deleted!")
        return

    try:
        if basePath.is_symlink():
            basePath.unlink()
        else:
            shutil.rmtree(basePath)
    except OSError as e:
        print("Sequestrum: Deletion of folder failed: {}".format(e))
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
