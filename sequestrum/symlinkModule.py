# Symlink Module

# Libraries
import os
import sequestrum.loggingModule as logMod

# Functions


def createSymlink(source, destination, pkgName=None):
    """
        Creates symlink from source to destination
    """
    try:
        os.symlink(source, destination)
    except OSError as error:
        logMod.printError("Unable to create symlink: {}"
                          .format(error), pkgName)
        return False
    else:
        logMod.printVerbose("Linking {} <-> {}"
                            .format(source, destination), pkgName)
        return True


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

    return True
