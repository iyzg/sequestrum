# Symlink Module

# Libraries
import os
from shutil import copytree, copyfile

# Functions


def createSymlink(source, destination):
    """
        Creates symlink from source to destination
    """
    try:
        os.symlink(source, destination)
    except OSError:
        print("Sequestrum: Symlink failed")
    else:
        print("Sequestrum: Symlink success")


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


def symlinkLocationExists(sourcePath):
    """
        Checks to see if symlink source exists
    """
    return os.path.exists(sourcePath)
