# Symlink Module

# Libraries
import os
from shutil import copytree, copyfile

import logging


def create_symlink(source, destination, package_name=None):
    """
        Creates symlink from source to destination
    """

    try:
        os.symlink(source, destination)
    except OSError as error:
        logMod.print_error("Unable to create symlink: {}".format(error), package_name)
    else:
        logMod.print_verbose("Linking {} <-> {}".format(source, destination), package_name)


def copy_file(source, destination):
    """
        Copys file from source to destination
    """

    try:
        copyfile(source, destination)
    except IOError:
        return False
    else:
        return True


def copy_folder(source, destination):
    """
        Copies frolder from source to destination
    """

    try:
        copytree(source, destination)
    except IOError:
        print("Location must be writable")
    else:
        print("Sucess copying folder ")


def symlink_source_exists(sourcePath):
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
