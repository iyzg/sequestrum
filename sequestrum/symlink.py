# Symlink Module

# Libraries
import os
from shutil import copytree, copyfile

import sequestrum.logging as logging


def create_symlink(source, destination):
    """
        Creates symlink from source to destination
    """

    try:
        os.symlink(source, destination)
    except OSError as error:
        logging.print_error("Unable to create symlink: {}".format(error))
    else:
        logging.print_verbose("Linking {} <-> {}".format(source, destination))


def copy_file(source, destination):
    """
        Copys file from source to destination
    """

    try:
        copyfile(source, destination)
    except IOError as error:
        logging.print_error("Unable to copy file: {}".format(error))
    else:
        logging.print_verbose("Copied {} --> {}".format(source, destination))


def copy_folder(source, destination):
    """
        Copies frolder from source to destination
    """

    try:
        copytree(source, destination)
    except IOError as error:
        logging.print_error("Unable to copy folder: {}".format(error))
    else:
        logging.print_verbose("Copied {} --> {}".format(source, destination))


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
