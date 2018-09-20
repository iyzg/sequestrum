# Symlink Module

# Libraries
import os
from shutil import copytree, copyfile

import sequestrum.loggingModule as logMod

# Functions


def createSymlink(source, destination, pkgName = None):
    """
        Creates symlink from source to destination
    """
    try:
        os.symlink(source, destination)
    except OSError as error:
        logMod.printError("Unable to create symlink: {}".format(error), pkgName)
    else:
        logMod.printVerbose("Linking {} <-> {}".format(source, destination), pkgName)


def copyFile(source, destination):
    """
        Copys file from source to destination
    """
    try:
        copyfile(source, destination)
    except IOError:
        return False
    else:
        return True


def copyFolder(source, destination):
    """
        Copies frolder from source to destination
    """
    try:
        copytree(source, destination)
    except IOError:
        print("Location must be writable")
    else:
        print("Sucess copying folder ")


def symlinkSourceExists(sourcePath):
    """
        Checks to see if symlink source exists
    """

    # Check if file exists
    if not os.path.exists(sourcePath):
        return False

    # We cannot link symlinks
    if os.path.islink(sourcePath):
        return False

    return os.path.exists(sourcePath)
