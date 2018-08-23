#!/usr/bin/python
#
# Symlink Module

# Libraries
import os

# Functions
def createSymlink(source, destination):
    try:
        os.symlink(source, destination)
    except OSError:
        print("Sequestrum: Symlink failed")
    else:
        print("Sequestrum: Symlink success")

def symlinkSourceExists(sourcePath):
    return os.path.exists(sourcePath)
