# Directory Module

# Libraries
import os
import sys
import shutil
import pathlib
import sequestrum.loggingModule as logMod

# Create Folder


def createFolder(path, pkgName):
    """
        Creates a folder
    """
    try:
        os.makedirs(path)
    except OSError as error:
        logMod.printError(
            "Could not create folder \"{}\" due to following error: {}".format(path, error), pkgName)
    else:
        logMod.printVerbose(
            "Folder dosent exist and was created: {}".format(path), pkgName)

# Create Base Folder


def createBaseFolder(path, pkgName):
    """
        Create Base directory if needed
    """
    basePath = pathlib.Path(path).parent

    # Check if the base folder is a file
    if basePath.exists():
        # Check if the parent is a file or if its a symlink
        if basePath.is_file() or basePath.is_symlink():
            logMod.printError(
                "Base directory is a file or link: {}".format(basePath), pkgName)
            return False
        # If not, it must be a directory, so we are ok
        else:
            return True

    # Create path and parents (or ignore if folder already exists)
    try:
        basePath.mkdir(parents=True, exist_ok=True)
    except Exception as error:
        logMod.printError(
            "Could not create parent folder \"{}\" due to following error: {}".format(basePath, error), pkgName)
        return False
    else:
        logMod.printVerbose(
            "Parent folder dosent exist and was created: {}".format(basePath), pkgName)

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
    except OSError as error:
        print("Sequestrum: Deletion of folder failed: {}".format(error))
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
