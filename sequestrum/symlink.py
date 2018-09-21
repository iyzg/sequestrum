import os

from sequestrum import logging


def create(source, destination, pkgName=None):
    """
        Creates symlink from source to destination
    """
    try:
        os.symlink(source, destination)
    except OSError as error:
        logging.error("Unable to create symlink: {}"
                      .format(error), pkgName)
        return False
    else:
        logging.debug("Linking {} <-> {}"
                      .format(source, destination), pkgName)
        return True


def source_exists(sourcePath):
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
